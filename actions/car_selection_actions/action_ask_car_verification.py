from typing import Dict, Text, List

from rasa_sdk import Tracker
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action

from model.action_model import ActionModel
from model.next_action import NextAction
from model.response_model import ResponseModel


class ActionAskCarNumber(Action):
    """This is the action that is called when the form `car_selection_form` starts."""

    @staticmethod
    def name(**kwargs) -> Text:
        return "action_ask_car_verification"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        # get the `car_name` slot value
        car_name = tracker.get_slot("car_name")

        response = self.return_response(f"Do you want to select {car_name}?")
        dispatcher.utter_message(json_message={
            "query": response.query,
            "reply": response.reply,
            "action": response.action.as_dict(),
            "data": response.data
        })
        return []

    @staticmethod
    def return_response(reply: str):
        response = ResponseModel(
            query="",
            reply=reply,
            action=ActionModel(
                next_action=NextAction.RECOGNITION.value
            ),
            data={}
        )
        return response

