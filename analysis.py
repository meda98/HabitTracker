import datetime
from database import (
    get_dates_completed, 
    get_habit_periodicity
)

def determine_completion(habit_name, table_name = "habits"):
    """
    Determines if a habit has been completed for the current day or week.

    This function checks if a given habit has been completed based on its periodicity 
    (daily or weekly). It retrieves the completion dates and periodicity from the 
    specified table in the database and compares the current date with the most recent 
    completion date.

    Parameters:
    - habit_name (str): The name of the habit to check for completion.
    - table_name (str): The name of the table from which to retrieve the habit data. 
      Defaults to "habits".

    Returns:
    - habit_completed (str): 'Yes' if the habit is completed for the current day 
      or week, 'No' otherwise.
    """
    # Get today's date
    today = datetime.datetime.now()

    # Retrieve a sorted list of completion dates for the habit
    all_dates_completed_sorted = get_dates_completed(habit_name, table_name)

    # Get the periodicity of the habit
    habit_periodicity = get_habit_periodicity(habit_name, table_name)

    # By default, assume the habit is completed
    habit_completed = str('Yes')

    # If there are no completion dates, the habit is not completed
    if not all_dates_completed_sorted:
        habit_completed = str('No')
    # Check completion based on habit periodicity
    elif habit_periodicity == "daily" and (today - all_dates_completed_sorted[-1]).days != 0:
        # If last completion date is not today for daily habits, habit is not completed
        habit_completed = str('No')
    # For weekly habits, compare current week and year with the last completion week and year
    elif habit_periodicity == "weekly":
        today_week              = today.isocalendar()[1]
        last_completion_week    = all_dates_completed_sorted[-1].isocalendar()[1]
        today_year              = today.isocalendar()[0]
        last_completion_year    = all_dates_completed_sorted[-1].isocalendar()[0]
        
        # If weeks and years are different, habit is not completed
        if (today_year - last_completion_year) * 52 + today_week - last_completion_week != 0:

            habit_completed = str('No')

    # return 'Yes' or 'No'
    return habit_completed


def determine_streaks(habit_name, table_name = "habits"):
    """
    Determines the current and longest streaks for a given habit.

    This function calculates the streaks for a specified habit based on its 
    periodicity (daily or weekly) and its completion dates. A streak is defined 
    as consecutive days or weeks in which the habit was completed. The function 
    returns the current streak and the longest streak of the habit.

    Parameters:
    - habit_name (str): The name of the habit to determine streaks for.
    - table_name (str): The name of the table from which to retrieve the habit data. 
      Defaults to "habits".

    Returns:
    - (int, int): A tuple containing:
      - current_streak (int): The number of consecutive days or weeks the habit 
        has been completed up to today.
      - longest_streak (int): The longest number of consecutive days or weeks the 
        habit has been completed.
    """
    # Get a sorted list of completion dates for the habit
    all_dates_completed_sorted = get_dates_completed(habit_name, table_name)

    # Get the periodicity of the habit
    habit_periodicity = get_habit_periodicity(habit_name, table_name)

    # If there are no completion dates, return 0 streaks
    if not all_dates_completed_sorted:
        return (0, 0)

    # Initialize streak counters
    streak = 1
    longest_streak = 1

    # Iterate over completion dates to determine streaks
    for i in range(1, len(all_dates_completed_sorted)):
        is_streak = False  # Initialize is_streak to False for each iteration
        
        if habit_periodicity == "daily":
            # If the difference of two successive dates is equal to one, a streak is determined
            is_streak = (all_dates_completed_sorted[i] - all_dates_completed_sorted[i-1]).days == 1
        elif habit_periodicity == "weekly":
            last_completion_week    = all_dates_completed_sorted[i-1].isocalendar()[1]
            current_completion_week = all_dates_completed_sorted[i].isocalendar()[1]
            
            last_completion_year    = all_dates_completed_sorted[i-1].isocalendar()[0]
            current_completion_year = all_dates_completed_sorted[i].isocalendar()[0]

            # Calculate the week difference, accounting for year difference
            week_difference = (current_completion_year - last_completion_year) * 52 + (current_completion_week - last_completion_week)

            # If a weekly habit is completed more than once in a week, the duplicate week number(s) will be skipped
            if week_difference == 0:
                continue
            # If the difference of two successive weeks is equal to one, a streak is determined
            # Taking into account the difference in years
            elif week_difference == 1:
                is_streak = True
        
        # Update streak count based on whether there's a streak or not
        if is_streak:
            streak += 1
        else:
            streak = 1

        # Update longest streak
        # If streak is higher than longest_streak, longest_streak will be set to the value of streak
        longest_streak = max(streak, longest_streak)

    # Set a default value for current_streak
    current_streak = streak

    # Get today's date
    today = datetime.datetime.now()

    # Update current streak
    # Check if the streak is broken based on habit periodicity
    if habit_periodicity == "daily" and (today - all_dates_completed_sorted[-1]).days > 1:
        # If the difference is bigger than one, the current streak is set back to zero
        current_streak = 0
    elif habit_periodicity == "weekly":
        # Get today's week and year
        today_week              = today.isocalendar()[1]
        last_completion_week    = all_dates_completed_sorted[-1].isocalendar()[1]
        
        # Get the week and year of the last completion date
        today_year              = today.isocalendar()[0]
        last_completion_year    = all_dates_completed_sorted[-1].isocalendar()[0]

        # Calculate the difference in weeks between today and the last completion date
        # Taking into account the difference in years
        if (today_year - last_completion_year) * 52 + today_week - last_completion_week > 1:
            # If the difference is bigger than one, the current streak is set back to zero
            current_streak = 0

    # Return the current streak and longest streak
    return current_streak, longest_streak

    
    

    
