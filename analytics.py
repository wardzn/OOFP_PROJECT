from database import load_all_habits

# Returns all habits ordered by daily, weekly and monthly
def get_habits_ordered_by_periodicity():

    habits = load_all_habits() # loads/calls all the habits/objects that are stored

    # We define the order we want (daily first, weekly second, monthly last)
    periodicity_order = {"daily": 1, "weekly": 2, "monthly": 3} # Simply done to rank them for the order them by periodicity for the users

    # sorted() takes the list and sorts it in the order we decide
    # This will return a new list for the habits and the key=lambda part will allow sorted to give us a rank for each habit based on its periodicity
    sorted_habits = sorted(habits, key=lambda h: periodicity_order.get(h.periodicity, 4))

    return sorted_habits


# Returns the habit with the highest currently active streak (Habit is still active)
def get_current_longest_streak():

    habits = load_all_habits() # loads/calls all the habits/objects that are stored

    if not habits: # if habits list is empty return none so no error occurs for max() below (Could also use Try/Except so consider it when reviewing code)
        return None

    # max() looks through the list and finds the item with the highest value (highest streak)
    # We tell it to look at the 'current_streak' attribute in main.py
    biggest_habit = max(habits, key=lambda h: h.current_streak)

    # If the biggest habit has a streak value of 0 then there is no active streak and return none
    if biggest_habit.current_streak == 0:
        return None

    return biggest_habit


# Returns the habit with the highest streak ever recorded by the user that exists within its database
def get_overall_longest_streak():

    habits = load_all_habits() # loads/calls all the habits/objects that are stored

    if not habits: # if habits list is empty return none so no error occurs for max() below
        return None

    # Same as above but we look at the 'longest_streak' attribute from main.py instead
    biggest_habit = max(habits, key=lambda h: h.longest_streak)

    return biggest_habit





