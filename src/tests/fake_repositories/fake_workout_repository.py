from dto.workout_summary import WorkoutSummary

class FakeWorkoutRepository:
    def __init__(self, workouts=None):
        self.workouts = workouts or []
        self._next_id = 1

    def delete_all(self):
        self.workouts = []
        self._next_id = 1

    def get_all_workout_summaries(self):
        return sorted(
            [
                WorkoutSummary(
                    workout_id=w.id,
                    date=w.date,
                    title=w.title,
                    duration=w.duration
                )
                for w in self.workouts
            ],
            key=lambda w: (w.date, w.workout_id),
            reverse=True
        )

    def get_by_id(self, workout_id):
        return next(
            (w for w in self.workouts if w.id == workout_id),
            None
        )

    def create(self, workout):
        workout.id = self._next_id
        self._next_id += 1
        self.workouts.append(workout)
        return workout

    def update(self, workout):
        for i, w in enumerate(self.workouts):
            if w.id == workout.id:
                self.workouts[i] = workout
                return workout
        return workout

    def delete(self, workout):
        self.workouts = [w for w in self.workouts if w.id != workout.id]

    def get_all_from_timespan(self, start, end):
        return [w for w in self.workouts if w.date >= start and w.date <= end]
