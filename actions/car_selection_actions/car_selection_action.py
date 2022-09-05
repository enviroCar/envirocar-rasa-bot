import json
from typing import Any, Text, Dict, List
from enums.custom_event_type import CustomEventType
from model.custom_event_model import CustomEventModel

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, ActiveLoop
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

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any], **kwargs) -> List[
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
        # if metadata["type"] == MetadataType.CAR_SELECTION.value:
        if metadata["isDashboardFragment"] and not metadata["car_selection_metadata"]["is_car_selection_fragment"]:
            # if the user is on dashboard fragment, then navigate them to car selection screen
            nav_to_car_selection_screen(dispatcher, message, intent, entities)
        elif metadata["car_selection_metadata"]["is_car_selection_fragment"]:
            # if the user is on car selection screen, select the car
            self.select_car(dispatcher, metadata, car_name, message, intent)
            return [ActiveLoop(None), SlotSet('car_number', None)]
        else:
            print(f"{self.name()}: user is not on dashboard and also not on car selection screen... ")
            dispatcher.utter_message(text="Something went wrong! Please try again!")
            return [ActiveLoop(None), SlotSet('car_number', None)]
    # else:
        #     print(f" {self.name()}: {metadata['type']} is not CAR_SELECTION")
        #     dispatcher.utter_message(text="Something went wrong! Please try again!")
        return [SlotSet("car_name", None)]

    def select_car(self, dispatcher: CollectingDispatcher, metadata, car_name: str, message: str, intent: str):
        cars = metadata["car_selection_metadata"]["cars"]
        if car_name in cars:
            response = ResponseModel(
                query=message, reply=f"Okay, selecting {car_name}",
                action=ActionModel(
                    activity_class_name="org.envirocar.app.views.carselection.CarSelectionActivity",
                    custom_event=CustomEventModel(
                        type=CustomEventType.CarSelection.value,
                        name=CarSelection.SELECT.value
                    ).as_dict(),
                    next_action=NextAction.STANDBY.value
                ),
                data={"intent": intent, "car_name": car_name}
            )
            dispatcher.utter_message(
                json_message={"query": response.query, "reply": response.reply, "action": response.action.as_dict(),
                              "data": response.data}
            )
        print(f"{self.name()} {car_name} not found in the car list")
        dispatcher.utter_message(text=f"{car_name} not found in the list,  Something went wrong! Please try again!")

