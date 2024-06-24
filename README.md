# Habit Tracker

This is a habit tracker application that allows you to manage and track your habits through a command-line interface. 
The application uses the questionary library to provide an interactive experience for users and the rich library for creating an overview table.

## Features

- **Add a New Habit:** Create a new habit with a specified task and periodicity (daily or weekly).
- **Complete a Habit:** Mark a habit as completed for a specific date.
- **Delete a Habit:** Remove a habit along with all its associated data.
- **Delete a Completion Date:** Remove a specific completion date for a habit.
- **Show an Overview:** Display an overview of your currently tracked habits with sorting options.
- **Exit:** Exit the application.

## Setup

Download 'HabitTracker' as ZIP and open folder within terminal.

## Prerequisites

Ensure you have installed the requirements. Those include the following:

- Python 3.6+
- **'questionary'** library
- **'pytest'** and **'freezegun'** for running tests
- **'questionary'** for creating and displaying the overview table

You can install the required libraries using pip:

```console
pip install -r requirements.txt
```

## Usage

Run the application using Python:

```console
python main.py
```

or

```console
python3 main.py
```

Upon running the application, you will be prompted to enter your name. After that, you will enter the main loop where you can select from the available tasks.

