import logging
from typing import List, Dict, Any

import aiofiles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.agent import Agent
from app.schemas.agent import Agent as AgentSchema
from app.utils.exceptions import AgentCreationError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# This configuration is based on the project's engineering context document.
AGENTS_CONFIG = {
    "story_architect": {"name": "Story Architect Agent", "guide_file": "story_architect_agent_guide.md"},
    "realism_critic": {"name": "Realism Critic Agent", "guide_file": "realism_critic__agent_guide.md"},
    "strategic_analyst": {"name": "Strategic Analyst Agent", "guide_file": "strategic_analyst_agent_guide.md"},
    "character_development": {"name": "Character Development Agent", "guide_file": "character_development_agent_guide.md"},
    "character_expansion": {"name": "Character Expansion Agent", "guide_file": "character_expansion_agent_guide.md"},
    "world_building": {"name": "World-Building Agent", "guide_file": "world_building_agent_guide.md"},
    "dialogue_voice": {"name": "Dialogue & Voice Agent", "guide_file": "dialogue_voice_agent_guide.md"},
    "theme": {"name": "Theme Agent", "guide_file": "theme_agent_guide.md"},
    "genre_tone": {"name": "Genre & Tone Agent", "guide_file": "genre_tone_agent_guide.md"},
    "pacing": {"name": "Pacing Agent", "guide_file": "pacing_agent_guide.md"},
    "conflict_tension": {"name": "Conflict & Tension Agent", "guide_file": "conflict_tension_agent_guide.md"},
}

class AgentManagerService:
    """
    A service responsible for creating, configuring, and managing the team of AI agents for a session.
    """

    def __init__(self, db_session: AsyncSession):
        """
        Initializes the service with a database session.

        Args:
            db_session: An asynchronous SQLAlchemy session.
        """
        self.db = db_session

    async def create_agent_team_for_session(self, session_id: str) -> List[AgentSchema]:
        """
        Creates a full team of 11 agents for a given session based on the predefined configuration.
        It reads the guide file for each agent, creates a database record, and returns the list of created agents.

        Args:
            session_id: The UUID of the session for which to create the agents.

        Returns:
            A list of Pydantic schemas for the newly created agents.

        Raises:
            AgentCreationError: If an agent's guide file cannot be found or if there's a database error.
        """
        logger.info(f"Starting agent team creation for session_id: {session_id}")
        created_agents = []

        try:
            for agent_type, config in AGENTS_CONFIG.items():
                guide_content = await self._load_guide_file(config["guide_file"])

                new_agent = Agent(
                    session_id=session_id,
                    agent_type=agent_type,
                    agent_name=config["name"],
                    guide_content=guide_content,
                    # Other model parameters will use their defaults as defined in the model
                )
                self.db.add(new_agent)
                created_agents.append(new_agent)

            await self.db.commit()

            for agent in created_agents:
                await self.db.refresh(agent)

            logger.info(f"Successfully created {len(created_agents)} agents for session_id: {session_id}")
            return [AgentSchema.from_orm(agent) for agent in created_agents]

        except FileNotFoundError as e:
            logger.error(f"Failed to create agents: Guide file not found - {e.filename}", exc_info=True)
            await self.db.rollback()
            raise AgentCreationError(f"Could not find guide file: {e.filename}")
        except Exception as e:
            logger.error(f"An unexpected database error occurred during agent creation: {e}", exc_info=True)
            await self.db.rollback()
            raise AgentCreationError(f"A database error prevented agent creation: {e}")

    async def get_agents_for_session(self, session_id: str) -> List[AgentSchema]:
        """
        Retrieves all agents associated with a given session from the database.

        Args:
            session_id: The UUID of the session.

        Returns:
            A list of Pydantic schemas for the agents.
        """
        result = await self.db.execute(select(Agent).where(Agent.session_id == session_id))
        agents = result.scalars().all()
        return [AgentSchema.from_orm(agent) for agent in agents]

    async def _load_guide_file(self, filename: str) -> str:
        """
        Asynchronously reads the content of an agent's guide file.
        Note: The path is relative to the project root.
        Since the CWD is /app/backend, we need to go up one level.
        """
        # Correct path from /app/backend to /app/<filename>
        filepath = f"../{filename}"
        try:
            async with aiofiles.open(filepath, mode='r', encoding='utf-8') as f:
                content = await f.read()
                return content
        except FileNotFoundError:
            logger.error(f"Guide file not found at path: {filepath}")
            raise

    def get_agent_config(self, agent_type: str) -> Dict[str, Any]:
        """
        Retrieves the static configuration for a specific agent type.

        Args:
            agent_type: The type of the agent (e.g., 'story_architect').

        Returns:
            A dictionary containing the agent's configuration.
        """
        config = AGENTS_CONFIG.get(agent_type)
        if not config:
            raise ValueError(f"No configuration found for agent type: {agent_type}")
        return config