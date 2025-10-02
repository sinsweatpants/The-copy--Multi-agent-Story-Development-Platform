import logging
from typing import List, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.models.session import Session
from app.models.idea import Idea
from app.schemas.idea import Idea as IdeaSchema

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/{session_id}/ideas", response_model=List[IdeaSchema])
async def get_session_ideas(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve the two competing ideas generated for a specific session.
    """
    # First, verify the user has access to this session
    session = await db.get(Session, session_id)
    if not session or session.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    # If session is valid, retrieve the ideas, ordered by their number
    result = await db.execute(
        select(Idea)
        .where(Idea.session_id == session_id)
        .order_by(Idea.idea_number)
    )
    ideas = result.scalars().all()

    if not ideas:
        logger.info(f"No ideas found for session {session_id}, though the session exists.")
        # This is expected if the orchestration hasn't reached this stage yet.

    return ideas