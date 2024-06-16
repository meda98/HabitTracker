from model import Habit
from rich.console import Console
from rich.table import Table
from datetime import (
    datetime,
    timedelta
)
from analysis import (
    determine_streaks, 
    determine_completion
)
from database import (
    insert_habit, 
    get_habit_periodicity,
    get_habit_task_specification, 
    get_all_habit_names, 
    get_habit_names_daily, 
    get_habit_names_weekly, 
    get_dates_completed
)

def add_habit(habit_name, habit_task_specification, habit_periodicity, table_name = "habits"):
    """
    Adds a new habit to the specified table in the database.

    This function creates a new Habit object with the provided name, task specification, 
    and periodicity. It then inserts the habit into the specified table in the database.

    Parameters:
    - habit_name (str): The name of the habit.
    - habit_task_specification (str): The task specification of the habit.
    - habit_periodicity (str): The periodicity of the habit (e.g., daily, weekly).
    - table_name (str): The name of the table where the habit is stored. 
      Defaults to "habits".

    Returns:
    - None
    """
    habit = Habit (habit_name = habit_name, 
                   habit_task_specification = habit_task_specification, 
                   habit_periodicity = habit_periodicity)
    insert_habit(habit, table_name)


def create_last_completion_dates_list(habit_name, table_name = "habits"):
    """
    Creates a list of the most recent completion dates for a specified habit.

    This function retrieves the completion dates for the specified habit from the database 
    table and returns a list of the most recent completion dates as strings. If the habit 
    has been completed more than 10 times, only the last 10 completion dates are included. 
    If the habit has never been completed, a congratulatory message is printed.

    Parameters:
    - habit_name (str): The name of the habit.
    - table_name (str): The name of the table where the habit completion dates are stored. 
      Defaults to "habits".

    Returns:
    - habit_completion_dates_list (list of str): A list of the most recent completion dates 
      in 'YYYY-MM-DD' format.
    """
    habit_completion_dates = get_dates_completed(habit_name, table_name)
    
    habit_completion_dates_list = []
    
    if not habit_completion_dates:
        print("Congratulations! This is your first time completing this habit.")
    
    elif len(habit_completion_dates) > 10:
        for habit_completion_date in habit_completion_dates[-10:]:
            habit_completion_date_str = habit_completion_date.strftime("%Y-%m-%d")
            habit_completion_dates_list.append(habit_completion_date_str)
    
    else:
        for habit_completion_date in habit_completion_dates:
            habit_completion_date_str = habit_completion_date.strftime("%Y-%m-%d")
            habit_completion_dates_list.append(habit_completion_date_str)
    
    return habit_completion_dates_list


def create_list_of_available_completion_dates(habit_name, table_name = "habits"):
    """
    Creates a list of available completion dates for a habit over the past 14 days.

    This function generates a list of the last 14 days (in 'YYYY-MM-DD' format) and 
    filters out the dates on which the specified habit has already been completed. 
    It returns the remaining dates as available completion dates.

    Parameters:
    - habit_name (str): The name of the habit for which to create the list of available completion dates.
    - table_name (str): The name of the table where the habit completion dates are stored. 
      Defaults to "habits".

    Returns:
    - available_dates_list (list of str): A list of available completion dates (in 'YYYY-MM-DD' format) 
      over the past 14 days, excluding the dates when the habit was already completed.
    """
    today = datetime.today()
    last_14_days = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(14)]
    
    already_completed_dates = get_dates_completed(habit_name, table_name)
    already_completed_dates_str = [date.strftime("%Y-%m-%d") for date in already_completed_dates]
    available_dates_list = [date for date in last_14_days if date not in already_completed_dates_str]
    
    return available_dates_list


def create_overview_table(periodicity_choice, column_sorted_by, table_name = "habits"):
    """
    Creates an overview table of habits based on specified periodicity and sorting column.

    This function generates an overview table displaying habit data such as name, task specification, 
    periodicity, completion status, current streak, and longest streak. The table is sorted based 
    on the specified sorting column and filtered by the chosen periodicity.

    Parameters:
    - periodicity_choice (str): The choice of periodicity for filtering habits.
      Options: "all" (all habits), "daily" (daily habits), "weekly" (weekly habits).
    - column_sorted_by (str): The column by which to sort the table.
      Options: "Current Streak" (sort by current streak), "Longest Streak" (sort by longest streak).
    - table_name (str): The name of the table where habit data is stored. Defaults to "habits".

    Returns:
    - None: The overview table is displayed using rich console output.
    """
    # Initialize an empty list to store habit data
    habits_data = []

    # Retrieve habit names based on the specified periodicity choice
    if periodicity_choice == "all":
        habit_names = get_all_habit_names(table_name)
    elif periodicity_choice == "daily":
        habit_names = get_habit_names_daily(table_name)
    elif periodicity_choice == "weekly":
        habit_names = get_habit_names_weekly(table_name)
    
    # Iterate through each habit name
    for habit_name in habit_names:
        # Retrieve habit task specification
        habit_task_specification = get_habit_task_specification(habit_name, table_name)
        
        # Retrieve habit periodicity
        habit_periodicity = get_habit_periodicity(habit_name, table_name)
        
        # Determine whether habit is already completed or not
        habit_completed = determine_completion(habit_name, table_name)
        
        # Determine streaks for the habit
        streaks = determine_streaks(habit_name, table_name)
        habit_current_streak = str(streaks[0])
        habit_longest_streak = str(streaks[1])
        
        # Append habit data to the list
        habit_data = [habit_name, habit_task_specification, habit_periodicity, habit_completed, habit_current_streak, habit_longest_streak]
        habits_data.append(habit_data)
    
    # Determine the index of the column to sort by
    if column_sorted_by == "Current Streak":
        column = 4
    elif column_sorted_by == "Longest Streak":
        column = 5
    
    # Sort habit data based on the specified column
    habits_data = sorted(habits_data, key=lambda x: int(x[column]), reverse = True)

    # Initialize a table with headers
    table = Table(show_header=True, header_style="bold magenta")

    # Add columns to the table
    table.add_column("Habit")
    table.add_column("Task Specification")
    table.add_column("Periodicity")
    table.add_column("Completed")
    table.add_column("Current Streak")
    table.add_column("Longest Streak")

    # Iterate through habits data and add a row for each habit to the table
    for row in habits_data:
        table.add_row(*row)

    # Display the table using rich console
    console = Console()
    console.print(table)



