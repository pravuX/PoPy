"""
Rewrite of my pomodoro app using the Model-View-Controller design pattern.

model.py:
    The model in my pomodoro app is going to incorporate a worker thread
    that does the countdown and update the corresponding labels in the UI.

view.py:
    Creates the graphical front end for the application.

controller.py:
    Takes an instance of both model and view and literally joins them.
    Signals from view are passed to model and updates from model are
    passed to view
"""
