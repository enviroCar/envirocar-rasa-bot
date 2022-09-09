from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from enums.custom_event_type import CustomEventType
from enums.recording.RecordingState import RecordingState
from enums.recording.recording import Recording
from model.action_model import ActionModel
from model.custom_event_model import CustomEventModel
from model.next_action import NextAction
from model.response_model import ResponseModel
from utils.recording_utils.navigation_to_recording_screen import nav_to_recording_screen


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

        # get metadata from the latest message
        metadata = tracker.latest_message.get("metadata")

        print("metadata", metadata)

        # if the metadata type is recording and user is on dashboard fragment,
        # TODO - get an object for all required start recording slots
        # if metadata["type"] == MetadataType.RECORDING.value:
        if metadata["recordingMetadata"]["is_recording_screen"] and not metadata["isDashboardFragment"]:
            # if the user is on recording screen, then check if recording is currently going on
            if metadata["recordingMetadata"]["recording_status"] == RecordingState.RECORDING_RUNNING.value:
                # if recording is currently going on, then stop the recording
                stop_recording(dispatcher, message, intent)
                return []

            elif metadata["recordingMetadata"]["recording_status"] == RecordingState.RECORDING_STOPPED.value:
                dispatcher.utter_message(
                    text="There is currently no Recording going on")
                return []
            elif metadata["recordingMetadata"]["recording_status"] == RecordingState.RECORDING_INIT.value:
                dispatcher.utter_message(
                    text="There is currently no Recording going on")
                return []
            else:
                print(f"{self.name()}: Wrong recording state other than init, running or stopped")
                dispatcher.utter_message(
                    text="Wrong Recording state, Something went wrong!")
                return []
        else:
            nav_to_recording_screen(dispatcher, message, intent)
            stop_recording(dispatcher, message, intent)
            return []


def stop_recording(dispatcher: CollectingDispatcher, message: str, intent: str) -> None:
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
