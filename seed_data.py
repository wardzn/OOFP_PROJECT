from datetime import datetime, timedelta
from database import initialize_db, save, get_connection
from main import PredefinedHabit, CustomHabit
import main

# Populates the database with 4 weeks of fake data for the 5 predefined habits
def seed_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Checks if the database is already seeded
    cursor.execute("SELECT COUNT(*) FROM habits") # This code finds how many rows are in the table/returns list of all habits
    count = cursor.fetchone()[0] # Picks the first value from the row in the line above (ex. (5,) would become 5
    conn.close()

    # If the database contains any habits/entries (>0) then it will skip duplicates and exit
    if count > 0:
        print("Database already has data. Skipping seed.")
        return

    print("Seeding database with 4 weeks of data...")

    # Defining the 5 predefined habits
    predefined_habits = [
        ("Exercise", "Daily workout", "daily"),
        ("Study", "Study for 1 hour", "daily"),
        ("Drink Water", "Drink 1.5L of water", "daily"),
        ("Diary", "Write in diary", "weekly"),
        ("Meal Prep", "Prep meals for the week", "weekly")
    ]

    # Setting the variable "now" to the date now
    now = datetime.now()

    # For every single entry in predefined_habits, iterate through them and create an object for every single one
    for name, desc, periodicity in predefined_habits:
        habit = PredefinedHabit(name, desc, periodicity)

        # Fake the creation date (using timedelta) to 4 weeks ago in order to seed the data for a period of 4 weeks
        # creation_date is now 4 weeks old
        habit.creation_date = now - timedelta(weeks=4)

        # Generate fake check-off dates
        if periodicity == "daily":
            """"
             This creates a loop using a range set to count backwards from 28 to 1. The loop will check the created habit 
            and then mark each day as [for ex. (today - 28) = 28 days ago] and then append it to the completed_dates 
            list. However, If the number is part of the list in i then it would continue(Skip).
            """
            for i in range(28, -1, -1):
                # We need to skip some days to make it realistic
                # So if the day we are looking at is one of the ones in "i" then continue(Used as a skip here)
                if name == "Exercise" and i in [5, 12, 20, 25]: # 4 days missed in this one
                    continue # i
                if name == "Study" and i in [3, 8, 10, 15, 22, 26, 27, 28]: # 8 days missed in this one
                    continue
                if name == "Drink Water" and i in [7, 14]: # 2 days missed in this one
                    continue

                # Today - iteration = Num of days ago
                fake_date = now - timedelta(days=i)
                habit.completed_dates.append(fake_date) # Then append it to the completed_dates list in habit

        elif periodicity == "weekly":
            # Same as above but we step 7 times backwards
            if name == "Diary":
                for i in range(28, 0, -7):
                    habit.completed_dates.append(now - timedelta(days=i))
            elif name == "Meal Prep":
                for i in range(28, 7, -7): # This range function stops at 7 so the last week is missed
                    habit.completed_dates.append(now - timedelta(days=i))

        # Sort the dates so the dates are no longer backwards
        habit.completed_dates.sort()


        if len(habit.completed_dates) >= 3:
            # Since the streak doesnt start until 3 tries then we will subtract two here to confirm this
            habit.current_streak = len(habit.completed_dates) - 2
            # Since meal prep missed the last week so it has to equal to 0
            if name == "Meal Prep":
                habit.current_streak = 0

            # Same as above where the streak only starts at 3 so the longest streak doesnt count
            habit.longest_streak = len(habit.completed_dates) - 2

        # If the list is not empty
        if habit.completed_dates:
            habit.last_completed_date = habit.completed_dates[-1] # The last_completed_date will be the last entry in the list

        # Finally we save the habits to the database
        save(habit)

    print("Prepopulation/Seeding process is complete!")


if __name__ == "__main__":
    initialize_db()  # Make sure tables exist
    seed_database()  # Fill with fake data that we just wrote in the function above




