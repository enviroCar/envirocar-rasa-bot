from typing import Any, Text, Dict

from model.action_model import ActionModel
from model.next_action import NextAction
from enums.recording.recording_requirements import RecordingRequirements

from rasa_sdk import Action, Tracker
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher

from enums.recording.bluetooth import Bluetooth
from enums.recording.car import Car
from enums.recording.gps import GPS
from model.response_model import ResponseModel


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
        recording_query = tracker.get_slot("recording_query")
        location_permission = tracker.get_slot("location_permission")
        is_dashboard_fragment = tracker.get_slot("is_dashboard_fragment")
        gps = tracker.get_slot("gps")
        car = tracker.get_slot("car")
        bluetooth_permission = tracker.get_slot("bluetooth_permission")
        bluetooth = tracker.get_slot("bluetooth")
        obd_adapter = tracker.get_slot("bluetooth")

        print("slots:", recording_query, is_dashboard_fragment,
              location_permission, gps, car, bluetooth, obd_adapter)

        # check if recording query is true
        if recording_query:
            # if not is_dashboard_fragment:
            #     navigate_dashboard_fragment(dispatcher)
            if not location_permission:
                grant_location_permission(dispatcher)
            elif gps == GPS.OFF.value:
                turn_on_gps(dispatcher)
            elif car == Car.Not_Selected.value:
                select_car(dispatcher)
            elif not bluetooth_permission:
                grant_bluetooth_permission(dispatcher)
            elif bluetooth == Bluetooth.OFF.value:
                turn_on_bluetooth(dispatcher)
            else:
                select_obd_adapter(dispatcher)

        return [AllSlotsReset()]


def navigate_dashboard_fragment(dispatcher: CollectingDispatcher) -> None:
    """
        Function to send response to navigate `Dashboard Fragment`.
    """
    response = ResponseModel(
        query="",
        reply="navigating to dashboard fragment",
        action=ActionModel(
            custom_event=RecordingRequirements.DASHBOARD.value,
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


def grant_location_permission(dispatcher: CollectingDispatcher) -> None:
    """
        Function to send response to grant location permissions.
    """
    response = ResponseModel(
        query="",
        reply="Please grant location permission",
        action=ActionModel(
            custom_event=RecordingRequirements.LOCATION_PERMS.value,
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


def turn_on_gps(dispatcher: CollectingDispatcher) -> None:
    """
        Function to send response to turn on GPS.
    """
    response = ResponseModel(
        query="",
        reply="Please turn on GPS",
        action=ActionModel(
            custom_event=RecordingRequirements.GPS.value,
            next_action=NextAction.RECOGNITION.value),
        data={}
    )
    dispatcher.utter_message(json_message={
        "query": response.query,
        "reply": response.reply,
        "action": response.action.as_dict(),
        "data": response.data
    })


def select_car(dispatcher: CollectingDispatcher) -> None:
    """
        Function to send response to Select car.
    """
    response = ResponseModel(
        query="",
        reply="Please Select Car",
        action=ActionModel(
            custom_event=RecordingRequirements.CAR.value,
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


def grant_bluetooth_permission(dispatcher: CollectingDispatcher) -> None:
    """
        Function to send response to grant bluetooth permissions.
    """
    response = ResponseModel(
        query="",
        reply="Please grant Bluetooth permissions",
        action=ActionModel(
            custom_event=RecordingRequirements.BLUETOOTH_PERMS.value,
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


def turn_on_bluetooth(dispatcher: CollectingDispatcher) -> None:
    """
        Function to send response to turn on Bluetooth.
    """
    response = ResponseModel(
        query="",
        reply="Please turn on Bluetooth",
        action=ActionModel(
            custom_event=RecordingRequirements.BLUETOOTH.value,
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


def select_obd_adapter(dispatcher: CollectingDispatcher) -> None:
    """
        Function to send response to Select OBD Adapter.
    """
    response = ResponseModel(
        query="",
        reply="Please select OBD Devices",
        action=ActionModel(
            custom_event=RecordingRequirements.OBD.value,
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
