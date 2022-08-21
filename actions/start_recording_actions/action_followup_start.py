from typing import Any, Text, Dict, List
from model.recording_track.recording_requirements import RecordingRequirements

from rasa_sdk import Action, Tracker
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher

from model.recording_track.Bluetooth import Bluetooth
from model.recording_track.Car import Car
from model.recording_track.GPS import GPS
from model.recording_track.RecordingStatus import RecordingStatus


class ActionFollowupStart(Action):
    """
        This is the action that is called when the user affirms to start something.
        1. happy path
            e.g. Bot: GPS is not on! Do you want to turn it on?
                User: Yes
        2. Unhappy path
            e.g. User: Yes (without any previous message/without in the context of recording)
                Bot: (NO response for now, later will be handled by similar great/okay response)
    """

    @staticmethod
    def name(**kwargs) -> Text:
        return "action_followup_start"

    @staticmethod
    def run(dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any], **kwargs):
        # get all slots
        recording_status = tracker.get_slot("recording_status")
        is_dashboard_fragment = tracker.get_slot("is_dashboard_fragment")
        gps = tracker.get_slot("gps")
        car = tracker.get_slot("car")
        bluetooth = tracker.get_slot("bluetooth")
        obd_adapter = tracker.get_slot("bluetooth")

        print("slots:", recording_status, gps, car, bluetooth, obd_adapter)

        if recording_status == RecordingStatus.GOING_ON.value:
            if gps == GPS.OFF.value:
                turn_on_gps(dispatcher)
            elif car == Car.Not_Selected.value:
                select_car(dispatcher)
            elif bluetooth == Bluetooth.OFF.value:
                turn_on_bluetooth(dispatcher)
            else:
                select_obd_adapter(dispatcher)

        return [AllSlotsReset()]


def turn_on_gps(dispatcher: CollectingDispatcher) -> None:
    """
        Function to send response to turn on GPS.
    """
    dispatcher.utter_message(
        response="utter_custom_response",
        query="",
        reply="gps",
        action={
            "customEvent": RecordingRequirements.GPS.value,
            "activity_class_name": "",
            "activity_extras": ""
        },
        data="",
    )


def select_car(dispatcher: CollectingDispatcher) -> None:
    """
        Function to send response to Select car.
    """
    dispatcher.utter_message(
        response="utter_custom_response",
        query="",
        reply="car",
        action={
            "customEvent": RecordingRequirements.CAR.value,
            "activity_class_name": "",
            "activity_extras": ""
        },
        data="",
    )


def turn_on_bluetooth(dispatcher: CollectingDispatcher) -> None:
    """
        Function to send response to turn on Bluetooth.
    """
    dispatcher.utter_message(
        response="utter_custom_response",
        query="",
        reply="bluetooth",
        action={
            "customEvent": RecordingRequirements.BLUETOOTH.value,
            "activity_class_name": "",
            "activity_extras": ""
        },
        data="",
    )


def select_obd_adapter(dispatcher: CollectingDispatcher) -> None:
    """
        Function to send response to Select OBD Adapter.
    """
    dispatcher.utter_message(
        response="utter_custom_response",
        query="",
        reply="OBD Adapter",
        action={
            "customEvent": RecordingRequirements.OBD.value,
            "activity_class_name": "",
            "activity_extras": ""
        },
        data="",
    )
