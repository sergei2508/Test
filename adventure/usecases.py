from __future__ import annotations
from adventure import models
from .notifiers import Notifier
from .repositories import JourneyRepository


class StartJourney:
    def __init__(self, repository: JourneyRepository, notifier: Notifier):
        self.repository = repository
        self.notifier = notifier

    def set_params(self, data: dict) -> StartJourney:
        self.data = data
        return self

    def execute(self) -> None:
        car = self.repository.get_or_create_car()
        vehicle = self.repository.create_vehicle(vehicle_type=car, **self.data)
        if not vehicle.can_start():
            raise StartJourney.CantStart("vehicle can't start")

        journey = self.repository.create_journey(vehicle)
        self.notifier.send_notifications(journey)
        return journey

    class CantStart(Exception):
        pass

class StopJourney:
    def __init__(self, repository: JourneyRepository, notifier: Notifier, journey: models.Journey):
        self.repository = repository
        self.journey = journey
        
    def set_params(self, data: dict) -> StopJourney:
        self.data = data
        return self

    def execute(self) -> None:
        if self.journey.start:
            self.repository.stop_journey(self.journey, self.data['date'])
        else:
            raise StopJourney.CantStop("cant stop")

    class CantStop(Exception):
        pass