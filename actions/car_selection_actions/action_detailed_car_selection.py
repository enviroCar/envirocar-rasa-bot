from typing import Any, Dict, Text, List

from rasa_sdk import Action
from rasa_sdk import Tracker
from rasa_sdk.events import FollowupAction, ActiveLoop
from rasa_sdk.executor import CollectingDispatcher

from utils.car_utils.CarUtils import CarUtils


class ActionDetailedCarSelection(Action):
    """This is the action that is called when the intent says "action_detailed_car_selection" is extracted."""

    @staticmethod
    def name(**kwargs) -> Text:
        return "action_detailed_car_selection"

    @staticmethod
    def run(dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any], **kwargs) -> List[
        Dict[Text, Any]
    ]:
        active_loop = None
        try:
            active_loop = tracker.active_loop.get('name')
        except KeyError:
            print(f"No active loop, error:{Exception}")

        # check if `car_selection_form` is not active, if not then run it.
        if active_loop != "car_selection_form":
            message = tracker.latest_message.get("text")
            intent = None
            entities = None
            try:
                intent = tracker.latest_message['intent'].get('name')
            except KeyError:
                print(f"No intent, something went wrong, error:{Exception}")
            try:
                entities = tracker.latest_message['entities']
            except KeyError:
                print(f"No entity, something went wrong, error:{Exception}")

            metadata = tracker.latest_message.get("metadata")
            CarUtils.ask_car_number(
                metadata=metadata, dispatcher=dispatcher, tracker=tracker,
                message=message, intent=intent, entities=entities)
            return [FollowupAction("car_selection_form"), ActiveLoop("car_selection_form")]

        return []
