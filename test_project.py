import pytest
import sqlite3
from model import Habit
from freezegun import freeze_time
from database import (
    create_table,
    insert_habit,
    get_all_habit_names,
    get_habit_names_daily,
    get_habit_names_weekly,
    complete_habit,
    get_dates_completed,
    get_habit_periodicity,
    get_habit_task_specification,
    delete_habit_data,
    delete_habit_completion_date
)
from analysis import(
    determine_completion,
    determine_streaks
)
from functionality import(
    add_habit,
    create_last_completion_dates_list,
    create_list_of_available_completion_dates,
    create_overview_table
)

# naming the test table
table_name = "test_habits"

# Fixture to create the table before the test runs
@pytest.fixture
def setup_habit_data():
    create_table(table_name)
    
    habits = [
        ("Cook", "I want to cook dinner.", "daily"),
        ("Read", "I want to read 30 minutes.", "daily"),
        ("Go to bed early", "I want to go to bed before 10pm.", "daily"),
        ("Meet a friend", "I want to meet with a friend in town.", "weekly"),
        ("Run", "I want to run 10km.", "weekly")
    ]
    
    for name, description, periodicity in habits:
        habit = Habit(name, description, periodicity)
        insert_habit(habit, table_name)

    # Dictionary mapping habits to lists of completion dates
    habit_completions = {
        "Cook":             ["2024-04-01", "2024-04-02", "2024-04-03", "2024-04-04", "2024-04-05", "2024-04-08", "2024-04-09",
                             "2024-04-10", "2024-04-12", "2024-04-13", "2024-04-14", "2024-04-15", "2024-04-16", "2024-04-17",
                             "2024-04-18", "2024-04-19", "2024-04-20", "2024-04-21", "2024-04-22", "2024-04-23", "2024-04-24", 
                             "2024-04-27", "2024-04-28"],
        "Read":             ["2024-04-01", "2024-04-02", "2024-04-05", "2024-04-06", "2024-04-07", "2024-04-08", "2024-04-09",
                             "2024-04-10", "2024-04-11", "2024-04-12", "2024-04-13", "2024-04-14", "2024-04-15", "2024-04-16",
                             "2024-04-18", "2024-04-19", "2024-04-20", "2024-04-21", "2024-04-22", "2024-04-23", "2024-04-24", 
                             "2024-04-26"],
        "Go to bed early":  ["2024-04-03", "2024-04-04", "2024-04-05", "2024-04-06", "2024-04-07", "2024-04-08", "2024-04-09",
                             "2024-04-11", "2024-04-12", "2024-04-17", "2024-04-18", "2024-04-19", "2024-04-20", "2024-04-21",
                             "2024-04-22", "2024-04-23", "2024-04-24", "2024-04-25", "2024-04-26", "2024-04-27"],
        "Meet a friend":    ["2024-04-02", "2024-04-12", "2024-04-15", "2024-04-26"],
        "Run":              ["2024-04-04", "2024-04-12"]
    }

    # Complete each habit for each date
    for habit_name, dates in habit_completions.items():
        for date_completed in dates:
            complete_habit(habit_name, date_completed, table_name)

    # This allows the test to run
    yield
    
    # Teardown: Drop the table after the test has finished
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()
    c.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.commit()
    conn.close()

def test_inserted_habit_data(setup_habit_data):
    habits = get_all_habit_names(table_name)
    assert len(habits) == 5

    habits_daily = get_habit_names_daily(table_name)
    assert len(habits_daily) == 3

    habits_weekly = get_habit_names_weekly(table_name)
    assert len(habits_weekly) == 2

@pytest.mark.parametrize("habit_name, expected_entries", [
    ("Cook", 23),
    ("Run", 2)
])
def test_inserted_completion_dates(setup_habit_data, habit_name, expected_entries):
    entries = get_dates_completed(habit_name, table_name)
    assert len(entries) == expected_entries

@pytest.mark.parametrize("habit_name, expected_periodicity", [
    ("Cook", "daily"),
    ("Read", "daily"),
    ("Meet a friend","weekly")
])
def test_get_habit_periodicity(setup_habit_data, habit_name, expected_periodicity):
    periodicity = get_habit_periodicity(habit_name, table_name)
    assert periodicity == expected_periodicity

@pytest.mark.parametrize("habit_name, expected_task_specification", [
    ("Cook", "I want to cook dinner."),
    ("Meet a friend","I want to meet with a friend in town.")
])
def test_get_habit_task_specification(setup_habit_data, habit_name, expected_task_specification):
    task_specification = get_habit_task_specification(habit_name, table_name)
    assert task_specification == expected_task_specification

def test_deleted_habit(setup_habit_data):
    delete_habit_data("Cook", table_name)
    habits = get_all_habit_names(table_name)
    assert len(habits) == 4

def test_deleted_completion_date(setup_habit_data):
    delete_habit_completion_date("Cook", "2024-04-01", table_name)
    entries = get_dates_completed("Cook", table_name)
    assert len(entries) == 22

