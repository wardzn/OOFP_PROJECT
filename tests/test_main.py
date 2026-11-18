from datetime import datetime, timedelta
import pytest
from main import Habit, PredefinedHabit, CustomHabit

# Testing by setting up a fake "scenario" and then testing if the code works with it.

# Testing if the creation values will come out exactly as inputted
def test_habit_creation():
    habit = Habit("Exercise", "Daily workout", "daily")
    # Assert will fail to pass if the values are not the same
    assert habit.name == "Exercise"
    assert habit.current_streak == 0
    assert habit.longest_streak == 0
    assert len(habit.completed_dates) == 0

# Same as above, using assert we will be able to identify if the check_streaks's work
# Test that the streak will remain as 0 for the first 2 checks
def test_streak_begins_after_three_check_streaks():
    habit = Habit("Exercise", "Daily workout", "daily")

    # fake day 1
    habit.check_streak()
    assert habit.current_streak == 0

    # fake the last check-off to be 2 days ago, so today is a "new day"
    habit.last_completed_date = datetime.now() - timedelta(days=2)

    # fake day 2
    habit.check_streak()
    assert habit.current_streak == 0

    # fake the last check-off to be 2 days ago again
    habit.last_completed_date = datetime.now() - timedelta(days=2)

    # fake day 3
    habit.check_streak()
    assert habit.current_streak == 1

    # fake the last check-off to be 2 days ago again
    habit.last_completed_date = datetime.now() - timedelta(days=2)

    # fake day 4
    habit.check_streak()
    assert habit.current_streak == 2

    # Longest streak should match the current streak
    assert habit.longest_streak == 2

# Test to see if the DAILY streaks reset after the streak was not checked within the deadline.
def test_streak_breaks_after_missed_deadline():
    habit = Habit("Water", "Drink water", "daily")

    # Fake a 3-day streak
    habit.check_streak()
    habit.check_streak()
    habit.check_streak()
    habit.current_streak = 3
    habit.longest_streak = 3

    # Manually set the last completion to 2 days ago
    habit.last_completed_date = datetime.now() - timedelta(days=2)

    # Check deadline should reset current_streak but keep longest_streak
    habit.check_deadline()
    assert habit.current_streak == 0
    assert habit.longest_streak == 3

# Test to see if the WEEKLY streaks reset after the streak was not checked within the deadline.
def test_weekly_streak_breaks_after_missed_deadline():
    habit = Habit("Diary", "Write in diary", "weekly")

    # Fake a current streak
    habit.current_streak = 5
    habit.longest_streak = 5

    # Fake that the last check-off was 8 days ago (1 day past the 7-day limit)
    habit.last_completed_date = datetime.now() - timedelta(days=8)

    # Check the deadline
    habit.check_deadline()

    # The streak should break
    assert habit.current_streak == 0
    assert habit.longest_streak == 5  # Record should remain intact

# Test to check if the WEEKLY streak did not break before the deadline ends and that the code is working
def test_weekly_streak_stays_alive_within_deadline():
    # Only 6 days have passed
    habit = Habit("Diary", "Write in diary", "weekly")

    habit.current_streak = 5
    habit.longest_streak = 5

    # Fake that the last check-off was 6 days ago (still within the 7-day limit)
    habit.last_completed_date = datetime.now() - timedelta(days=6)

    habit.check_deadline()

    # The streak should remain 5
    assert habit.current_streak == 5

#  Test that a MONTHLY habit's streak resets if more than 30 days have passed
def test_monthly_streak_breaks_after_missed_deadline():
    habit = Habit("Deep Clean", "Clean the house", "monthly")

    habit.current_streak = 3
    habit.longest_streak = 3

    # Fake that the last check-off was 31 days ago (1 day past the 30-day limit)
    habit.last_completed_date = datetime.now() - timedelta(days=31)

    habit.check_deadline()

    assert habit.current_streak == 0
    assert habit.longest_streak == 3

# checks whether the codes going to inherit properly from the habit or not
def test_inheritance():
    p_habit = PredefinedHabit("Study", "Study daily", "daily")
    c_habit = CustomHabit("Read", "Read 20 pages", "daily")

    assert p_habit.is_predefined is True
    assert c_habit.is_predefined is False

    # Test that they inherit the check_streak method
    p_habit.check_streak()
    assert len(p_habit.completed_dates) == 1


# All the 8 tests passed



