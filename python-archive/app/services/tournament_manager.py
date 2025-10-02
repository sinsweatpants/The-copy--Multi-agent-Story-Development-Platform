import asyncio
import logging
import json
import random
from typing import Tuple, List, Dict, Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tournament import Tournament
from app.models.tournament_turn import TournamentTurn
from app.schemas.idea import Idea as IdeaSchema
from app.models.agent import Agent as AgentModel
from app.integrations.gemini.client import GeminiClient
from app.integrations.gemini.prompts import create_tournament_argument_prompt
from app.schemas.tournament import Tournament as TournamentSchema, TournamentTurn as TournamentTurnSchema, Argument
from app.api.websocket import ConnectionManager
from app.utils.exceptions import TournamentError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TournamentManager:
    """
    Service to manage and execute the turn-based tournament of minds.
    """

    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.max_turns = 8 # As specified in the engineering context

    async def conduct_tournament(
        self,
        session_id: UUID,
        api_key: str,
        ideas: Tuple[IdeaSchema, IdeaSchema],
        reviews: Dict[str, Any],
        agents: List[AgentModel],
        ws_manager: ConnectionManager
    ) -> TournamentSchema:
        """
        Conducts the full tournament from initialization to completion.

        Args:
            session_id: The UUID of the current session.
            api_key: The user's Gemini API key.
            ideas: The two competing ideas.
            reviews: The aggregated reviews from the previous phase.
            agents: The list of initialized agents.
            ws_manager: The WebSocket connection manager for broadcasting updates.

        Returns:
            The completed tournament data.
        """
        logger.info(f"Starting tournament for session {session_id}")

        # 1. Initialize the tournament in the database
        tournament_db = await self._create_tournament_record(session_id)

        previous_turns_data: List[TournamentTurnSchema] = []

        for turn_num in range(1, self.max_turns + 1):
            await ws_manager.broadcast_to_session(session_id, {"type": "turn_start", "payload": {"turn": turn_num}})

            # 2. Execute a single turn
            turn_result = await self._execute_turn(
                tournament_db.id,
                api_key,
                turn_num,
                reviews,
                agents,
                previous_turns_data
            )
            previous_turns_data.append(turn_result)

            # 3. Broadcast the turn result
            await ws_manager.broadcast_to_session(session_id, {"type": "turn_result", "payload": turn_result.dict()})

        # 4. Finalize the tournament
        tournament_db.status = "completed"
        self.db.add(tournament_db)
        await self.db.commit()
        await self.db.refresh(tournament_db)

        logger.info(f"Tournament completed for session {session_id}")

        # We need to load the turns relationship to return the full object
        # This is a simplified representation. A real implementation would query the turns.
        final_tournament_schema = TournamentSchema.from_orm(tournament_db)
        final_tournament_schema.turns = previous_turns_data
        return final_tournament_schema

    async def _execute_turn(
        self,
        tournament_id: UUID,
        api_key: str,
        turn_number: int,
        reviews: Dict[str, Any],
        agents: List[AgentModel],
        previous_turns: List[TournamentTurnSchema]
    ) -> TournamentTurnSchema:
        """Executes a single turn of the tournament."""

        # Simple logic to select a subset of agents for the turn
        participants = random.sample(agents, k=min(len(agents), 4))
        participant_names = [p.agent_type for p in participants]
        logger.info(f"Executing Turn {turn_number} with participants: {participant_names}")

        argument_tasks = []
        for agent in participants:
            task = self._get_agent_argument(api_key, agent, reviews.get(agent.agent_type, {}), previous_turns)
            argument_tasks.append(task)

        arguments = await asyncio.gather(*argument_tasks)

        # Save the turn to the database
        turn_db = await self._save_turn(tournament_id, turn_number, participant_names, arguments)
        return TournamentTurnSchema.from_orm(turn_db)

    async def _get_agent_argument(
        self, api_key: str, agent: AgentModel, review: Dict[str, Any], previous_turns: List[TournamentTurnSchema]
    ) -> Argument:
        """Gets a structured argument from a single agent."""
        client = GeminiClient(api_key, agent.model_name)
        prompt = create_tournament_argument_prompt(agent.guide_content, review, previous_turns)

        raw_argument = await client.generate_content(prompt)
        parsed_argument = self._parse_argument_response(raw_argument, agent.agent_name)
        return Argument(**parsed_argument)

    async def _create_tournament_record(self, session_id: UUID) -> Tournament:
        """Creates the initial tournament record in the database."""
        new_tournament = Tournament(session_id=session_id, max_turns=self.max_turns)
        self.db.add(new_tournament)
        await self.db.commit()
        await self.db.refresh(new_tournament)
        return new_tournament

    async def _save_turn(
        self, tournament_id: UUID, turn_number: int, participants: List[str], arguments: List[Argument]
    ) -> TournamentTurn:
        """Saves a completed turn to the database."""
        turn_data = {
            "tournament_id": tournament_id,
            "turn_number": turn_number,
            "participating_agents": participants,
            "arguments": [arg.dict() for arg in arguments]
        }
        new_turn = TournamentTurn(**turn_data)
        self.db.add(new_turn)
        await self.db.commit()
        await self.db.refresh(new_turn)
        return new_turn

    def _parse_argument_response(self, response: str, agent_name: str) -> Dict[str, Any]:
        """Parses the JSON response for an agent's argument."""
        try:
            if response.strip().startswith("```json"):
                response = response.strip()[7:-3].strip()

            data = json.loads(response)
            data['agent_name'] = agent_name # Inject agent name into the parsed data
            return data
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Failed to parse argument from {agent_name}: {e}\nResponse: {response}")
            raise TournamentError(f"Could not parse argument from {agent_name}: {e}")