@pytest.mark.parametrize("habit_name, expected_completion", [
    ("Cook", "Yes"), 
    ("Read", "No"), 
    ("Go to bed early", "No"), 
    ("Meet a friend", "Yes"), 
    ("Run", "No")
])
@freeze_time("2024-04-28")
def test_determined_completion(setup_habit_data, habit_name, expected_completion):
    determined_completion = determine_completion(habit_name, table_name)
    assert determined_completion == expected_completion

@freeze_time("2025-01-01") #future date is needed, because complete_habit function regards last entry of sorted dates list
def test_determined_completion_across_years(setup_habit_data):
    complete_habit("Cook", "2024-12-31", table_name)  
    determined_completion = determine_completion("Cook", table_name)
    assert determined_completion == "No"
    complete_habit("Cook", "2025-01-01", table_name)  
    determined_completion = determine_completion("Cook", table_name)
    assert determined_completion == "Yes"

    complete_habit("Run", "2024-12-26", table_name) # Last calender week of 2024 
    determined_completion = determine_completion("Run", table_name)
    assert determined_completion == "No"
    complete_habit("Run", "2025-01-01", table_name) # First calender week of 2025
    determined_completion = determine_completion("Run", table_name)
    assert determined_completion == "Yes"

@pytest.mark.parametrize("habit_name, expected_current_streak, expected_longest_sreak", [
    ("Cook", 2, 13),
    ("Read", 0, 12),
    ("Go to bed early", 11, 11),
    ("Meet a friend", 4, 4),
    ("Run", 0, 2)
])
@freeze_time("2024-04-28")
def test_determined_streaks(setup_habit_data, habit_name, expected_current_streak, expected_longest_sreak):
    determined_streaks = determine_streaks(habit_name, table_name)
    determined_current_streak = determined_streaks[0]
    assert determined_current_streak == expected_current_streak
    determined_longest_streak = determined_streaks[1]
    assert determined_longest_streak == expected_longest_sreak

@freeze_time("2025-01-02")
def test_determined_streaks_across_years_daily(setup_habit_data):
    complete_habit("Cook", "2024-12-31", table_name)
    determined_streaks = determine_streaks("Cook", table_name)
    determined_current_streak = determined_streaks[0]
    assert determined_current_streak == 0
    
    complete_habit("Cook", "2025-01-01", table_name)
    complete_habit("Cook", "2025-01-02", table_name)
    determined_streaks = determine_streaks("Cook", table_name)
    determined_current_streak = determined_streaks[0]
    assert determined_current_streak == 3
    determined_longest_streak = determined_streaks[1]
    assert determined_longest_streak == 13 # longest streak should still be 13

@freeze_time("2025-01-10")
def test_determined_streaks_across_years(setup_habit_data):
    determined_streaks = determine_streaks("Run", table_name)
    determined_current_streak = determined_streaks[0]
    assert determined_current_streak == 0
    determined_longest_streak = determined_streaks[1]
    assert determined_longest_streak == 2 # longest streak should still be 2
    
    complete_habit("Run", "2024-12-26", table_name)
    complete_habit("Run", "2025-01-01", table_name)
    complete_habit("Run", "2025-01-06", table_name)
    complete_habit("Run", "2025-01-08", table_name) # double completion of one week should be ignored
    determined_streaks = determine_streaks("Run", table_name)
    determined_current_streak = determined_streaks[0]
    assert determined_current_streak == 3
    determined_longest_streak = determined_streaks[1]
    assert determined_longest_streak == 3 # longest streak should now be updated to 3

def test_add_habit(setup_habit_data):
    habits = get_all_habit_names(table_name)
    assert len(habits) == 5

    add_habit("Dance", "Go to dancing a class", "weekly", table_name)
    habits = get_all_habit_names(table_name)
    assert len(habits) == 6

def test_create_last_completion_dates_list(setup_habit_data):
   last_completion_dates = create_last_completion_dates_list("Meet a friend", table_name)
   assert len(last_completion_dates) == 4

   last_completion_dates = create_last_completion_dates_list("Cook", table_name)
   assert len(last_completion_dates) == 10 # only the last ten dates should be shown

@freeze_time("2024-04-28") # counting starts on 2024-04-15
def test_create(setup_habit_data):
    available_dates = create_list_of_available_completion_dates("Read", table_name)
    assert len(available_dates) == 4 # not completed: 2024-04-17, 2024-04-25, 2024-04-27, 2024-04-28

    available_dates = create_list_of_available_completion_dates("Meet a friend", table_name)
    assert len(available_dates) == 12 # only completed: 2024-04-15, 2024-04-26

@freeze_time("2024-04-28")
def test_create_overview_table(setup_habit_data):
    create_overview_table("all", "Longest Streak", table_name) # program is able to print overview table

# Run the tests
pytest.main()


