import pandas as pd
from pandas import DataFrame, Series
from db import get_all_students


def set_status(avg):
    # this method set status for each students
    if avg >= 85:
        return "excellent"
    elif avg >= 75:
        return "good"
    else:
        return "bad"

# the method converts tuple of the two lists to dataframe 
def make_dataframe(rows, columns) -> DataFrame:
    return pd.DataFrame(rows, columns=columns)

async def load_data() -> tuple[list, list]:
    # getting data from database as tuple of the two lists
    rows, columns = await get_all_students()
    return rows, columns

def add_status(df: DataFrame) -> DataFrame:
    # creating column "average_score" based on average score of three columns
    df['average_score'] = df[['math', 'physics', 'english']].mean(axis=1)

    # creating "status" column
    df['status'] = df['average_score'].apply(set_status)

    return df

# the method formats unreadable dataframe to readable text 
def format_stats(stats: DataFrame) -> str:
    lines = []

    for (grade, status), row in stats.iterrows():
        lines.append(
            f"📊 *Класс {grade} | Статус: {status}*\n"
            f"👥 Учеников: {int(row['number_of_students'])}\n"
            f"📈 Средний балл: {row['avg_points']}\n"
            f"📉 Мин / Макс: {row['min_points']} / {row['max_points']}\n"
            f"🧮 Математика: {row['math_avg']}\n"
            f"⚛️ Физика: {row['physics_avg']}\n"
            f"📘 Английский: {row['english_avg']}\n"
            f"{'─' * 25}"
        )
    
    return "\n".join(lines)

def format_statuses(series: Series, status: str) -> str:
    # the method returns names which their statuses equal to a choosen status
    if series.empty:
        return f"No students with status '{status}'"
    names = []
    for _, value in series.items():
        names.append(
            f"Status: {status}\n"
            f"Name: {value}\n"
            f"{'-'*25}"
        )
    
    return "\n".join(names)

# the method formats unreadable dataframe to readable text 
def format_top(top: DataFrame) -> str:
    # returns top n students in database based on average_score
    if isinstance(top, str):
        return top
    if top.empty:
        return "No students found"
    lines = []

    for _, row in top.iterrows():
        lines.append(
            f"name: {row['name']} | status: {row['status']}\n"
            f"age: {row['age']} | Grade: {row['grade']}\n"
            f"math score: {row['math']} | physics score: {row['physics']}\n"
            f"english score: {row['english']} | average score: {row['average_score']}\n"
            f"given status: {row['status']}\n"
            f"{'-' * 25}"

        )
    return "\n".join(lines)

def group_summary(df: DataFrame) -> DataFrame:
    # returns dataframe which is grouped by status and grade
    df = add_status(df)
    group = df.groupby(["grade", "status"]).agg(
        number_of_students = ('name', 'count'),
        avg_points = ('average_score', 'mean'),
        min_points = ('average_score', 'min'),
        max_points = ('average_score', 'max'),
        math_avg=('math', 'mean'),
        physics_avg=('physics', 'mean'),
        english_avg=('english', 'mean') 
    )
    return group

def top_students(df1: DataFrame, n: int) -> Series:
    # returns Series of names which are in top n students
    if df1.empty:
        return f"No students to get top {n}"
    
    if len(df1) < n:
        return "number is too big or too small, check your number of students"
    
    df = add_status(df1)
    return df.sort_values(ascending=False, by='average_score').head(n)

def students_by_status(df1: pd.DataFrame, status):
    # returns serial of name coloum which have a choosen status
    df1 = add_status(df1)
    filtered = df1[df1['status'] == status]
    return filtered['name']