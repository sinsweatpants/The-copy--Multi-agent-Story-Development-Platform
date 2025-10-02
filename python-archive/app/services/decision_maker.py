import logging
import json
from typing import Dict, Any, List
from uuid import UUID
from collections import Counter

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.decision import FinalDecision
from app.schemas.decision import FinalDecision as FinalDecisionSchema, FinalDecisionCreate
from app.schemas.tournament import Tournament as TournamentSchema
from app.integrations.gemini.client import GeminiClient
from app.integrations.gemini.prompts import create_final_decision_prompt
from app.utils.exceptions import DecisionMakerError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DecisionMakerService:
    """
    Service responsible for analyzing the tournament, conducting a final vote,
    and generating the final decision report.
    """

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def make_final_decision(
        self,
        session_id: UUID,
        api_key: str,
        tournament_result: TournamentSchema,
        # We'll need more context, like the original ideas and reviews, for a full implementation.
        # For now, we'll focus on what the tournament schema provides.
    ) -> FinalDecisionSchema:
        """
        Orchestrates the final decision-making process.

        Args:
            session_id: The UUID of the current session.
            api_key: The user's Gemini API key.
            tournament_result: The completed tournament data.

        Returns:
            The final decision Pydantic schema.

        Raises:
            DecisionMakerError: If the final decision process fails.
        """
        try:
            logger.info(f"Starting final decision process for session {session_id}")

            # 1. Analyze tournament arguments and conduct a "vote"
            vote_breakdown = self._analyze_votes(tournament_result.turns)

            # 2. Determine the winning idea
            if not vote_breakdown:
                raise DecisionMakerError("No votes were cast during the tournament.")

            winning_idea_number = vote_breakdown.most_common(1)[0][0]
            winning_idea_id, losing_idea_id = self._get_idea_ids_from_tournament(tournament_result, winning_idea_number)

            # 3. Generate the final report using a Gemini call
            # This is a simplified call; a real one would need more context.
            client = GeminiClient(api_key, "gemini-2.5-pro") # Use a powerful model for the final report
            prompt = create_final_decision_prompt(
                tournament_turns=tournament_result.turns,
                # These are simplified for this implementation
                agent_reviews={},
                winning_idea=None
            )
            report_raw = await client.generate_content(prompt)
            report_data = self._parse_report_response(report_raw)

            # 4. Save the final decision to the database
            decision = await self._save_decision(
                session_id=session_id,
                tournament_id=tournament_result.id,
                winning_idea_id=winning_idea_id,
                losing_idea_id=losing_idea_id,
                vote_breakdown=dict(vote_breakdown),
                report_data=report_data
            )

            logger.info(f"Final decision made for session {session_id}. Winning idea: {winning_idea_number}")
            return FinalDecisionSchema.from_orm(decision)

        except Exception as e:
            logger.error(f"Failed to make final decision for session {session_id}: {e}", exc_info=True)
            raise DecisionMakerError(f"Decision-making failed: {e}")

    def _analyze_votes(self, turns: List[Any]) -> Counter:
        """Analyzes the arguments in each turn to tally up support for each idea."""
        votes = Counter()
        for turn in turns:
            for argument in turn.arguments:
                votes[argument.supporting_idea] += 1
        return votes

    def _get_idea_ids_from_tournament(self, tournament: TournamentSchema, winning_idea_number: int) -> tuple[UUID, UUID]:
        """
        Placeholder function to extract idea IDs. In a real scenario, this info
        would be passed down or queried.
        """
        # This is a major assumption and needs a proper implementation
        # where ideas are linked to the tournament or session context.
        # We'll use placeholder UUIDs for now.
        from uuid import uuid4
        idea_1_id = uuid4()
        idea_2_id = uuid4()

        if winning_idea_number == 1:
            return idea_1_id, idea_2_id
        else:
            return idea_2_id, idea_1_id

    async def _save_decision(
        self,
        session_id: UUID,
        tournament_id: UUID,
        winning_idea_id: UUID,
        losing_idea_id: UUID,
        vote_breakdown: Dict[str, int],
        report_data: Dict[str, Any]
    ) -> FinalDecision:
        """Saves the final decision to the database."""

        total_votes = sum(vote_breakdown.values())
        winning_votes = max(vote_breakdown.values())

        decision_create = FinalDecisionCreate(
            session_id=session_id,
            tournament_id=tournament_id,
            winning_idea_id=winning_idea_id,
            losing_idea_id=losing_idea_id,
            decision_rationale=report_data.get("decision_rationale", "No rationale provided."),
            key_strengths=report_data.get("key_strengths", []),
            addressed_weaknesses=report_data.get("addressed_weaknesses", []),
            vote_breakdown=vote_breakdown,
            unanimous=(winning_votes == total_votes and total_votes > 0),
            confidence_score=float(winning_votes) / total_votes if total_votes > 0 else 0.0,
            implementation_recommendations=report_data.get("implementation_recommendations", []),
            next_steps=report_data.get("next_steps", [])
        )

        new_decision = FinalDecision(**decision_create.dict())
        self.db.add(new_decision)
        await self.db.commit()
        await self.db.refresh(new_decision)
        return new_decision

    def _parse_report_response(self, response: str) -> Dict[str, Any]:
        """Parses the JSON response for the final report."""
        try:
            if response.strip().startswith("```json"):
                response = response.strip()[7:-3].strip()
            return json.loads(response)
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Failed to parse final report: {e}\nResponse: {response}")
            raise DecisionMakerError(f"Could not parse final report from LLM: {e}")