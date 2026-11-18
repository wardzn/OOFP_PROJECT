# This is the model for the Habit class
# The habit class will contain most of the work
# analytics.py will read this class
# database.py will store values from this class
from datetime import datetime, timedelta


# The habit class will contain all the data that will be used in the app. All of our objects will be created from the data in here.
class Habit:

    # Initializing the habit and all the necessary data for streaks
    def __init__(self, name, description, periodicity):
        self.id = None
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.creation_date = datetime.now()
        self.completed_dates = []
        self.current_streak = 0
        self.longest_streak = 0
        self.last_completed_date = None

# If we check a streak three times then a habit streak will start
    def check_streak(self):

        now = datetime.now()

        # Conditions depending on periodicity
        if self.last_completed_date is not None:
            if self.periodicity == "daily":
                if self.last_completed_date.date() == now.date():
                    return False  # Already done today

            elif self.periodicity == "weekly":
                if (now - self.last_completed_date).days < 7:
                    return False  # Already done this week

            elif self.periodicity == "monthly":
                if (now - self.last_completed_date).days < 30:
                    return False  # Already done this month

        # Appends now to the completed_dates list
        self.completed_dates.append(now)

        # Sets the last_completed_date to now
        self.last_completed_date = now

        # The streaks will only start at 3 check offs so the rule is set
        if len(self.completed_dates) < 3:
            self.current_streak = 0
        else:
            self.current_streak += 1

        # Update the longest streak if the current_streak becomes bigger than the longest_streak
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak

        return True  # successfully checked off

    # If the streak is not checked off in time, the streak will be reset to 0
    def check_deadline(self):

        if self.last_completed_date is None: # We do this to avoid errors in the code below should the list be empty
            return

        now = datetime.now() # We have to set this everytime since it is local and not global

        # Functionality for each Periodicity and how to check their deadline using the timedelta function
        # Using the timedelta function we can create difference between two dates or times

        # If we miss a day without checking then todays date would be bigger than yesterday and hence reset the streak
        if self.periodicity == "daily":
            if now > self.last_completed_date + timedelta(days=1): # For daily streaks
                self.current_streak = 0

        # If we go 8 days without checking then todays date would be bigger than the last_completed_date by 7 and hence reset the streak
        elif self.periodicity == "weekly":
            if now > self.last_completed_date + timedelta(days=7): # For weekly streaks
                self.current_streak = 0

        # Same as the weekly condition above but with 30 days instead
        elif self.periodicity == "monthly":
            if now > self.last_completed_date + timedelta(days=30): # For monthly streaks
                self.current_streak = 0

class PredefinedHabit(Habit):
    def __init__(self, name, description, periodicity):
        # This calls the Habit __init__ so we do not have to rewrite it
        super().__init__(name, description, periodicity) # Using super() we inherit these values from the init in the first class
        self.is_predefined = True # Tells us that it is a predefined habit


class CustomHabit(Habit):
    def __init__(self, name, description, periodicity):
        super().__init__(name, description, periodicity) # Using super() we inherit these values from the init in the first class
        self.is_predefined = False # Tells us that it is a custom habit



