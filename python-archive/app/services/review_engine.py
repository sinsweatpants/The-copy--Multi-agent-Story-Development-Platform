import asyncio
import logging
import json
from typing import Tuple, List, Dict, Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.review import Review
from app.schemas.review import Review as ReviewSchema, ReviewCreate
from app.schemas.idea import Idea as IdeaSchema
from app.schemas.creative_brief import CreativeBrief
from app.models.agent import Agent as AgentModel
from app.integrations.gemini.client import GeminiClient
from app.integrations.gemini.prompts import create_review_prompt
from app.utils.exceptions import ReviewEngineError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReviewEngineService:
    """
    Service responsible for orchestrating the independent review phase, where each
    agent critiques the two competing ideas.
    """

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def conduct_independent_reviews(
        self,
        session_id: UUID,
        api_key: str,
        ideas: Tuple[IdeaSchema, IdeaSchema],
        agents: List[AgentModel],
        brief: CreativeBrief
    ) -> Dict[str, Any]:
        """
        Manages the process of having each agent review both ideas independently.

        Args:
            session_id: The UUID of the current session.
            api_key: The user's Gemini API key.
            ideas: A tuple containing the two generated ideas.
            agents: The list of initialized agents for the session.
            brief: The user's creative brief.

        Returns:
            A dictionary containing the aggregated reviews from all agents.
        """
        logger.info(f"Starting independent review phase for session {session_id}")

        idea_1, idea_2 = ideas
        review_tasks = []

        for agent in agents:
            # Create a separate task for each agent's review process
            task = self._get_agent_review(session_id, api_key, agent, ideas, brief)
            review_tasks.append(task)

        # Run all agent reviews concurrently
        try:
            results = await asyncio.gather(*review_tasks)
        except Exception as e:
            logger.error(f"Error during concurrent review gathering for session {session_id}: {e}", exc_info=True)
            raise ReviewEngineError(f"Failed to gather all agent reviews: {e}")

        # Process and structure the results
        all_reviews = {}
        for agent_type, idea_1_review, idea_2_review in results:
            all_reviews[agent_type] = {
                "idea_1_review": idea_1_review,
                "idea_2_review": idea_2_review,
            }

        logger.info(f"Successfully completed independent review phase for session {session_id}")
        return all_reviews

    async def _get_agent_review(
        self,
        session_id: UUID,
        api_key: str,
        agent: AgentModel,
        ideas: Tuple[IdeaSchema, IdeaSchema],
        brief: CreativeBrief
    ) -> Tuple[str, Dict[str, Any], Dict[str, Any]]:
        """
        Handles the complete review process for a single agent.
        """
        try:
            client = GeminiClient(api_key, agent.model_name)
            prompt = create_review_prompt(agent.guide_content, ideas, brief)

            raw_review_data = await client.generate_content(prompt)
            parsed_reviews = self._parse_review_response(raw_review_data)

            # Save reviews to the database
            review_1_db = await self._save_review(session_id, agent.id, ideas[0].id, parsed_reviews['idea_1_review'])
            review_2_db = await self._save_review(session_id, agent.id, ideas[1].id, parsed_reviews['idea_2_review'])

            return agent.agent_type, ReviewSchema.from_orm(review_1_db).dict(), ReviewSchema.from_orm(review_2_db).dict()

        except Exception as e:
            logger.error(f"Failed to get review from agent {agent.agent_type} for session {session_id}: {e}", exc_info=True)
            # In a real scenario, we might want to allow failures for non-critical agents
            # For now, any failure is critical.
            raise ReviewEngineError(f"Review from agent '{agent.agent_type}' failed: {e}")

    async def _save_review(self, session_id: UUID, agent_id: UUID, idea_id: UUID, review_data: Dict[str, Any]) -> Review:
        """Saves a single agent review to the database."""
        review_schema = ReviewCreate(
            session_id=session_id,
            agent_id=agent_id,
            idea_id=idea_id,
            **review_data
        )

        new_review = Review(**review_schema.dict())
        self.db.add(new_review)
        await self.db.commit()
        await self.db.refresh(new_review)
        return new_review

    def _parse_review_response(self, response: str) -> Dict[str, Any]:
        """
        Parses the structured JSON response from an agent's review.
        Assumes the LLM returns a JSON object with keys 'idea_1_review' and 'idea_2_review'.
        """
        try:
            if response.strip().startswith("```json"):
                response = response.strip()[7:-3].strip()

            data = json.loads(response)

            if 'idea_1_review' not in data or 'idea_2_review' not in data:
                raise KeyError("Response missing 'idea_1_review' or 'idea_2_review' keys.")

            # Further validation could be done here on the inner structure
            return data
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON from review response: {e}\nResponse was: {response}")
            raise ReviewEngineError(f"Invalid JSON format from review LLM: {e}")
        except KeyError as e:
            logger.error(f"Key error in review response: {e}\nResponse was: {response}")
            raise ReviewEngineError(f"Missing key in review LLM response: {e}")