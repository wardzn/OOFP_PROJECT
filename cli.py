import questionary
from database import load_all_habits, initialize_db, save, delete
from analytics import get_habits_ordered_by_periodicity, get_current_longest_streak, get_overall_longest_streak
from seed_data import seed_database
import sqlite3
from main import PredefinedHabit, CustomHabit, Habit
from datetime import datetime
import os

"""
Questinary notes:
With the questionary module, the user can use questionary.select to make choices at the start of the commands.
Make sure to add .ask() in the end so the the user is asked for said choices.
Make sure cancel/exit is part of the choices or else the user will be stuck.
Add confirmation to edit and delete.
"""

def main_menu():
    # Initialize the DB just in case
    initialize_db()

    # Creates 4 weeks of seeded / pre-populated data on app startup
    seed_database()

    # A while loop so the app would not close on the user after doing only 1 activity
    while True:
        # Displays the main menu
        choice = questionary.select(
            "What would you like to do?",
            choices=[
                "Check Habit",
                "Create Habit",
                "Edit Habit",
                "Delete Habit",
                "Analytics",
                "Exit"
            ]
        ).ask()

        # Conditions for user choices
        if choice == "Check Habit":
            check_habit()
        elif choice == "Create Habit":
            create_habit()
        elif choice == "Edit Habit":
            edit_habit()
        elif choice == "Delete Habit":
            delete_habit()
        elif choice == "Analytics":
            show_analytics()
        elif choice == "Exit":
            print("Goodbye!")
            break # This breaks the while loop and closes the app


# For both Custom and Predefined habits
def create_habit():

    habit_type = questionary.select(
        "What type of habit do you want to create?",
        choices=["Predefined", "Custom", "Cancel"]
    ).ask()

    if habit_type == "Cancel":
        return

    if habit_type == "Predefined":
        predefined_choices = [
            "Exercise (Daily)",
            "Study (Daily)",
            "Drink 1.5L Of Water (Daily)",
            "Diary (Weekly)",
            "Meal Prep (Weekly)",
        ]

        choice = questionary.select(
            "Which predefined habit?",
            choices=predefined_choices + ["Cancel"]
        ).ask()

        if choice == "Cancel":
            return

        if choice == "Exercise (Daily)":
            name = "Exercise"
            desc = "Daily workout"
            periodicity = "daily"
        elif choice == "Study (Daily)":
            name = "Study"
            desc = "Study for 1 hour"
            periodicity = "daily"
        elif choice == "Drink 1.5L Of Water (Daily)":
            name = "Drink Water"
            desc = "Drink 1.5L of water"
            periodicity = "daily"
        elif choice == "Diary (Weekly)":
            name = "Diary"
            desc = "Write in diary"
            periodicity = "weekly"
        elif choice == "Meal Prep (Weekly)":
            name = "Meal Prep"
            desc = "Prep meals for the week"
            periodicity = "weekly"

        # Checks if the user has this streak as an active one
        existing = load_all_habits()
        if any(h.name == name for h in existing):
            print("\n")
            print(f"You already have a habit called '{name}'!")
            print("\n")
            return

        # Creates the object after its been confirmed that it is not a duplicate and save it to the DB
        habit = PredefinedHabit(name, desc, periodicity)
        save(habit)
        print("\n")
        print(f"Created predefined habit: {name} ({periodicity}) ")
        print("\n")

    # Custom habit
    else:
        name = questionary.text("Enter habit name: ").ask()
        if not name or not name.strip():
            print("Habit name cannot be empty!!!")
            return

        description = questionary.text("Enter habit description: ").ask()

        periodicity = questionary.select(
            "Would you like this to be a daily, weekly or monthly thing?",
            choices=["daily", "weekly", "monthly"]
        ).ask()

        habit = CustomHabit(name.strip(), description.strip(), periodicity)
        save(habit)
        print("\n")
        print(f"Created custom habit: {name} ({periodicity})")
        print("\n")

    # User must click to continue. Done so the user can read before the menu reappears
    questionary.press_any_key_to_continue().ask()


def check_habit():

    habits = load_all_habits()

    if not habits:
        print("\n")
        print("You have no habits yet! Create one first.")
        print("\n")
        return

    habit_choices = [f"{h.name} ({h.periodicity})" for h in habits]

    # asks the user which habit to check off
    choice = questionary.select(
        "Which habit did you complete?",
        choices=habit_choices + ["Cancel"] # Either he chooses one of the habits or cancels
    ).ask()

    if choice == "Cancel":
        return

    # Find the habit object that matches the chosen string
    # The index of the chosen string is the same as the index in `habits`
    chosen_index = habit_choices.index(choice) # choice returns a string then this turns it into its position in the DB
    habit = habits[chosen_index] # This uses the index position in the DB for said habit so we can select it

    habit.check_deadline() # check if the habit deadline has already been broken

    # now the user can check off the habit
    success = habit.check_streak()

    # save it back to the database or tell user they already completed it
    if success:
        save(habit)
        print("\n")
        print(f"Checked off: {habit.name}")
        print(f"Current streak: {habit.current_streak}")
        print(f"Longest streak: {habit.longest_streak}")
        print("\n")
    else:
        print("\n")
        print(f"You already completed '{habit.name}' for this {habit.periodicity} period!")
        print("\n")

    # User must click to continue. Done so the user can read before the menu reappears
    questionary.press_any_key_to_continue().ask()


