import logging
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.models.session import Session
from app.models.tournament import Tournament
from app.schemas.tournament import Tournament as TournamentSchema

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/{session_id}/tournament", response_model=TournamentSchema)
async def get_session_tournament(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve the tournament details for a specific session, including all turns.
    """
    # First, verify the user has access to this session
    session = await db.get(Session, session_id)
    if not session or session.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    # If session is valid, retrieve the tournament and its turns
    result = await db.execute(
        select(Tournament)
        .where(Tournament.session_id == session_id)
        .options(selectinload(Tournament.turns)) # Eagerly load the turns
    )
    tournament = result.scalar_one_or_none()

    if not tournament:
        logger.info(f"No tournament found for session {session_id}.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tournament for this session has not started yet.")

    return tournament