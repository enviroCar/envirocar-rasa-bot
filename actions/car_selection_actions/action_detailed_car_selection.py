from typing import Dict, Text, List

from rasa.shared.core.events import ActiveLoop
from rasa_sdk import Tracker
from rasa_sdk.events import EventType, FollowupAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action


class ActionDetailedCarSelection(Action):
    """This is the action that is called when the intent says "action_detailed_car_selection" is extracted."""

    @staticmethod
    def name(**kwargs) -> Text:
        return "action_detailed_car_selection"

    @staticmethod
    def run(dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict, **kwargs) -> List[EventType]:
        active_loop = None
        try:
            active_loop = tracker.active_loop.get('name')
        except KeyError:
            print(f"No active loop, error:{Exception}")

        # check if `car_selection_form` is not active, if not then run it.
        if active_loop != "car_selection_form":
            return [FollowupAction("car_selection_form"), ActiveLoop("car_selection_form")]

        return []
