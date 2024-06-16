import sqlite3
import datetime
from datetime import datetime
from model import Habit

# Connect to the SQLite database file 'habits.db'
conn = sqlite3.connect('habits.db')

# Create a cursor object to execute SQL commands
c = conn.cursor()

def create_table(table_name = "habits"):
  """
  Creates a table in the database for storing habits.

  This function creates a table with the specified name in the database to store 
  habit details if it does not already exist. The table includes columns for the 
  habit name, task specification, periodicity, date added, and date completed.

  Parameters:
  - table_name (str): The name of the table to be created. Defaults to "habits".

  Returns:
  None
  """
  c.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
            habit_name,
            habit_task_specification,
            habit_periodicity,
            date_added,
            date_completed
            )""")


def insert_habit(habit: Habit,table_name = "habits"):
  """
  Inserts a habit into the database.

  This function takes a Habit object as input and inserts its attributes into
  the specified table in the database.

  Parameters:
  - habit (Habit): An instance of the Habit class containing the habit details.
  - table_name (str): The name of the table where the habit will be inserted. 
    Defaults to "habits".

  Returns:
  None
  """
  with conn:
    c.execute(f'INSERT INTO {table_name} VALUES (:habit_name, :habit_task_specification, :habit_periodicity, :date_added, :date_completed)', 
              {'habit_name': habit.habit_name, 'habit_task_specification': habit.habit_task_specification, 'habit_periodicity':habit.habit_periodicity,
                'date_added': habit.date_added, 'date_completed': habit.date_completed})
      

def get_all_habit_names(table_name = "habits"):
  """
  Retrieves all unique habit names from the database.

  This function queries the specified table in the database to retrieve all 
  unique habit names. It returns a list of habit names.

  Parameters:
  - table_name (str): The name of the table from which to retrieve habit names. 
    Defaults to "habits".

  Returns:
  - all_habits (list of str): A list of unique habit names.
  """
  with conn:
    c.execute(f'SELECT DISTINCT habit_name FROM {table_name}')
    habits = c.fetchall()
    all_habits = []
    for habit in habits:
        all_habits.append(habit[0])
    return all_habits


def get_habit_names_daily(table_name = "habits"):
  """
  Retrieves all unique habit names with daily periodicity from the database.

  This function queries the specified table in the database to retrieve all 
  unique habit names that have a periodicity of 'daily'. It returns a list 
  of these habit names.

  Parameters:
  - table_name (str): The name of the table from which to retrieve habit names. 
    Defaults to "habits".

  Returns:
  - daily_habits (list of str): A list of unique habit names with daily periodicity.
  """
  with conn:
    c.execute(f'SELECT DISTINCT habit_name FROM {table_name} WHERE habit_periodicity = \'daily\'')
    habits = c.fetchall()
    daily_habits = []
    for habit in habits:
        daily_habits.append(habit[0])
    return daily_habits


def get_habit_names_weekly(table_name = "habits"):
  """
  Retrieves all unique habit names with weekly periodicity from the database.

  This function queries the specified table in the database to retrieve all 
  unique habit names that have a periodicity of 'weekly'. It returns a list 
  of these habit names.

  Parameters:
  - table_name (str): The name of the table from which to retrieve habit names. 
    Defaults to "habits".

  Returns:
  - weekly_habits (list of str): A list of unique habit names with weekly periodicity.
  """
  with conn:
    c.execute(f'SELECT DISTINCT habit_name FROM {table_name} WHERE habit_periodicity = \'weekly\'')
    habits = c.fetchall()
    weekly_habits = []
    for habit in habits:
        weekly_habits.append(habit[0])
    return weekly_habits


def complete_habit(habit_name, date_completed, table_name = "habits"):
  """
  Marks a habit as completed by updating the date completed.

  This function inserts a new entry into the specified table in the database 
  with the provided completion date for the habit. It selects the habit based on its name
  and creates a duplicate of the habit's first entry, where date_completed equals NULL.
  Instead of NULL, the completion date is provided as input for the new entry.

  Parameters:
  - habit_name (str): The name of the habit to be marked as completed.
  - date_completed (str): The date when the habit was completed, in the format 'YYYY-MM-DD'.
  - table_name (str): The name of the table where the habit is stored. 
    Defaults to "habits".

  Returns:
  None
  """
  with conn:
    c.execute(f"""INSERT INTO {table_name} (
            habit_name,
            habit_task_specification,
            habit_periodicity,
            date_added,
            date_completed
            )
            SELECT
            habit_name,
            habit_task_specification,
            habit_periodicity,
            date_added,
            ? as date_completed
            FROM {table_name}
            WHERE
            habit_name = ? AND date_completed IS NULL""", (date_completed, habit_name))


def get_dates_completed(habit_name, table_name = "habits"):
  """
  Retrieves and sorts the completion dates of a habit.

  This function queries the specified table in the database to retrieve all 
  completion dates for a given habit name where the completion date is not NULL. 
  It converts these dates to datetime objects, sorts them in ascending order 
  based on the ISO calendar week, and returns the sorted list.

  Parameters:
  - habit_name (str): The name of the habit for which to retrieve completion dates.
  - table_name (str): The name of the table from which to retrieve the completion dates. 
    Defaults to "habits".

  Returns:
  - all_dates_completed_sorted (list of datetime): A list of completion dates 
    sorted in ascending order based on the ISO calendar week.
  """
  with conn:
    c.execute(f'SELECT date_completed FROM {table_name} WHERE habit_name = ? AND date_completed IS NOT NULL', (habit_name,))
    dates_completed = c.fetchall()
    all_dates_completed = []
    for date_completed in dates_completed:
        all_dates_completed.append(date_completed[0])
    # Convert strings to datetime objects to facilitate sorting
    all_dates_completed = [datetime.strptime(date_completed, "%Y-%m-%d") for date_completed in all_dates_completed]
    # Sort the completion dates in ascending order based on the ISO calendar week
    all_dates_completed_sorted = sorted(all_dates_completed, key = lambda x: x.isocalendar())
    return all_dates_completed_sorted


def get_habit_periodicity(habit_name, table_name = "habits"):
  """
  Retrieves the periodicity of a habit.

  This function queries the specified table in the database to retrieve the 
  periodicity of a given habit name where the completion date is NULL. 
  It returns the periodicity as a string.

  Parameters:
  - habit_name (str): The name of the habit for which to retrieve the periodicity.
  - table_name (str): The name of the table from which to retrieve the periodicity. 
    Defaults to "habits".

  Returns:
  - habit_periodicity (str): The periodicity of the habit (e.g., 'daily' or 'weekly').
  """
  with conn:
    c.execute(f'SELECT habit_periodicity FROM {table_name} WHERE habit_name = ? AND date_completed IS NULL', (habit_name,))
    habit_periodicity = c.fetchall()
    return habit_periodicity[0][0]


def get_habit_task_specification(habit_name, table_name = "habits"):
  """
  Retrieves the task specification of a habit.

  This function queries the specified table in the database to retrieve the 
  task specification of a given habit name where the completion date is NULL. 
  It returns the task specification as a string.

  Parameters:
  - habit_name (str): The name of the habit for which to retrieve the task specification.
  - table_name (str): The name of the table from which to retrieve the task specification. 
    Defaults to "habits".

  Returns:
  - habit_task_specification (str): The task specification of the habit.
  """
  with conn:
    c.execute(f'SELECT habit_task_specification FROM {table_name} WHERE habit_name = ? AND date_completed IS NULL', (habit_name,))
    habit_task_specification = c.fetchall()
    return habit_task_specification[0][0]


def delete_habit_data(habit_name, table_name = "habits"):
  """
  Deletes a habit and its associated data from the database.

  This function deletes all entries of a given habit name from the specified 
  table in the database.

  Parameters:
  - habit_name (str): The name of the habit to be deleted.
  - table_name (str): The name of the table from which to delete the habit data. 
    Defaults to "habits".

  Returns:
  None
  """
  with conn:
    c.execute(f'DELETE FROM {table_name} WHERE habit_name = ?', (habit_name,))


def delete_habit_completion_date(habit_name, habit_completion_date, table_name = "habits"):
  """
  Deletes a specific completion date of a habit from the database.

  This function deletes an entry with a specific completion date for a given 
  habit name from the specified table in the database.

  Parameters:
  - habit_name (str): The name of the habit for which to delete the completion date.
  - habit_completion_date (str): The completion date to be deleted, in the format 'YYYY-MM-DD'.
  - table_name (str): The name of the table from which to delete the habit completion date. 
    Defaults to "habits".

  Returns:
  None
  """
  with conn:
      c.execute(f'DELETE FROM {table_name} WHERE habit_name = ? AND date_completed = ?', (habit_name, habit_completion_date))