import random
from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionCurrentCar(Action):
    def name(self) -> Text:
        return "action_current_car"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # get the currently selected car from tracker
        current_car = tracker.get_slot("selected_car")

        # generate a response to inform the user about the currently selected car
        if current_car is not None:
            message = f"Your current car is '{current_car}'."
        else:
            message = "You haven't selected a car yet."

        # send the message to the user
        dispatcher.utter_message(message)

        return []
