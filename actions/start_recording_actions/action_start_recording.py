from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from model.action_model import ActionModel
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

        # get all slots
        recording_mode = tracker.get_slot("recording_mode")
        gps = tracker.get_slot("gps")
        car = tracker.get_slot("car")
        bluetooth = tracker.get_slot("bluetooth")
        obd_adapter = tracker.get_slot("bluetooth")

        # GPS MODE
        if gps == GPS.ON.value and recording_mode == RecordingMode.GPS.value \
                and car == Car.Selected.value:
            start_recording(dispatcher, message)
            return [SlotSet("recording_mode", None), SlotSet("gps", None), SlotSet("car", None),
                    SlotSet("bluetooth", None), SlotSet("obd_adapter", None), SlotSet("requested_slot", None)]
        # OBD MODE
        elif gps == GPS.ON.value and recording_mode == RecordingMode.OBD.value \
                and car == Car.Selected.value and bluetooth == Bluetooth.ON.value \
                and obd_adapter == OBDAdapter.Selected.value:
            start_recording(dispatcher, message)
            return [SlotSet("recording_mode", None), SlotSet("gps", None), SlotSet("car", None),
                    SlotSet("bluetooth", None), SlotSet("obd_adapter", None), SlotSet("requested_slot", None)]
        else:
            return []


def start_recording(dispatcher: CollectingDispatcher, message: str):
    response = ResponseModel(
        query=message,
        reply="sure start I will.",
        action=ActionModel(
            activity_class_name="org.envirocar.app.recording.RecordingService",
        ),
        data={
            # "intent": intent,
            # "entity": entities[0]['entity']
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
