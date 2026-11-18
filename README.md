# Habit Tracking App

A simple habit tracking application. Users get to create both predefined and custom habits 
with streaks that would need to be checked off on a certain day depending on their 
periodicity. The habits can later be edited or deleted and the users can also check 
the analytics section to check their progress. 

# Application Features
#### CRUD Operations: Create, Edit or delete habits at any time.
#### Custom Habits: Users can create their own custom habit.
#### Predefined Habits: Users can pick from 5 predefined habits.
#### Streak Tracking: Automatically calculates streaks when the user checks them off.
#### Periodicity: Users get to choose from daily, weekly or monthly streaks.
#### Analytics: View all habits ordered by periodicity(daily > weekly > monthly), your current longest active streak, and your all-time streak record.
#### Data Persistence: Uses SQLite3 to securely store your habits and completion history.
#### CLI: Built with `questionary` for a smooth experience.

# Required
- Python 3.8 or higher
- Dependencies listed in `requirements.txt`

# Seeded data
#### Should automatically happen when the user access's the main menu. Should it not work automatically, run 'python seed_data.py' before running the app.






