from sqlalchemy import select
from typing import Optional
from .models import User
from .database import async_session  

async def create_user(user_id: int, bot_id: int, first_name: str, language: str, last_name: Optional[str] = None, username: Optional[str] = None) -> User:
    async with async_session() as session:
        user = User(user_id=user_id, bot_id=bot_id, first_name=first_name, last_name=last_name, username=username, language=language)
        session.add(user)
        await session.commit()
        return user

async def get_user(user_id: int, bot_id: int) -> Optional[User]:
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.user_id == user_id and User.bot_id == bot_id)
        )
        return result.scalar_one_or_none()