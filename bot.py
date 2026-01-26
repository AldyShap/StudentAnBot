import asyncio

from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from config import BOT_TOKEN # your bot's token
import analytics as an
import db

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


# -------------------- START --------------------
@dp.message(CommandStart())
async def psh_start(message: Message):
    text = """
    Что я умею делать: 
    /start → главное меню
    /stats → общая статистика по всем группам
    /top <n> → топ n учеников
    /status <status> → ученики с этим статусом
    /export → отправить CSV в чат
    /add_student <name age grade math physics english> → добавить ученика к базе
    /delete_student <name> → удалить ученика в базе
    """
    await message.answer("Привет 👋\nЯ бот для работы с учениками.")
    await message.answer(text)

# -------------------- TOP <N> students --------------------
@dp.message(Command('top'))
async def get_help(message: Message, command: CommandObject):
    n = command.args

    if not n:
        await message.answer("использование /top <кол.учеников>")
        return
    rows, columns = await an.load_data()
    if not rows:
        await message.answer("📭 База данных пуста.")
        return
    try:
        df = an.make_dataframe(rows, columns)
        df = an.top_students(df, int(n))
        text = an.format_top(df)
        await message.answer(text)
    except ValueError as e:
        await message.answer(f'Oops.. something went wrong... Try again, {e}')

# -------------------- STUDENTS BY STATUS --------------------
@dp.message(Command('status'))
async def get_stats(message: Message, command: CommandObject):

    status_text = command.args

    if not status_text or status_text not in ['good', 'bad', 'excellent']:
        await message.answer("Использование: /status <ваш статус>")
        await message.answer("Statuses: ['good', 'bad', 'excellent']")
        return

    rows, columns = await an.load_data()
    if not rows:
        await message.answer("📭 База данных пуста.")
        return
    
    df = an.make_dataframe(rows, columns)

    series = an.students_by_status(df, status_text)
    try:
        text = an.format_statuses(series, status_text)
        await message.answer(text)
    except Exception as e:
        await message.answer(f'oops... something went wrong, try again! {e}')

# -------------------- STATISTICS OF THE STUDENTS --------------------
@dp.message(Command('stats'))
async def cmd_stats(message: Message):
    rows, columns = await an.load_data()
    if not rows:
        await message.answer("📭 База данных пуста.")
        return
    df = an.make_dataframe(rows, columns)
    stats = an.group_summary(df)
    text = an.format_stats(stats)
    try:
        await message.answer(text)
    except Exception as e:
        await message.answer(f'oops... something went wrong, try again! {e}')
    
# -------------------- EXPORT INFORMATION ABOUT STUDENTS TO CSV FILE --------------------
@dp.message(Command('export'))
async def cmd_export(message: Message):
    rows, columns = await an.load_data()
    if not rows:
        await message.answer("📭 База данных пуста.")
        return
    
    df = an.make_dataframe(rows, columns)

    export_csv = an.group_summary(df)
    export_csv.to_csv('export.csv')
    try:
        await message.reply_document(document=types.FSInputFile(path='export.csv'))
    except Exception as e:
        await message.answer(f'oops... something went wrong, try again! {e}')

# -------------------- ADD A STUDENT --------------------
@dp.message(Command('add_student'))
async def add_someone(message: Message, command: CommandObject):
    student = command.args
    if not student:
        await message.answer("Использование: /add_student <name age grade math physics english>")
        return
    student_info = student.split(' ')
    if len(student_info) < 6 or len(student_info) > 6:
        await message.answer("Недостаточо или имеется лишняя информация об ученике, попробуйте снова.")
    
    
    name = student_info[0]
    try:
        age, grade, math, physics, english = map(int, student_info[1:])
    except ValueError:
        await message.answer("Прошу вас дать правильную информацию о студенте соответсвуйщим образом")
        await message.answer("Использование: /add_student <name age grade math physics english>")
        return
    
    ans = await db.add_student(
        name=name,
        age=age,
        grade=grade,
        math=math,
        physics=physics,
        english=english
    )

    await message.answer(ans)
# -------------------- DELETE A STUDENT --------------------
@dp.message(Command('delete_student'))
async def add_someone(message: Message, command: CommandObject):
    student = command.args
    if not student:
        await message.answer("Использование: /delete_student <name>")
        return
    
    ans = await db.delete_student(name = student)

    await message.answer(ans)

@dp.message()
async def echo(message: Message):
    await message.answer("Извините, но я не знаю эту команду")
    text = """
    Но я умею делать: 
    /start → главное меню
    /stats → общая статистика по всем группам
    /top <n> → топ n учеников
    /status <status> → ученики с этим статусом
    /export → отправить CSV в чат
    /add_student <name age grade math physics english> → добавить ученика к базе
    /delete_student <name> → удалить ученика в базе
    """
    await message.answer(text)

async def main():
    await db.create_table()
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit :)")
