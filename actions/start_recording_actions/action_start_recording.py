model/recording_track/RecordingMetadata.pyimport json
from typing import Any, Text, Dict, List

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

        if metadata["type"] == MetadataType.RECORDING.value:
            # get variables from metadata
            recording_mode = metadata["recordingMetadata"]["recording_mode"]
            gps = metadata["recordingMetadata"]["gps"]
            car = metadata["recordingMetadata"]["car"]
            bluetooth = metadata["recordingMetadata"]["bluetooth"]
            obd_adapter = metadata["recordingMetadata"]["obd_adapter"]

            # validating common data
            if gps == GPS.OFF.value:
                dispatcher.utter_message(text="GPS is not on! Do you want to turn it on?")
                return [SlotSet("gps", False), SlotSet("recording_status", True)]

            if car == Car.Not_Selected.value:
                dispatcher.utter_message(text="Car is not selected! Do you want to select one?")
                return [SlotSet("car", False), SlotSet("recording_status", True)]

            # GPS MODE
            if recording_mode == RecordingMode.GPS.value:
                start_recording(dispatcher, message, intent, entities)
                return [SlotSet("gps", True), SlotSet("car", True)]
            else:
                if bluetooth == Bluetooth.ON.value:
                    if obd_adapter == OBDAdapter.Selected.value:
                        start_recording(dispatcher, message, intent, entities)
                        return [
                            SlotSet("gps", True),
                            SlotSet("car", True),
                            SlotSet("bluetooth", True),
                            SlotSet("obd_adapter", True)
                        ]
                    else:
                        dispatcher.utter_message(text="OBD Adapter is not selected! Do you want to select one?")
                        return [
                            SlotSet("gps", True),
                            SlotSet("car", True),
                            SlotSet("bluetooth", True),
                            SlotSet("obd_adapter", False),
                            SlotSet("recording_status", True)
                        ]
                else:
                    dispatcher.utter_message(text="Bluetooth is not on! Do you want to turn it on?")
                    return [
                        SlotSet("gps", True),
                        SlotSet("car", True),
                        SlotSet("bluetooth", False),
                        SlotSet("recording_status", True)
                    ]
        return []


def start_recording(dispatcher: CollectingDispatcher, message: str, intent: str, entities: json) -> None:
    response = ResponseModel(
        query=message,
        reply="Sure, I will start recording",
        action=ActionModel(
            activity_class_name="org.envirocar.app.recording.RecordingService",
        ),
        data={
            "intent": intent,
            "entity": entities[0]['entity']
        }
    )

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
