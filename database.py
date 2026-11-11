import sqlite3
from models import PredefinedHabit, CustomHabit, Habit
from datetime import datetime
import os

DB_NAME = "habits.db"

# Creates a connection
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    # This allows us to access columns by name instead of just index
    conn.row_factory = sqlite3.Row
    return conn

# Initializes a database if it doesn't already exist
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Creates the habits table
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

    # Create the completions table
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

## Tests if the database initializes properly
# if __name__ == "__main__":
#     init_db()
#     print("Database and tables created successfully!")

# Saves a new habit or updates an existing one in SQLite3
def save(habit):

    conn = get_connection()
    cursor = conn.cursor()

    # Check if the habit has an ID. If not, it's new!
    if habit.id is None:
        # --- NEW HABIT (INSERT) ---
        cursor.execute("""
            INSERT INTO habits (name, description, periodicity, created_at, current_streak, longest_streak, is_predefined)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            habit.name, habit.description, habit.periodicity,
            habit.creation_date.strftime("%Y-%m-%d %H:%M:%S"),
            habit.current_streak, habit.longest_streak,
            1 if isinstance(habit, PredefinedHabit) else 0
        ))
        # Save the new ID back to the habit object so we know it for next time
        habit.id = cursor.lastrowid

        # Insert ALL completion dates
        for date in habit.completed_dates:
            cursor.execute("INSERT INTO completions (habit_id, completed_at) VALUES (?, ?)",
                           (habit.id, date.strftime("%Y-%m-%d %H:%M:%S")))

    else:
        # --- EXISTING HABIT (UPDATE) ---
        cursor.execute("""
            UPDATE habits 
            SET name = ?, description = ?, periodicity = ?, current_streak = ?, longest_streak = ?
            WHERE id = ?
        """, (
            habit.name, habit.description, habit.periodicity,
            habit.current_streak, habit.longest_streak, habit.id
        ))

        # For completions, we only want to add the NEWEST date.
        # We can do this by checking if it's already in the database,
        # but for simplicity, let's just clear the old ones and re-insert them all.
        # (This is a bit lazy but perfectly fine for a small app).
        cursor.execute("DELETE FROM completions WHERE habit_id = ?", (habit.id,))
        for date in habit.completed_dates:
            cursor.execute("INSERT INTO completions (habit_id, completed_at) VALUES (?, ?)",
                           (habit.id, date.strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()
    conn.close()
    print(f"Saved {habit.name} (ID: {habit.id}) to SQLite!")





