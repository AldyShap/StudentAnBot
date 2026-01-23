import pandas as pd
from pandas import DataFrame, Series


def set_status(avg):
    # this method set status for each students
    if avg >= 85:
        return "excellent"
    elif avg >= 75:
        return "good"
    else:
        return "bad"

def load_data(file_path):
    # loading csv file with this method
    df = pd.read_csv(file_path)
    return df

def add_status(df: DataFrame) -> DataFrame:
    # creating column "average_score" based on average score of three columns
    df['average_score'] = df[['math', 'physics', 'english']].mean(axis=1)

    # creating "status" column
    df['status'] = df['average_score'].apply(set_status)

    return df

def format_stats(stats: DataFrame) -> str:
    lines = []

    for (grade, status), row in stats.iterrows():
        lines.append(
            f"📊 *Класс {grade} | Статус: {status}*\n"
            f"👥 Учеников: {int(row['number_of_students'])}\n"
            f"📈 Средний балл: {row['avg_points']:.1f}\n"
            f"📉 Мин / Макс: {row['min_points']} / {row['max_points']}\n"
            f"🧮 Математика: {row['math_avg']:.1f}\n"
            f"⚛️ Физика: {row['physics_avg']:.1f}\n"
            f"📘 Английский: {row['english_avg']:.1f}\n"
            f"{'─' * 25}"
        )
    
    return "\n".join(lines)

def format_statuses(series: Series, status: str) -> str:
    # the method returns names which their statuses equal to a choosen status
    names = []
    for _, value in series.items():
        names.append(
            f"Status: {status}\n"
            f"Name: {value}\n"
            f"{'-'*25}"
        )
    
    return "\n".join(names)

def format_top(top: int) -> str:
    # returns top n students in csv based on average_score
    if len(top)> 8:
        return "There is only 8 students, choose less number :)"
    lines = []

    for _, row in top.iterrows():
        lines.append(
            f"name: {row['name']} | status: {row['status']}\n"
            f"age: {row["age"]:.1f} | Grade: {row['grade']:.1f}\n"
            f"math score: {row['math']:.1f} | physics score: {row['physics']:.1f}\n"
            f"english score: {row['english']:.1f} | average score: {row['average_score']:.1f}\n"
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
    if len(df1) < n:
        return "please, enter the correct number"
    df = add_status(df1)
    return df.sort_values(ascending=False, by='average_score').head(n)

def students_by_status(df1: pd.DataFrame, status):
    # returns serial of name coloum which have a choosen status
    df1 = add_status(df1)
    df = df1[df1['status'] == status]
    return df['name']