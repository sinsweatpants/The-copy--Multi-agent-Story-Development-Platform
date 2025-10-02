import logging
from typing import List, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.models.session import Session
from app.schemas.session import Session as SessionSchema, SessionCreate
from app.schemas.creative_brief import CreativeBrief, CreativeBriefCreate
from app.services.orchestrator import MasterOrchestratorService
from app.api.websocket import ConnectionManager # Assuming this is a singleton instance

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
websocket_manager = ConnectionManager()

@router.post("/", response_model=SessionSchema, status_code=status.HTTP_201_CREATED)
async def create_session(
    session_in: SessionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create a new session for the current user.
    """
    new_session = Session(
        user_id=current_user.id,
        api_key_id=session_in.api_key_id
    )
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    logger.info(f"New session created with id: {new_session.id} for user: {current_user.email}")
    return new_session

@router.get("/", response_model=List[SessionSchema])
async def get_user_sessions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> List[SessionSchema]:
    """
    Retrieve all sessions for the current user.
    """
    result = await db.execute(
        select(Session)
        .where(Session.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .order_by(Session.created_at.desc())
    )
    sessions = result.scalars().all()
    return sessions

@router.get("/{session_id}", response_model=SessionSchema)
async def get_session_details(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get details for a specific session.
    """
    session = await db.get(Session, session_id)
    if not session or session.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    return session

@router.post("/{session_id}/run", status_code=status.HTTP_202_ACCEPTED)
async def run_session_orchestration(
    session_id: UUID,
    brief_in: CreativeBrief,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Submit the creative brief and start the full orchestration cycle in the background.
    """
    session = await db.get(Session, session_id)
    if not session or session.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    if session.status != 'initialized':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Session has already been run or is currently running. Status: {session.status}")

    # Save the creative brief
    # This logic should ideally be in a service, but for simplicity, it's here.
    from app.models.creative_brief import CreativeBrief as CreativeBriefModel
    db_brief = CreativeBriefModel(**brief_in.dict(), session_id=session_id)
    db.add(db_brief)
    await db.commit()

    # Initialize the orchestrator and run it in the background
    orchestrator = MasterOrchestratorService(db, websocket_manager)
    background_tasks.add_task(orchestrator.run_full_cycle, session_id, brief_in)

    logger.info(f"Orchestration for session {session_id} has been started in the background.")
    return {"message": "Session orchestration has been successfully started."}