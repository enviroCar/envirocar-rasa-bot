from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from actions.start_recording_actions.checkGPS import checkGPS
from model.action_model import ActionModel
from model.response_model import ResponseModel

from rasa_sdk.events import FollowupAction


class ActionStartRecording(Action):
    """This is the action that is called when the user says "start recording"."""

    @staticmethod
    def name(**kwargs) -> Text:
        return "action_start_recording"

    @staticmethod
    def run(dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any], **kwargs) -> List[
        Dict[Text, Any]
    ]:
        message = tracker.latest_message.get("text")
        intent = tracker.latest_message['intent'].get('name')
        entities = tracker.latest_message['entities']

        response = ResponseModel(
            query=message,
            reply="sure start I will.",
            action=ActionModel(
                activity_class_name="org.envirocar.app.recording.RecordingService",
            ),
            data={
                "intent": intent,
                "entity": entities[0]['entity']
            }
        )

        if checkGPS:
            if

        dispatcher.utter_message(
            response="utter_custom_response",
            query=response.query,
            reply=response.reply,
            action={
                "activity_class_name": response.action.activity_class_name,
                "activity_extras": response.action.activity_extras
            },
            data=response.data,
        )

        FollowupAction("action_stop_recording")

        return []
