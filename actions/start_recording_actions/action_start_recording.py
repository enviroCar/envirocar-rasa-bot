from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from enums.custom_event_type import CustomEventType
from enums.recording.OBD_adapter import OBDAdapter
from enums.recording.RecordingMode import RecordingMode
from enums.recording.RecordingState import RecordingState
from enums.recording.bluetooth import Bluetooth
from enums.recording.car import Car
from enums.recording.gps import GPS
from enums.recording.recording import Recording
from model.action_model import ActionModel
from model.custom_event_model import CustomEventModel
from model.next_action import NextAction
from model.response_model import ResponseModel
from utils.recording_utils.navigation_to_recording_screen import nav_to_recording_screen


class ActionStartRecording(Action):
    """This is the action that is called when the user says "start recording"."""

    @staticmethod
    def name(**kwargs) -> Text:
        return "action_start_recording"

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
        # if recording is already started then navigate to recording screen
        if metadata["recordingMetadata"]["recording_status"] == RecordingState.RECORDING_STOPPED.value:
            if metadata["isDashboardFragment"]:
                # if the user is on dashboard fragment, then check if recording is not currently going on
                if metadata["recordingMetadata"]["recording_status"] == RecordingState.RECORDING_STOPPED.value:
                    # check if the user has granted location permission
                    if metadata["recordingMetadata"]["has_location_permission"]:
                        # get variables from metadata
                        recording_mode = metadata["recordingMetadata"]["recording_mode"]
                        gps = metadata["recordingMetadata"]["gps"]
                        car = metadata["recordingMetadata"]["car"]
                        bluetooth = metadata["recordingMetadata"]["bluetooth"]
                        obd_adapter = metadata["recordingMetadata"]["obd_adapter"]

                        # validating recording requirements
                        if gps == GPS.OFF.value:
                            return_response(dispatcher, "GPS is not on! Do you want to turn it on?")
                            return [SlotSet("location_permission", True), SlotSet("is_dashboard_fragment", True),
                                    SlotSet("gps", False),
                                    SlotSet("recording_start_query", True)]

                        if car == Car.Not_Selected.value:
                            return_response(dispatcher, "Car is not selected! Do you want to select one?")
                            return [SlotSet("location_permission", True), SlotSet("is_dashboard_fragment", True),
                                    SlotSet("car", False), SlotSet("recording_start_query", True)]

                        # GPS MODE
                        if recording_mode == RecordingMode.GPS.value:
                            start_recording(
                                dispatcher, message, intent)
                            return [
                                SlotSet("location_permission", True),
                                SlotSet("is_dashboard_fragment", True),
                                SlotSet("gps", True),
                                SlotSet("car", True),
                                SlotSet("recording_start_query", False)
                            ]
                        else:
                            if metadata["recordingMetadata"]["has_bluetooth_permission"]:
                                if bluetooth == Bluetooth.ON.value:
                                    if obd_adapter == OBDAdapter.Selected.value:
                                        start_recording(
                                            dispatcher, message, intent)
                                        return [
                                            SlotSet(
                                                "location_permission", True),
                                            SlotSet(
                                                "is_dashboard_fragment", True),
                                            SlotSet("gps", True),
                                            SlotSet("car", True),
                                            SlotSet(
                                                "bluetooth_permission", True),
                                            SlotSet("bluetooth", True),
                                            SlotSet("obd_adapter", True),
                                            SlotSet(
                                                "recording_start_query", False)
                                        ]
                                    else:
                                        return_response(dispatcher,
                                                        "OBD Adapter is not selected! Do you want to select one?")
                                        return [
                                            SlotSet(
                                                "location_permission", True),
                                            SlotSet(
                                                "is_dashboard_fragment", True),
                                            SlotSet("gps", True),
                                            SlotSet("car", True),
                                            SlotSet(
                                                "bluetooth_permission", True),
                                            SlotSet("bluetooth", True),
                                            SlotSet("obd_adapter", False),
                                            SlotSet(
                                                "recording_start_query", True)
                                        ]
                                else:
                                    return_response(dispatcher, "Bluetooth is not on! Do you want to turn it on?")
                                    return [
                                        SlotSet("location_permission", True),
                                        SlotSet("is_dashboard_fragment", True),
                                        SlotSet("gps", True),
                                        SlotSet("car", True),
                                        SlotSet("bluetooth_permission", True),
                                        SlotSet("bluetooth", False),
                                        SlotSet("recording_start_query", True)
                                    ]
                            else:
                                return_response(dispatcher, "Bluetooth permission is not granted! Do you want to grant it?")
                                return [
                                    SlotSet("location_permission", True),
                                    SlotSet("is_dashboard_fragment", True),
                                    SlotSet("gps", True),
                                    SlotSet("car", True),
                                    SlotSet("bluetooth_permission", False),
                                    SlotSet("bluetooth", False),
                                    SlotSet("recording_start_query", True)
                                ]
                    else:
                        return_response(dispatcher, "Location permission is not granted! Do you want to grant it?")
                        return [
                            SlotSet("is_dashboard_fragment", True),
                            SlotSet("location_permission", False),
                            SlotSet("recording_start_query", True)
                        ]
                elif metadata["recordingMetadata"]["recording_status"] == RecordingState.RECORDING_RUNNING.value:
                    reply = "Recording is already running! Navigating to recording screen"
                    nav_to_recording_screen(dispatcher, message, reply,  intent)
                    return [SlotSet("recording_start_query", False)]
                elif metadata["recordingMetadata"]["recording_status"] == RecordingState.RECORDING_INIT.value:
                    dispatcher.utter_message(
                        text="Recording is starting, Please wait!")
                    return [SlotSet("recording_start_query", False)]
                else:
                    print(
                        f"{self.name()}: Wrong Recording state, Something went wrong!")
                    dispatcher.utter_message(
                        text="Wrong Recording state, Something went wrong!")
                    return [SlotSet("recording_start_query", False)]
            else:
                reply = "Recording is already running! Navigating to recording screen"
                nav_to_recording_screen(dispatcher, message, reply,  intent)
                return [SlotSet("recording_start_query", False)]
        else:
            print(f"{self.name()}: No Recording going on!")
            dispatcher.utter_message(
                text="There is currently no Recording going on")
            return []
        # else:
        #     print(f" {self.name()}: {metadata['type']} is not RECORDING")
        #     dispatcher.utter_message(
        #         text="Something went wrong! Please try again!")
        #     return [SlotSet("recording_start_query", False)]


def start_recording(dispatcher: CollectingDispatcher, message: str, intent: str) -> None:
    response = ResponseModel(
        query=message,
        reply="Sure, I will start recording",
        action=ActionModel(
            activity_class_name="org.envirocar.app.recording.RecordingService",
            custom_event=CustomEventModel(
                type=CustomEventType.Recording.value,
                name=Recording.START.value
            ).as_dict(),
            next_action=NextAction.STANDBY.value
        ),
        data={"intent": intent}
    )

    dispatcher.utter_message(json_message={
        "query": response.query,
        "reply": response.reply,
        "action": response.action.as_dict(),
        "data": response.data
    })


def return_response(dispatcher: CollectingDispatcher, reply: str):
    response = ResponseModel(
        query="query",
        reply=reply,
        action=ActionModel(
            next_action=NextAction.RECOGNITION.value
        ),
        data={}
    )

    dispatcher.utter_message(json_message={
        "query": response.query,
        "reply": response.reply,
        "action": response.action.as_dict(),
        "data": response.data
    })
