from aiogram import Router

from .users import router as user_router

main_router = Router(name="main_router")
main_router.include_router(user_router)
