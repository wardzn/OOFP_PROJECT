import sqlite3
from main import PredefinedHabit, CustomHabit, Habit
from datetime import datetime
import os

DB_NAME = "habits.db"

# Creates a connection
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    # This allows us to access columns by name instead of just index (Will be beneficial for the loading function later)
    conn.row_factory = sqlite3.Row
    return conn

# Initializes a database if it doesn't already exist
def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Creates the habits table if it does not already exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            periodicity TEXT,
            created_at TEXT,
            current_streak INTEGER,
            longest_streak INTEGER,
            is_predefined INTEGER
        )
    """)

    # Create the completions table if it doesnt already exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER,
            completed_at TEXT,
            FOREIGN KEY (habit_id) REFERENCES habits (id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()

# Saves a new habit or updates an existing one in SQLite3
def save(habit):

    conn = get_connection()
    cursor = conn.cursor()

    # Check if the habit has an ID. If not, it iss new and we can proceed
    if habit.id is None:
        cursor.execute("""
            INSERT INTO habits (name, description, periodicity, created_at, current_streak, longest_streak, is_predefined)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            habit.name, habit.description, habit.periodicity,
            habit.creation_date.strftime("%Y-%m-%d %H:%M:%S"), # Set the date to this format in the brackets
            habit.current_streak, habit.longest_streak,
            1 if isinstance(habit, PredefinedHabit) else 0
            # With isinstance we set the habit types to 0 (custom habit) and 1 (Predefined habit) then use isinstance true return True or False
        ))
        # Save the new ID back to the habit object so we know it for next time
        habit.id = cursor.lastrowid

        # Insert every single completion date into the DB
        for date in habit.completed_dates:
            cursor.execute("INSERT INTO completions (habit_id, completed_at) "
                           "VALUES (?, ?)",
                           (habit.id, date.strftime("%Y-%m-%d %H:%M:%S")))

    else:
        # If it is not new then update said existing habit
        cursor.execute("""
            UPDATE habits 
            SET name = ?, description = ?, periodicity = ?, current_streak = ?, longest_streak = ?
            WHERE id = ?
        """, (
            habit.name, habit.description, habit.periodicity,
            habit.current_streak, habit.longest_streak, habit.id
        ))

        # only adds the new dates for the completions
        cursor.execute("DELETE FROM completions WHERE habit_id = ?", (habit.id,))
        for date in habit.completed_dates:
            cursor.execute("INSERT INTO completions (habit_id, completed_at) VALUES (?, ?)",
                           (habit.id, date.strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()
    conn.close()
    print(f"Saved {habit.name} (ID: {habit.id}) to SQLite!")


def load_all_habits():

    conn = get_connection()
    cursor = conn.cursor()

    # gets all habits
    cursor.execute("SELECT * FROM habits")
    habit_rows = cursor.fetchall() # Fetches all the data in the database (returns all the rows)

    habits_list = []

    # Use a 'for loop' to fetch out all the habits that exist one by one
    # Essentially we are making new adjusted objects
    for row in habit_rows:
        # Recreate the object to the type that is needed
        if row["is_predefined"] == 1: # If the is_predefined = 1, it is predefined
            habit = PredefinedHabit(row["name"], row["description"], row["periodicity"]) # Object
        else: # If the is_predefined = 0, it is custom
            habit = CustomHabit(row["name"], row["description"], row["periodicity"]) # Object

        # Restoring all the attributes
        # setting habit.id for this specific habit to take it from that specific row?
        habit.id = row["id"]
        habit.creation_date = datetime.strptime(row["created_at"], "%Y-%m-%d %H:%M:%S")
        habit.current_streak = row["current_streak"]
        habit.longest_streak = row["longest_streak"]

        # Get the completion dates (rows) for this specific habit
        cursor.execute("SELECT completed_at FROM completions WHERE habit_id = ?", (habit.id,))
        completion_rows = cursor.fetchall()

        # This nested loop will fetch the completion dates
        for c_row in completion_rows:
            # This converts the string (strptime) back to datetime
            date_obj = datetime.strptime(c_row["completed_at"], "%Y-%m-%d %H:%M:%S")
            habit.completed_dates.append(date_obj) # the list is in the original habit class (Iterated values per habit)

        # This sets the last_completed_date if there are completions
        if habit.completed_dates: # Only passes if there is at least 1 value
            habit.completed_dates.sort()  # Sort to make sure the last one is the newest
            habit.last_completed_date = habit.completed_dates[-1] # assigns the last (newest check_off) value in the list to last_completed_date

        habits_list.append(habit)

    conn.close()
    return habits_list

def delete(habit_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))

    conn.commit()
    conn.close()
    print(f"Deleted habit ID {habit_id} from SQLite!")


