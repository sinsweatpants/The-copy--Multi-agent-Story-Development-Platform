import logging
import json
from typing import Tuple, List, Dict, Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.idea import Idea
from app.schemas.idea import Idea as IdeaSchema, IdeaCreate
from app.schemas.creative_brief import CreativeBrief
from app.integrations.gemini.client import GeminiClient
from app.integrations.gemini.prompts import create_story_prompt, create_character_enhancement_prompt
from app.utils.exceptions import IdeaGenerationError
from app.models.agent import Agent as AgentModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IdeaGeneratorService:
    """
    Service responsible for the two-step idea generation process involving the
    Story Architect and Character Development agents.
    """

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def generate_competing_ideas(
        self,
        session_id: UUID,
        api_key: str, # Assuming API key is passed down for client creation
        brief: CreativeBrief,
        agents: List[AgentModel]
    ) -> Tuple[IdeaSchema, IdeaSchema]:
        """
        Orchestrates the generation of two complete, competing story ideas.

        Args:
            session_id: The UUID of the current session.
            api_key: The user's Gemini API key.
            brief: The user's creative brief.
            agents: The list of initialized agents for the session.

        Returns:
            A tuple containing the two generated Idea schemas.

        Raises:
            IdeaGenerationError: If any step of the generation process fails.
        """
        try:
            logger.info(f"Starting competing idea generation for session {session_id}")

            # 1. Get the specialized agents
            story_architect = self._get_agent_by_type(agents, "story_architect")
            char_developer = self._get_agent_by_type(agents, "character_development")

            # 2. Generate two story structures from the Story Architect
            story_architect_client = GeminiClient(api_key, story_architect.model_name)
            story_prompt = create_story_prompt(brief, num_variations=2)

            story_structures_raw = await story_architect_client.generate_content(story_prompt)
            story_structures = self._parse_llm_json_response(story_structures_raw, expected_keys=['variation_1', 'variation_2'])

            structure_1 = story_structures['variation_1']
            structure_2 = story_structures['variation_2']

            # 3. Enhance each structure with the Character Development agent
            char_developer_client = GeminiClient(api_key, char_developer.model_name)

            idea_1_full = await self._enhance_structure(char_developer_client, structure_1, brief)
            idea_2_full = await self._enhance_structure(char_developer_client, structure_2, brief)

            # 4. Save the final ideas to the database
            idea_1_db = await self._save_idea(session_id, 1, idea_1_full, [story_architect.agent_type, char_developer.agent_type])
            idea_2_db = await self._save_idea(session_id, 2, idea_2_full, [story_architect.agent_type, char_developer.agent_type])

            logger.info(f"Successfully generated and saved two ideas for session {session_id}")

            return IdeaSchema.from_orm(idea_1_db), IdeaSchema.from_orm(idea_2_db)

        except Exception as e:
            logger.error(f"Failed to generate competing ideas for session {session_id}: {e}", exc_info=True)
            raise IdeaGenerationError(f"Idea generation failed: {e}")

    async def _enhance_structure(self, client: GeminiClient, structure: Dict[str, Any], brief: CreativeBrief) -> Dict[str, Any]:
        """Calls the character developer and merges results."""
        prompt = create_character_enhancement_prompt(structure, brief)
        enhancement_raw = await client.generate_content(prompt)
        enhancements = self._parse_llm_json_response(enhancement_raw, expected_keys=['main_characters_enhanced'])

        # Merge the enhanced characters back into the original structure
        structure['main_characters'] = enhancements['main_characters_enhanced']
        return structure

    async def _save_idea(self, session_id: UUID, idea_number: int, idea_data: Dict[str, Any], generated_by: List[str]) -> Idea:
        """Saves a generated idea to the database."""
        idea_create_schema = IdeaCreate(
            session_id=session_id,
            idea_number=idea_number,
            title=idea_data.get("title", "Untitled"),
            logline=idea_data.get("logline", "No logline provided."),
            synopsis=idea_data.get("synopsis", "No synopsis provided."),
            three_act_structure=idea_data.get("three_act_structure", {}),
            main_characters=idea_data.get("main_characters", []),
            key_scenes=idea_data.get("key_scenes", []),
            thematic_elements=idea_data.get("thematic_elements", []),
            unique_selling_points=idea_data.get("unique_selling_points", []),
            generated_by_agents=generated_by
        )

        new_idea = Idea(**idea_create_schema.dict())
        self.db.add(new_idea)
        await self.db.commit()
        await self.db.refresh(new_idea)
        return new_idea

    def _get_agent_by_type(self, agents: List[AgentModel], agent_type: str) -> AgentModel:
        """Finds a specific agent from the list by its type."""
        for agent in agents:
            if agent.agent_type == agent_type:
                return agent
        raise IdeaGenerationError(f"Agent of type '{agent_type}' not found in the provided list.")

    def _parse_llm_json_response(self, response: str, expected_keys: List[str]) -> Dict[str, Any]:
        """
        Parses a JSON string from an LLM, ensuring it's valid and contains expected keys.
        This is a critical "blind" step. We assume the LLM returns a markdown code block with JSON.
        """
        try:
            # Clean up markdown code block fences
            if response.strip().startswith("```json"):
                response = response.strip()[7:-3].strip()

            data = json.loads(response)

            for key in expected_keys:
                if key not in data:
                    raise KeyError(f"Missing expected key in LLM response: '{key}'")
            return data
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON from LLM response: {e}\nResponse was: {response}")
            raise IdeaGenerationError(f"Invalid JSON format from LLM: {e}")
        except KeyError as e:
            logger.error(f"Key error in LLM response: {e}\nResponse was: {response}")
            raise IdeaGenerationError(f"Missing key in LLM response: {e}")