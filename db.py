import aiosqlite


async def create_table():
    async with aiosqlite.connect('data.db') as db:
        await db.execute("""
                    CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY,
                        name VARCHAR(120),
                        age INTEGER,
                        grade INTEGER,
                        math INTEGER,
                        physics INTEGER,
                        english INTEGER
                    )
                """)
        await db.commit()

async def get_all_students():
    async with aiosqlite.connect('data.db') as db:
        async with db.execute("SELECT * FROM students") as cursor:
            row = await cursor.fetchall()
            column = [cur[0] for cur in cursor.description]
    return row, column

async def add_student(name: str, age: int, grade: int, math: int, physics: int, english: int):
    async with aiosqlite.connect('data.db') as db:
        await db.execute(
                        """
                         INSERT INTO students (name, age, grade, math, physics, english)
                         VALUES (?, ?, ?, ?, ?, ?)
                        """, 
                        (name, age, grade, math, physics, english)
        )
        await db.commit()
    return "Student added successfully ✅"

async def delete_student(name: str):
    async with aiosqlite.connect('data.db') as db:
        async with db.execute("DELETE FROM students WHERE name = ?", (name,)) as cursor:            
            await db.commit()

            if cursor.rowcount == 0:
                return "Student not found 😕"
        
    return "Student deleted successfully ✅"

