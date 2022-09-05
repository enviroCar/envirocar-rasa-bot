import json
from typing import Any, Text, Dict, List
from enums.custom_event_type import CustomEventType
from model.custom_event_model import CustomEventModel

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from enums.recording.RecordingState import RecordingState
from enums.recording.metadata_type import MetadataType
from enums.recording.recording import Recording
from model.action_model import ActionModel
from model.next_action import NextAction
from model.response_model import ResponseModel


class ActionStopRecording(Action):
    """This is the action that is called when the user says "stop recording"."""

    @staticmethod
    def name(**kwargs) -> Text:
        return "action_stop_recording"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any], **kwargs) -> List[
        Dict[Text, Any]
    ]:
        message = tracker.latest_message.get("text")
        intent = tracker.latest_message['intent'].get('name')
        entities = tracker.latest_message['entities']

        # get metadata from the latest message
        metadata = tracker.latest_message.get("metadata")

        print("metadata", metadata)

        # if the metadata type is recording and user is on dashboard fragment,
        # TODO - get an object for all required start recording slots
        # if metadata["type"] == MetadataType.RECORDING.value:
        if metadata["recordingMetadata"]["isDashboardFragment"]:
            # if the user is on dashboard fragment, then check if recording is currently going on
            if metadata["recordingMetadata"]["recording_status"] == RecordingState.RECORDING_RUNNING.value:
                # if recording is currently going on, then stop the recording
                stop_recording(dispatcher, message, intent, entities)
                return [SlotSet("is_dashboard_fragment", True)]

            elif metadata["recordingMetadata"]["recording_status"] == RecordingState.RECORDING_STOPPED.value:
                dispatcher.utter_message(
                    text="There is currently no Recording going on")
                return [SlotSet("recording_stop_query", False)]
            elif metadata["recordingMetadata"]["recording_status"] == RecordingState.RECORDING_INIT.value:
                dispatcher.utter_message(
                    text="There is currently no Recording going on")
                return [SlotSet("recording_stop_query", False)]
            else:
                print(f"{self.name()}: Wrong recording state other than init, running or stopped")
                dispatcher.utter_message(
                    text="Wrong Recording state, Something went wrong!")
                return [SlotSet("recording_stop_query", False)]
        else:
            dispatcher.utter_message(
                text="You are not on dashboard fragment! Please go to dashboard fragment to start recording.")
            return [SlotSet("is_dashboard_fragment", False), SlotSet("recording_stop_query", True)]
        
        dispatcher.utter_message(
                text="Something went wrong! Please try again!")
        return [SlotSet("recording_stop_query", False)]


def stop_recording(dispatcher: CollectingDispatcher, message: str, intent: str, entities: json) -> None:
    response = ResponseModel(
        query=message,
        reply="Sure, I will stop recording",
        action=ActionModel(
            activity_class_name="org.envirocar.app.recording.RecordingService",
            custom_event=CustomEventModel(
                type=CustomEventType.Recording.value,
                name=Recording.STOP.value
            ).as_dict(),
            next_action=NextAction.STANDBY.value
        ),
        data={
            "intent": intent,
        }
    )

    dispatcher.utter_message(json_message={
        "query": response.query,
        "reply": response.reply,
        "action": response.action.as_dict(),
        "data": response.data
    })
