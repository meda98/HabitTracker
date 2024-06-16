import datetime

class Habit:
  """
  Represents a habit with its details.

  This class is used to create and manage habits by storing the habit's name, task 
  specification, periodicity, and dates related to the habit.

  Attributes:
  - habit_name (str): The name of the habit.
  - habit_task_specification (str): The task specification of the habit.
  - habit_periodicity (str): The periodicity of the habit (e.g., daily or weekly).
  - date_added (str): The date when the habit was added, in the format 'YYYY-MM-DD'.
  - date_completed (str or None): The date when the habit was last completed, 
    in the format 'YYYY-MM-DD', or None if the habit hasn't been completed yet.
  """
  def __init__(self, habit_name, habit_task_specification, habit_periodicity, date_completed = None):
    self.habit_name                 = habit_name
    self.habit_task_specification   = habit_task_specification
    self.habit_periodicity          = habit_periodicity
    self.date_added                 = str(datetime.datetime.now().date())
    self.date_completed             = date_completed