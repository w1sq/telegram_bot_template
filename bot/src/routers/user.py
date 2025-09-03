import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from filters import IsUser
from db import UserRepository
from keyboards.user import get_main_menu_keyboard

router = Router(name="user_router")
router.message.filter(IsUser())


@router.message(Command("start"))
async def start_command(
    message: Message, user_repo: UserRepository, logger: logging.Logger
):
    if message.from_user:
        user = await user_repo.get(message.from_user.id)
    else:
        return

    if user:
        logger.info(f"User {user.id} accessed /start command")
        await message.answer(
            f"Добро пожаловать, {user.username}! Выберите, что хотите сделать:",
            reply_markup=get_main_menu_keyboard(),
        )
    else:
        logger.error(f"User {message.from_user.id} not found")
        await message.answer("Произошла ошибка, попробуйте позже")


@router.message()
async def handle_any_message(
    message: Message,
    user_repo: UserRepository,
    logger: logging.Logger,
):
    if message.from_user:
        user = await user_repo.get(message.from_user.id)
    else:
        return

    if user:
        logger.info(f"User {user.id} sent message outside FSM: {message.text}")
        await message.answer(
            "Выберите действие:", reply_markup=get_main_menu_keyboard()
        )
