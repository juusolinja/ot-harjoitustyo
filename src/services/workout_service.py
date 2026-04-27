import re
from datetime import datetime
from entities.workout import Workout
from entities.set_entry import SetEntry

from repositories.workout_repository import (
    workout_repository as default_workout_repository
)


class WorkoutService:
    """Treeneihin liittyvästä logiikasta vastaava luokka
    """

    def __init__(self, workout_repository=default_workout_repository):
        """Luokan konstruktori

        Args:
            workout_repository:
                Vapaaehtoinen, oletusarvoltaan WorkoutRepository-olio
                Olio, jolla on WorkoutRepository-luokkaa vastaavat metodit
        """

        self._workout_repository = workout_repository

    def create_workout(self, title, date, duration, notes, sets):
        """Luo treenin

        Args:
            title: Merkkijonoarvo, joka kuvaa treenin nimeä
            date: Merkkijonoarvo, joka kuvaa treenin päivämäärää
            duration: Kokonaisluku, joka kuvaa treenin kestoa
            notes: Merkkijonoarvo, joka kuvaa treenin muistiinpanoja
            sets: Lista kirjastoja, jotka kuvaa tehtyjä sarjoja

        Returns:
            Palauttaa luodun treenin Workout-oliona
        """

        set_entries = [
            SetEntry(
                movement=s["movement"],
                reps=s["reps"],
                weight=s["weight"],
                rir=s["rir"]
            )
            for s in sets
        ]
        workout = self._workout_repository.create(
            Workout(title=title, date=date, duration=duration,
                    notes=notes, sets=set_entries)
        )
        return workout

    def get_workout_by_id(self, workout_id):
        """Palauttaa treenin id:n perusteella

        Args:
            workout_id: Palautettavan treenin id

        Returns:
            Palauttaa Workout-olion, jos on olemassa treeni kyseisellä id:llä
            Muussa tapauksessa None
        """

        return self._workout_repository.get_by_id(workout_id)

    def get_all_workout_summaries(self):
        """Palauttaa treenien tiivistelmät

        Returns:
            Palauttaa listan WorkoutSummary-olioita
        """

        return self._workout_repository.get_all_workout_summaries()

    def validate_set(self, set_entry):
        """Validoi sarjan sisällön

        Args:
            set_entry: Validoitava sarja SetEntry-oliona

        Returns:
            Palauttaa kirjaston, jossa avaimena on virheellinen syöte merkkijonoarvona
            ja arvona on virheviesti merkkijononarvona
        """

        errors = {}
        if not set_entry["movement"]:
            errors["movement"] = "No movement selected"
        try:
            weight = float(set_entry["weight"])
            if weight <= 0:
                errors["weight"] = "> 0"
        except ValueError:
            errors["weight"] = "> 0"
        try:
            reps = int(set_entry["reps"])
            if reps <= 0:
                errors["reps"] = "> 0"
        except ValueError:
            errors["reps"] = "> 0"
        try:
            rir = int(set_entry["rir"])
            if rir < -1:
                errors["rir"] = "≥ -1"
        except ValueError:
            errors["rir"] = "≥ -1"
        return errors

    def validate_workout(self, workout_metadata, sets):
        errors = {}
        if not self._is_valid_date(workout_metadata["date"]):
            errors["date"] = "Invalid"
        if len(sets) == 0:
            errors["general"] = "Workout must contain a set"
        return errors

    def _is_valid_date(self, date_str, fmt="%Y-%m-%d"):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_str):
            return False
        try:
            datetime.strptime(date_str, fmt)
            return True
        except ValueError:
            return False

    def update_workout(self, workout, pending_metadata, pending_sets):
        set_entires = [
            SetEntry(
                movement=s["movement"],
                reps=s["reps"],
                weight=s["weight"],
                rir=s["rir"]
            )
            for s in pending_sets
        ]
        updated_workout = Workout(
            workout_id=workout.id,
            title=pending_metadata["title"],
            date=pending_metadata["date"],
            notes=pending_metadata["notes"],
            duration=pending_metadata["duration"],
            sets=set_entires
        )
        return self._workout_repository.update(updated_workout)

    def delete_workout(self, workout):
        self._workout_repository.delete(workout)

workout_service = WorkoutService()
