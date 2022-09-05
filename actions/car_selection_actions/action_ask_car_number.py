from typing import Dict, Text, List

from rasa_sdk import Tracker
from rasa_sdk.events import EventType, ActiveLoop, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action

from enums.recording.metadata_type import MetadataType
from utils.car_utils.CarUtils import CarUtils
from utils.car_utils.navigation_to_screen import nav_to_car_selection_screen


class ActionAskCarNumber(Action):
    """This is the action that is called when the form `car_selection_form` starts."""

    @staticmethod
    def name(**kwargs) -> Text:
        return "action_ask_car_number"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
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

        # if the metadata type is car selection
        # if metadata["type"] == MetadataType.CAR_SELECTION.value:

        # check if intent is `select_car` to avoid any NLP errors
        # TODO: if the form is on and intent is `select_car`, then directly go for next steps!
        if intent == "select_car":
            if metadata["isDashboardFragment"] and \
                    not metadata["car_selection_metadata"]["is_car_selection_fragment"]:
                # if the user is on dashboard fragment, then navigate them to car selection screen
                nav_to_car_selection_screen(
                    dispatcher, message, intent, entities)
                return [ActiveLoop(None), SlotSet('car_number', None)]
            elif metadata["car_selection_metadata"]["is_car_selection_fragment"]:
                    # if the user is on car selection screen, start the form
                    select_car_iteration = tracker.get_slot("select_car_iteration")

                    cars = metadata["car_selection_metadata"]["cars"]

                    car_utils = CarUtils()
                    car_index = car_utils.get_car_index(select_car_iteration)

                    available_car_status = car_utils.get_available_car_status(
                        cars, car_index)
                    response = car_utils.return_response(
                        available_car_status["message"])
                    dispatcher.utter_message(json_message={
                        "query": response.query,
                        "reply": response.reply,
                        "action": response.action.as_dict(),
                        "data": response.data
                    })
        # else:
            # return a message and deactive the form
            # print(f"{self.name()}: {metadata['type']} is not CAR_SELECTION")
            # dispatcher.utter_message(
            #     text="Something went wrong! Please try again!")
            # return [ActiveLoop(None), SlotSet('car_number', None)]
        # else:
        #     # return a message and deactive the form
        #     print(f"{self.name()}: {metadata['type']} is not CAR_SELECTION")
        #     dispatcher.utter_message(text="Something went wrong! Please try again!")
        #     return [ActiveLoop(None), SlotSet('car_number', None)]
        return []
