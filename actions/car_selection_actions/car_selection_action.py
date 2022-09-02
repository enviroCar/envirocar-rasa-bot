import json
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from enums.car_selection.car_selection import CarSelection
from enums.recording.metadata_type import MetadataType
from model.action_model import ActionModel
from model.next_action import NextAction
from model.response_model import ResponseModel
from utils.car_utils.navigation_to_screen import nav_to_car_selection_screen


class ActionCarSelection(Action):
    """This is the action that is called when the user says "start recording"."""

    def name(self) -> Text:
        return "action_car_selection"

    @staticmethod
    def run(dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any], **kwargs) -> List[
        Dict[Text, Any]
    ]:

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

        # get metadata from the latest message
        metadata = tracker.latest_message.get("metadata")

        # get the `car_name` slot value
        car_name = tracker.get_slot("car_name")
        # if the metadata type is car selection
        if metadata["type"] == MetadataType.CAR_SELECTION.value:
            if metadata["isDashboardFragment"] and not metadata["car_selection_metadata"]["is_car_selection_fragment"]:
                # if the user is on dashboard fragment, then navigate them to car selection screen
                nav_to_car_selection_screen(dispatcher, message, intent, entities)
            elif metadata["car_selection_metadata"]["is_car_selection_fragment"]:
                # if the user is on car selection screen, select the car
                select_car(dispatcher, metadata, car_name, message, intent, entities)
            else:
                dispatcher.utter_message(text="Something went wrong! Please try again!")
        else:
            dispatcher.utter_message(text="Something went wrong! Please try again!")
        return [SlotSet("car_name", None)]


def select_car(dispatcher: CollectingDispatcher, metadata, car_name: str, message: str, intent: str,
               entities: json) -> None:
    cars = metadata["car_selection_metadata"]["cars"]
    if car_name in cars:
        response = ResponseModel(
            query=message, reply=f"Okay, selecting {car_name}",
            action=ActionModel(
                activity_class_name="org.envirocar.app.views.carselection.CarSelectionActivity",
                custom_event=CarSelection.SELECT.value,
                next_action=NextAction.STANDBY.value
            ),
            data={"intent": intent, "entity": entities[0]['entity'], "car_name": car_name}
        )
        dispatcher.utter_message(
            json_message={"query": response.query, "reply": response.reply, "action": response.action.as_dict(),
                          "data": response.data}
        )
    else:
        dispatcher.utter_message(text="Something went wrong! Please try again!")
