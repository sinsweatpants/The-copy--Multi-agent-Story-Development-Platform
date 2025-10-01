import asyncio
import logging
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.session import Session
from app.services.agent_manager import AgentManagerService
from app.services.idea_generator import IdeaGeneratorService
from app.services.review_engine import ReviewEngineService
from app.services.tournament_manager import TournamentManager
from app.services.decision_maker import DecisionMakerService
from app.schemas.creative_brief import CreativeBrief
from app.api.websocket import ConnectionManager
from app.utils.exceptions import OrchestrationError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MasterOrchestratorService:
    """
    The central orchestrator that manages the entire narrative development lifecycle.
    It coordinates all other services and manages the session state.
    """

    def __init__(self, db_session: AsyncSession, websocket_manager: ConnectionManager):
        self.db = db_session
        self.ws_manager = websocket_manager
        # Initialize all required services
        self.agent_manager = AgentManagerService(db_session)
        self.idea_generator = IdeaGeneratorService(db_session)
        self.review_engine = ReviewEngineService(db_session)
        self.tournament_manager = TournamentManager(db_session)
        self.decision_maker = DecisionMakerService(db_session)

    async def run_full_cycle(self, session_id: UUID, brief: CreativeBrief):
        """
        Runs the entire narrative development process from start to finish.
        This is the main entry point after a session and brief are created.
        """
        try:
            logger.info(f"Orchestrator starting full cycle for session_id: {session_id}")

            # Phase 1: Create Agent Team
            await self._update_session_status(session_id, "agents_creating", "agent_creation")
            await self.ws_manager.broadcast_to_session(session_id, {"type": "status_update", "payload": "Creating agent team..."})
            agents = await self.agent_manager.create_agent_team_for_session(session_id)
            if not agents or len(agents) != 11:
                raise OrchestrationError(f"Failed to create the full team of 11 agents. Only {len(agents)} were created.")

            # Phase 2: Generate Competing Ideas
            await self._update_session_status(session_id, "ideas_generating", "idea_generation")
            await self.ws_manager.broadcast_to_session(session_id, {"type": "status_update", "payload": "Generating competing ideas..."})
            idea_a, idea_b = await self.idea_generator.generate_competing_ideas(session_id, brief, agents)
            await self.ws_manager.broadcast_to_session(session_id, {"type": "ideas_generated", "payload": {"idea_a": idea_a.dict(), "idea_b": idea_b.dict()}})

            # Phase 3: Conduct Independent Reviews
            await self._update_session_status(session_id, "reviewing", "independent_review")
            await self.ws_manager.broadcast_to_session(session_id, {"type": "status_update", "payload": "Agents are conducting independent reviews..."})
            reviews = await self.review_engine.conduct_independent_reviews(session_id, (idea_a, idea_b), agents, brief)
            await self.ws_manager.broadcast_to_session(session_id, {"type": "reviews_completed", "payload": reviews})

            # Phase 4: Run the Tournament
            await self._update_session_status(session_id, "tournament_active", "tournament")
            await self.ws_manager.broadcast_to_session(session_id, {"type": "status_update", "payload": "The tournament of minds has begun!"})
            tournament_result = await self.tournament_manager.conduct_tournament(session_id, (idea_a, idea_b), reviews, agents, self.ws_manager)

            # Phase 5: Make Final Decision
            await self._update_session_status(session_id, "decision_making", "final_decision")
            await self.ws_manager.broadcast_to_session(session_id, {"type": "status_update", "payload": "The final decision is being made..."})
            final_decision = await self.decision_maker.make_final_decision(session_id, tournament_result)
            await self.ws_manager.broadcast_to_session(session_id, {"type": "decision_made", "payload": final_decision.dict()})

            # Finalization
            await self._update_session_status(session_id, "completed", "completed")
            await self.ws_manager.broadcast_to_session(session_id, {"type": "status_update", "payload": "Session completed successfully."})
            logger.info(f"Orchestrator finished full cycle for session_id: {session_id}")

        except Exception as e:
            logger.error(f"Orchestration cycle failed for session_id {session_id}: {e}", exc_info=True)
            await self._update_session_status(session_id, "failed", "failed")
            await self.ws_manager.broadcast_to_session(session_id, {"type": "error", "payload": f"A critical error occurred: {e}"})
            # Re-raise to be handled by the API layer
            raise

    async def _update_session_status(self, session_id: UUID, status: str, phase: str):
        """
        Updates the status and phase of a session in the database.
        """
        session = await self.db.get(Session, session_id)
        if not session:
            raise OrchestrationError(f"Session with id {session_id} not found for status update.")

        session.status = status
        session.current_phase = phase

        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        logger.info(f"Session {session_id} status updated to '{status}' and phase to '{phase}'.")