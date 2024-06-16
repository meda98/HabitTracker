import questionary
from functionality import (
    add_habit, 
    create_overview_table,
    create_last_completion_dates_list,
    create_list_of_available_completion_dates
)
from database import (
    create_table,
    get_all_habit_names, 
    complete_habit, 
    delete_habit_data, 
    delete_habit_completion_date
)

# Call the create_table function to ensure the table exists
create_table()

# Introduction: Greet the user and ask for their name
user_name = questionary.text("Hi there! What's your name?").ask()

# Main loop to continuously prompt the user for tasks
while True:

      # Prompt user for task choice
      greeting_text = "Hi {name}, what would you like to do?".format(name=user_name)

      task_choice = questionary.select(
            greeting_text,
            choices = [ "Add a new habit",
                        "Complete a habit",
                        "Delete a habit, including all its data",
                        "Delete a completion date",
                        "Show an overview of my currently tracked habits",
                        "Exit"]
      ).ask()

      # Execute the chosen task
      if task_choice == "Add a new habit":
            habit_name = questionary.text("What's the name of your new habit?").ask()
            existing_habits = get_all_habit_names()
            if habit_name in existing_habits:
                  print("\nThe given name aleady exists within your habit tracker.")
            else:
                  habit_task_specification = questionary.text("Please specify the task of your habit:").ask()
                  habit_periodicity = questionary.select(
                        "Do you want to complete this habit daily or weekly?",
                        choices = ["daily", "weekly"]
                  ).ask()
                  add_habit(habit_name, habit_task_specification, habit_periodicity)
                  print("\nYour new habit \"{habit_name}\" has been added. Good luck!".format(habit_name = habit_name))


      elif task_choice == "Complete a habit":
            habit_list = get_all_habit_names()
            habit_name = questionary.select(
                  "Which habit do you want to complete? These are your current ones:",
                  choices = habit_list
            ).ask()
            available_completion_dates = create_list_of_available_completion_dates(habit_name)
            date_completed = questionary.select(
                  "When did you complete the habit?",
                  choices = available_completion_dates
            ).ask()
            complete_habit(habit_name, date_completed)
            print("\nThe date has been saved.\n")

                  
      elif task_choice == "Delete a habit, including all its data":
            habit_names = get_all_habit_names()
            
            habit_name = questionary.select(
                  "Which habit do you want to delete?",
                  choices = habit_names
            ).ask()

            delete_habit_data(habit_name)
            print("\nYour habit \"{habit_name}\", including all its data, has been deleted.".format(habit_name = habit_name))


      elif task_choice == "Delete a completion date":
            habit_names = get_all_habit_names()
            habit_name = questionary.select(
                  "For which habit do you want to delete a completion date?",
                  choices = habit_names
            ).ask()
            last_completion_dates = create_last_completion_dates_list(habit_name)
            habit_completion_date = questionary.select(
                  "Which of your last completion dates do you want to delete?",
                  last_completion_dates
            ).ask()
            delete_habit_completion_date(habit_name, habit_completion_date)
            print("\nThe completion date \"{habit_completion_date}\" for your habit \"{habit_name}\" has been deleted."
                        .format(habit_completion_date = habit_completion_date, habit_name = habit_name))
            

      elif task_choice == "Show an overview of my currently tracked habits":
            periodicity_list = ["all","daily","weekly"]
            periodicity_choice = questionary.select(
                  "Which habits do you want to be shown?",
                  choices = periodicity_list
            ).ask()
            column_list = ["Current Streak","Longest Streak"]
            column_sorted_by = questionary.select(
                  "Which column do you want to sort the table by?",
                  choices = column_list
            ).ask()
            create_overview_table(periodicity_choice, column_sorted_by)
            print("\nPlease click enter after you have finished analysing your habits.")
            input()


      elif task_choice == "Exit":
            print("\nSee you!")
            break



