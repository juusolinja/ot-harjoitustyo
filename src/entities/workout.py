class Workout:
    def __init__(self, title, date, notes=None, workout_id=None, duration=None, sets=None):
        self.title = title
        self.date = date
        self.notes = notes
        self.id = workout_id
        self.duration = duration
        self.sets = sets if sets is not None else []