def edit_habit():

    habits = load_all_habits()

    if not habits:
        print("You have no habits to edit!")
        return

    # Pick which habit to edit
    habit_choices = [f"{h.name} ({h.periodicity})" for h in habits]
    choice = questionary.select(
        "Which habit do you want to edit?",
        choices=habit_choices + ["Cancel"]
    ).ask()

    if choice == "Cancel":
        return

    # Same as check_habit
    chosen_index = habit_choices.index(choice)
    habit = habits[chosen_index]

    # pick which section to edit - section representing one of the values in the habit
    section = questionary.select(
        f"What would you like to edit about '{habit.name}'?",
        choices=["Name", "Description", "Periodicity", "Cancel"]
    ).ask()

    if section == "Cancel":
        return

    if section == "Name":
        new_name = questionary.text("Enter new name:").ask()
        if new_name and new_name.strip():
            habit.name = new_name.strip()
            print("\n")
            print(f"Name updated to: {habit.name}")
            print("\n")
        else:
            print("\n")
            print("Invalid name. No changes made.")
            print("\n")
            return

    elif section == "Description":
        new_desc = questionary.text("Enter new description:").ask()
        habit.description = new_desc.strip() if new_desc else ""
        print("Description has been updated!!")

    elif section == "Periodicity":
        new_periodicity = questionary.select(
            "Choose new periodicity:",
            choices=["daily", "weekly", "monthly"]
        ).ask()
        habit.periodicity = new_periodicity
        print("\n")
        print(f"Periodicity updated to: {habit.periodicity}")
        print("\n")

    # Confirmation
    confirm = questionary.confirm(
        f"Are you sure you want to save these changes to '{habit.name}'?"
    ).ask()

    if confirm:
        save(habit)
        print("\n")
        print(f"Changes saved successfully!")
        print("\n")
    else:
        print("\n")
        print("Changes cancelled.")
        print("\n")

    # User must click to continue. Done so the user can read before the menu reappears
    questionary.press_any_key_to_continue().ask()


def delete_habit():
    habits = load_all_habits()
    if not habits:
        print("\n")
        print("You have no habits to delete!")
        print("\n")
        return

    # Pick which habit to delete
    habit_choices = [f"{h.name} ({h.periodicity})" for h in habits]
    choice = questionary.select(
        "Which habit do you want to delete?",
        choices=habit_choices + ["Cancel"]
    ).ask()

    if choice == "Cancel":
        return

    # Same as check_habit
    chosen_index = habit_choices.index(choice)
    habit = habits[chosen_index]

    # confirmation
    confirm = questionary.confirm(
        f"Are you sure you want to delete '{habit.name}'? This will also delete all its history."
    ).ask()

    if confirm:
        delete(habit.id)
        print("\n")
        print(f"'{habit.name}' deleted successfully!")
        print("\n")
    else:
        print("\n")
        print("Deletion cancelled.")
        print("\n")

    # User must click to continue. Done so the user can read before the menu reappears
    questionary.press_any_key_to_continue().ask()


def show_analytics():

    habits = get_habits_ordered_by_periodicity()

    if not habits:
        print("\n")
        print("You have no habits yet! Create one first.")
        print("\n")
        return

    print("\n")
    print("YOUR ANALYTICS:")
    print("_" * 50)
    print("\n")

    # prints all habits ordered by periodicity
    print("Habits ordered by periodicity:")
    for h in habits:
        print(f"[{h.periodicity.upper()}] {h.name} ") # Periodicity + name
        print(f"Current streak: {h.current_streak} ")
        print(f"Record: {h.longest_streak} ")
        print("\n")

    # shows the current longest currently active streak
    current_best = get_current_longest_streak()
    print("Current longest active streak:")
    if current_best:
        print(f"  {current_best.current_streak} with {current_best.name}! ")
    else:
        print("No active streaks right now.")

    # shows the all-time record / longest streak ever recorded for the user
    overall_best = get_overall_longest_streak()
    print("\n")
    print("All-time longest streak (record): ")
    if overall_best:
        print(f"  {overall_best.longest_streak} with {overall_best.name}!  ")
    else:
        print("No streak records yet! Start some streaks and set new records daily!!!")

    print("\n")

    # User must click to continue. Done so the user can read before the menu reappears
    questionary.press_any_key_to_continue().ask()



if __name__ == "__main__":
    main_menu()


