import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import Habit, PredefinedHabit
from analytics import (get_habits_ordered_by_periodicity, get_current_longest_streak, get_overall_longest_streak)
import analytics


# This fixture gives us a fake set of habits to test with
@pytest.fixture

# Here we created some habits that will be used in order to test the code we wrote in analytics.py
def mock_habits():
    # Habit A: daily, active streak of 10 and record of 10
    h1 = Habit("Exercise", "Workout", "daily")
    h1.current_streak = 10
    h1.longest_streak = 10

    # Habit B: weekly, broken streak (0) but a big record of 30
    h2 = Habit("Diary", "Write diary", "weekly")
    h2.current_streak = 0
    h2.longest_streak = 30

    # Habit C: monthly, active streak of 5 and a record of 8
    h3 = Habit("Clean", "Clean house", "monthly")
    h3.current_streak = 5
    h3.longest_streak = 8

    return [h1, h2, h3]

# We are using monkeypatch for testing below. It tells python that this code is temporary and to use it for the duration of the testing phase.

# Test that habits are sorted in this order [ daily -> weekly -> monthly ]
def test_habits_ordered_by_periodicity(monkeypatch, mock_habits):
    # We temporarily replace the database call with our fake list
    monkeypatch.setattr(analytics, "load_all_habits", lambda: mock_habits) # We set the attribute inbetween the bracket

    sorted_habits = get_habits_ordered_by_periodicity() # Now we apply the order function

    # We will use assert to confirm if the function works as it should
    # The order should be Daily (Exercise), Weekly (Diary), Monthly (Deep Clean)
    assert len(sorted_habits) == 3
    assert sorted_habits[0].name == "Exercise"  # daily
    assert sorted_habits[1].name == "Diary"  # weekly
    assert sorted_habits[2].name == "Clean"  # monthly


# Test that it finds the highest currently active streak (essentially ignoring broken ones)
def test_current_longest_streak(monkeypatch, mock_habits):
    monkeypatch.setattr(analytics, "load_all_habits", lambda: mock_habits) # Setting the attributes for this test

    best_now = get_current_longest_streak()

    # We will use assert to confirm that it could find the current biggest streak
    # Exercise has 10 (active), Deep Clean has 5 (active). Diary is 0 (broken). So it should pick "Exercise"
    assert best_now is not None
    assert best_now.name == "Exercise"
    assert best_now.current_streak == 10


# Test that it finds the all-time record, even if the streak is broken
def test_overall_longest_streak(monkeypatch, mock_habits):
    monkeypatch.setattr(analytics, "load_all_habits", lambda: mock_habits) # Setting the attributes like the two above

    best_ever = get_overall_longest_streak()

    # We will use assert to confirm that it could find the biggest streak ever
    # Diary is broken (streak = 0), but its best streak ever is 30. # So it should pick "Diary"
    assert best_ever is not None
    assert best_ever.name == "Diary"
    assert best_ever.longest_streak == 30

# Test that analytics handles an empty database fluidly
def test_analytics_empty_database(monkeypatch):

    # Pretend the database is empty
    monkeypatch.setattr(analytics, "load_all_habits", lambda: []) # We won't use mock_habits here because we need the set to be empty

    # Using assert to confirm that when the list has no entries then the code won't run into an error.
    assert get_habits_ordered_by_periodicity() == []
    assert get_current_longest_streak() is None
    assert get_overall_longest_streak() is None


# All 3 tests passed.


