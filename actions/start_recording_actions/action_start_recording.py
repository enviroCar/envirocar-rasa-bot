import json
from typing import Any, Text, Dict, List

from model.recording_track.RecordingState import RecordingState
from model.recording_track.recording import Recording

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from model.action_model import ActionModel
from model.metadata_type import MetadataType
from model.recording_track.Bluetooth import Bluetooth
from model.recording_track.Car import Car
from model.recording_track.GPS import GPS
from model.recording_track.OBDAdapter import OBDAdapter
from model.recording_track.RecordingMode import RecordingMode
from model.response_model import ResponseModel


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

        # get metadata from the latest message
        metadata = tracker.latest_message.get("metadata")

        print("metadata", metadata)

        # if the metadata type is recording and user is on dashboard fragment,
        if metadata["type"] == MetadataType.RECORDING.value:
            if metadata["recordingMetadata"]["isDashboardFragment"]:
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
                        is_dashboard_fragment = metadata["recordingMetadata"]["isDashboardFragment"]

                        # validating recording requirements
                        if gps == GPS.OFF.value:
                            dispatcher.utter_message(
                                text="GPS is not on! Do you want to turn it on?")
                            return [SlotSet("location_permission", True), SlotSet("is_dashboard_fragment", True),
                                    SlotSet("gps", False),
                                    SlotSet("recording_query", True)]

                        if car == Car.Not_Selected.value:
                            dispatcher.utter_message(
                                text="Car is not selected! Do you want to select one?")
                            return [SlotSet("location_permission", True), SlotSet("is_dashboard_fragment", True),
                                    SlotSet("car", False), SlotSet("recording_query", True)]

                        # GPS MODE
                        if recording_mode == RecordingMode.GPS.value:
                            start_recording(dispatcher, message, intent, entities)
                            return [
                                SlotSet("location_permission", True),
                                SlotSet("is_dashboard_fragment", True),
                                SlotSet("gps", True),
                                SlotSet("car", True),
                                SlotSet("recording_query", False)
                            ]
                        else:
                            if metadata["recordingMetadata"]["has_bluetooth_permission"]:
                                if bluetooth == Bluetooth.ON.value:
                                    if obd_adapter == OBDAdapter.Selected.value:
                                        start_recording(dispatcher, message, intent, entities)
                                        return [
                                            SlotSet("location_permission", True),
                                            SlotSet("is_dashboard_fragment", True),
                                            SlotSet("gps", True),
                                            SlotSet("car", True),
                                            SlotSet("bluetooth_permission", True),
                                            SlotSet("bluetooth", True),
                                            SlotSet("obd_adapter", True),
                                            SlotSet("recording_query", False)
                                        ]
                                    else:
                                        dispatcher.utter_message(
                                            text="OBD Adapter is not selected! Do you want to select one?")
                                        return [
                                            SlotSet("location_permission", True),
                                            SlotSet("is_dashboard_fragment", True),
                                            SlotSet("gps", True),
                                            SlotSet("car", True),
                                            SlotSet("bluetooth_permission", True),
                                            SlotSet("bluetooth", True),
                                            SlotSet("obd_adapter", False),
                                            SlotSet("recording_query", True)
                                        ]
                                else:
                                    dispatcher.utter_message(
                                        text="Bluetooth is not on! Do you want to turn it on?")
                                    return [
                                        SlotSet("location_permission", True),
                                        SlotSet("is_dashboard_fragment", True),
                                        SlotSet("gps", True),
                                        SlotSet("car", True),
                                        SlotSet("bluetooth_permission", True),
                                        SlotSet("bluetooth", False),
                                        SlotSet("recording_query", True)
                                    ]
                            else:
                                dispatcher.utter_message(
                                    text="Bluetooth permission is not granted! Do you want to grant it?")
                                return [
                                    SlotSet("location_permission", True),
                                    SlotSet("is_dashboard_fragment", True),
                                    SlotSet("gps", True),
                                    SlotSet("car", True),
                                    SlotSet("bluetooth_permission", False),
                                    SlotSet("bluetooth", False),
                                    SlotSet("recording_query", True)
                                ]
                    else:
                        dispatcher.utter_message(
                            text="Location permission is not granted! Do you want to grant it?")
                        return [
                            SlotSet("is_dashboard_fragment", True),
                            SlotSet("location_permission", False),
                            SlotSet("recording_query", True)
                        ]
                elif metadata["recordingMetadata"]["recording_status"] == RecordingState.RECORDING_RUNNING.value:
                    dispatcher.utter_message(
                        text="Recording is already started!")
                    return [SlotSet("recording_query", False)]
                elif metadata["recordingMetadata"]["recording_status"] == RecordingState.RECORDING_INIT.value:
                    dispatcher.utter_message(
                        text="Recording is starting, Please wait!")
                    return [SlotSet("recording_query", False)]
                else:
                    dispatcher.utter_message(
                        text="Wrong Recording state, Something went wrong!")
                    return [SlotSet("recording_query", False)]

                    # dispatcher.utter_message(
                    #     text="Recording is already started! Navigating to recording screen(if not already there)")
                    # return [SlotSet("recording_query", True)]

                    # dispatcher.utter_message(
                    #     text="Recording is already started! Do you want to stop it?")
                    # return [SlotSet("recording_query", True)]
            else:
                dispatcher.utter_message(
                    text="You are not on dashboard fragment! Do you want to go to dashboard fragment?")
                return [SlotSet("is_dashboard_fragment", False), SlotSet("recording_query", True)]
        else:
            dispatcher.utter_message(
                text="Something went wrong! Please try again!")
            return [SlotSet("recording_query", False)]


def start_recording(dispatcher: CollectingDispatcher, message: str, intent: str, entities: json) -> None:
    response = ResponseModel(
        query=message,
        reply="Sure, I will start recording",
        action=ActionModel(
            activity_class_name="org.envirocar.app.recording.RecordingService",
            custom_event=Recording.START.value
        ),
        data={
            "intent": intent,
            "entity": entities[0]['entity']
        }
    )

    dispatcher.utter_message(json_message={
        "query": response.query,
        "reply": response.reply,
        "action": response.action.as_dict(),
        "data": response.data
    })
