import bcrypt
import asyncio


async def get_hashed_password(password: str) -> str:
    byte_password = password.encode()
    salt = await asyncio.to_thread(bcrypt.gensalt)
    hashed_password = await asyncio.to_thread(bcrypt.hashpw, byte_password, salt)
    return hashed_password


async def check_hashed_password(hashed_password: str, check_password: bytes) -> bool:
    return await asyncio.to_thread(bcrypt.checkpw, check_password, hashed_password)
