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
from app.models.agent import Agent
from app.schemas.agent import Agent as AgentSchema

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/{session_id}/agents", response_model=List[AgentSchema])
async def get_session_agents(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve all agents created for a specific session.
    """
    # First, verify the user has access to this session
    session = await db.get(Session, session_id)
    if not session or session.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    # If session is valid, retrieve the agents
    result = await db.execute(
        select(Agent).where(Agent.session_id == session_id)
    )
    agents = result.scalars().all()

    if not agents:
        logger.info(f"No agents found for session {session_id}, though the session exists.")
        # Return an empty list, as this is not an error condition.
        # Agents are created when the session is run.

    return agents