import logging
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.models.session import Session
from app.models.decision import FinalDecision
from app.schemas.decision import FinalDecision as FinalDecisionSchema

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/{session_id}/decision", response_model=FinalDecisionSchema)
async def get_session_decision(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve the final decision for a specific session.
    """
    # First, verify the user has access to this session
    session = await db.get(Session, session_id)
    if not session or session.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    # If session is valid, retrieve the final decision
    result = await db.execute(
        select(FinalDecision).where(FinalDecision.session_id == session_id)
    )
    decision = result.scalar_one_or_none()

    if not decision:
        logger.info(f"No final decision found for session {session_id}.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The final decision for this session has not been made yet.")

    return decision