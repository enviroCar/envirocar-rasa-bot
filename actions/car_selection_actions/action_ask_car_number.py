from typing import Dict, Text, List

from rasa_sdk import Tracker
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action

from utils.car_utils.CarUtils import CarUtils


class ActionAskCarNumber(Action):
    """This is the action that is called when the form `car_selection_form` starts."""

    @staticmethod
    def name(**kwargs) -> Text:
        return "action_ask_car_number"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        metadata = tracker.latest_message.get("metadata")
        intent = None
        try:
            intent = tracker.latest_message['intent'].get('name')
        except KeyError:
            print(f"No intent, something went wrong, error:{Exception}")

        # check if intent is `select_car` to avoid any NLP errors
        if intent == "select_car":
            select_car_iteration = tracker.get_slot("select_car_iteration")

            cars = metadata["car_selection_metadata"]["cars"]

            car_utils = CarUtils()
            car_index = car_utils.get_car_index(select_car_iteration)

            available_car_status = car_utils.get_available_car_status(cars, car_index)
            dispatcher.utter_message(text=available_car_status["message"])
            return []
