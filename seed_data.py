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
                if name == "Drink Water" and i in [10]: # 1 day missed in this one
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

        # Simulate
        consecutive_count = 0  # for check-offs in a row

        for fake_date in habit.completed_dates:

            # Check for missed deadlines
            missed = False

            # If last_completed_date is not empty
            if habit.last_completed_date is not None:

                # If fake_date is bigger than last_completed date + day/week/month then date is missed
                if habit.periodicity == "daily":
                    if fake_date > habit.last_completed_date + timedelta(days=1):
                        missed = True

                elif habit.periodicity == "weekly":
                    if fake_date > habit.last_completed_date + timedelta(days=7):
                        missed = True

                elif habit.periodicity == "monthly":
                    if fake_date > habit.last_completed_date + timedelta(days=30):
                        missed = True

            # If missed then restart from 0
            if missed:
                consecutive_count = 0
                habit.current_streak = 0

            # Add this check off to the count
            consecutive_count += 1

            # Since streaks start after the 3rd check off:
            # Once the concecutive_count >= 3 then start the streak counting
            if consecutive_count >= 3:
                habit.current_streak = consecutive_count - 2
            else:
                habit.current_streak = 0

            # Update the all time record
            if habit.current_streak > habit.longest_streak:
                habit.longest_streak = habit.current_streak

            habit.last_completed_date = fake_date

        # Check if the habit has been broken today by checking if now is bigger than the last checkoff by 1 day for daily etc
        if habit.last_completed_date is not None:
            if habit.periodicity == "daily" and now > habit.last_completed_date + timedelta(days=1):
                habit.current_streak = 0
            elif habit.periodicity == "weekly" and now > habit.last_completed_date + timedelta(days=7):
                habit.current_streak = 0
            elif habit.periodicity == "monthly" and now > habit.last_completed_date + timedelta(days=30):
                habit.current_streak = 0

        save(habit)

    print("Prepopulation/Seeding process is complete!")


if __name__ == "__main__":
    initialize_db()  # Make sure tables exist
    seed_database()  # Fill with fake data that we just wrote in the function above




