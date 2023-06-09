from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message
import services.services
import services.stat_game
from keyboards.keyboards import game_kb, yes_no_kb
from lexicon.lexicon_ru import LEXICON_RU
from services.services import get_bot_choice, get_winner


router: Router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup=yes_no_kb)
    if message.from_user.id not in services.stat_game.users:
        services.stat_game.users[message.from_user.id] = {
                                       'total_games': 0,
                                       'bot_wins': 0,
                                       'user_wins': 0}


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'], reply_markup=yes_no_kb)


# Этот хэндлер срабатывает на согласие пользователя играть в игру
@router.message(Text(text=LEXICON_RU['yes_button']))
async def process_yes_answer(message: Message):
    await message.answer(text=LEXICON_RU['yes'], reply_markup=game_kb)


# Этот хэндлер срабатывает на отказ пользователя играть в игру
@router.message(Text(text=LEXICON_RU['no_button']))
async def process_no_answer(message: Message):
    await message.answer(text=LEXICON_RU['no'])

# Этот хэндлер срабатывает на статистику
@router.message(Text(text=LEXICON_RU['stat_button']))
async def process_stat(message: Message):
    await message.answer(f"Сыграно игр - {services.stat_game.users[message.from_user.id]['total_games']}. "
                         f"Счёт {services.stat_game.users[message.from_user.id]['user_wins']} "
                         f": {services.stat_game.users[message.from_user.id]['bot_wins']}", reply_markup=yes_no_kb)


# Этот хэндлер срабатывает на любую из игровых кнопок
@router.message(Text(text=[LEXICON_RU['rock'],
                           LEXICON_RU['paper'],
                           LEXICON_RU['scissors'],
                           LEXICON_RU['lizard'],
                           LEXICON_RU['spoke']
                           ]))

async def process_game_button(message: Message):
    bot_choice = get_bot_choice()
    await message.answer(text=f'{LEXICON_RU["bot_choice"]} '
                              f'- {LEXICON_RU[bot_choice]}')
    winner = get_winner(message.text, bot_choice)
    if winner == 'user_won':
        services.stat_game.users[message.from_user.id]['user_wins'] +=1
    elif winner == 'bot_won':
        services.stat_game.users[message.from_user.id]['bot_wins'] +=1
    services.stat_game.users[message.from_user.id]['total_games'] +=1
    await message.answer(text=LEXICON_RU[winner], reply_markup=yes_no_kb)