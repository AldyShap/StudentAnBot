import asyncio

from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from config import BOT_TOKEN
import analytics as an


bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def psh_start(message: Message):
    text = """
    /stats → общая статистика по всем группам
    /top <n> → топ n учеников
    /status <status> → ученики с этим статусом
    /export → отправить CSV в чат
    """
    await message.answer("Hello I am the bot who analyzes the csv file!")
    await message.answer(text)

@dp.message(Command('top'))
async def get_help(message: Message, command: CommandObject):
    n = command.args

    if not n:
        await message.answer("использование /top <кол.учеников>")
        return
    df = an.load_data('data.csv')
    try:
        df = an.top_students(df, int(n))
        text = an.format_top(df)
        await message.answer(text)
    except ValueError as e:
        await message.answer(f'Oops.. something went wrong... Try again, {e}')

@dp.message(Command('status'))
async def get_stats(message: Message, command: CommandObject):

    status_text = command.args

    if not status_text or status_text not in ['good', 'bad', 'excellent']:
        await message.answer("Использование: /status <ваш статус>")
        await message.answer("Statuses: ['good', 'bad', 'excellent']")
        return

    # Дальше ваша логика
    df = an.load_data('data.csv')
    series = an.students_by_status(df, status_text)
    print(series)
    try:
        text = an.format_statuses(series, status_text)
        print(df.to_string)
        await message.answer(text)
    except Exception as e:
        await message.answer(f'oops... something went wrong, try again! {e}')

@dp.message(Command('stats'))
async def cmd_stats(message: Message):
    df = an.load_data('data.csv')
    stats = an.group_summary(df)
    text = an.format_stats(stats)
    try:
        await message.answer(text)
    except Exception as e:
        print(e)
        await message.answer(f'oops... something went wrong, try again! {e}')
    
@dp.message(Command('export'))
async def cmd_export(message: Message):
    df = an.load_data('data.csv')
    export_csv = an.group_summary(df)
    export_csv.to_csv('export.csv')
    try:
        await message.reply_document(document=types.FSInputFile(path='export.csv'))
    except Exception as e:
        await message.answer(f'oops... something went wrong, try again! {e}')



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit :)")
