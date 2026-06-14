import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.api.v1.validators import check_telegram_id_duplicate
from app.core.dependencies import SessionDep
from app.core.user import current_user, get_jwt_strategy
from app.models.user import User
from app.schemas.user import TelegramLinkByCodeRequest, TelegramLinkRequest

router = APIRouter()


@router.post("/link-code")
async def generate_telegram_link_code(
    session: SessionDep,
    user: User = Depends(current_user),
):
    code = secrets.token_urlsafe(8)

    user.telegram_link_code = code
    session.add(user)
    await session.commit()

    return {"telegram_link_code": code}


@router.post("/link")
async def link_telegram_by_code(
    data: TelegramLinkByCodeRequest,
    session: SessionDep,
):
    user = await session.scalar(
        select(User).where(User.telegram_link_code == data.code)
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid link code",
        )

    await check_telegram_id_duplicate(data.telegram_id, session)

    user.telegram_id = data.telegram_id
    user.telegram_link_code = None

    session.add(user)
    await session.commit()

    strategy = get_jwt_strategy()
    access_token = await strategy.write_token(user)

    return {
        "detail": "Telegram привязан",
        "email": user.email,
        "access_token": access_token,
    }


@router.post("/auth")
async def telegram_auth(
    data: TelegramLinkRequest,
    session: SessionDep,
):
    user = await session.scalar(
        select(User).where(User.telegram_id == data.telegram_id)
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Telegram account is not linked",
        )

    strategy = get_jwt_strategy()
    access_token = await strategy.write_token(user)

    return {
        "access_token": access_token,
        "email": user.email,
    }
