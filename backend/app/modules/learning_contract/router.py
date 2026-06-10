"""Learning Contract API router."""

from __future__ import annotations

from fastapi import APIRouter

from app.dependencies import CurrentUserId, DbSession
from app.modules.learning_contract.schemas import ContractResponse
from app.modules.learning_contract.services import create_contract, get_current_contract

router = APIRouter(prefix="/learning-contract", tags=["learning-contract"])


@router.get("/current", response_model=ContractResponse)
async def read_current_contract(user_id: CurrentUserId, db: DbSession):
    """Get current learning entry contract."""
    contract = await get_current_contract(db, user_id)
    return _contract_to_response(contract)


@router.post("/current", response_model=ContractResponse)
async def create_new_contract(user_id: CurrentUserId, db: DbSession):
    """Create a new learning entry contract."""
    contract = await create_contract(db, user_id)
    return _contract_to_response(contract)


def _contract_to_response(contract) -> ContractResponse:
    return ContractResponse(
        id=str(contract.id),
        target_language=contract.target_language,
        support_language=contract.support_language,
        lesson_duration_minutes=contract.lesson_duration_minutes,
        active_vocabulary_budget=contract.active_vocabulary_budget,
        grammar_focus_count=contract.grammar_focus_count,
        max_primary_corrections=contract.max_primary_corrections,
        scaffolding_mode=contract.scaffolding_mode,
        lesson_complexity=contract.lesson_complexity,
        diagnostic_profile_snapshot=contract.diagnostic_profile_snapshot,
        version=contract.version,
        status=contract.status,
        created_at=contract.created_at.isoformat(),
        updated_at=contract.updated_at.isoformat(),
    )
