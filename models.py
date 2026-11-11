from datetime import datetime, timedelta

class Habit:

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

# If we check a streak then the 
    def check_streak(self):
        now = datetime.now()

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

    def check_deadline(self):
        if self.last_completed_date is None:
            return

        now = datetime.now()

        # Functionality for each Periodicity and how to check their deadline using timedelta
        # Using timedelta we can create difference between two dates or times
        if self.periodicity == "daily":
            if now > self.last_completed_date + timedelta(days=1):
                self.current_streak = 0
        elif self.periodicity == "weekly":
            if now > self.last_completed_date + timedelta(days=7):
                self.current_streak = 0
        elif self.periodicity == "monthly":
            if now > self.last_completed_date + timedelta(days=30):
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

