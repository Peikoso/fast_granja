from sqlalchemy import select
from fast_granja.database import get_session
from fast_granja.models import UserModel
from fast_granja.security import get_password_hash

async def admin_create():
    async for session in get_session():
        admin = await session.scalar(select(UserModel).where(UserModel.isAdmin == True))
        if not admin:
            new_admin = UserModel(
                username="admin",
                password=get_password_hash("admin123"),
                full_name="Admin User",
                email="admin@email.com",
                isAdmin=True
            )

            session.add(new_admin)
            await session.commit()
            print("Admin user created or already exists.")

