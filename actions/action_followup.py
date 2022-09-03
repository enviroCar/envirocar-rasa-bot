from typing import Any, Text, Dict
from enums.custom_event_type import CustomEventType
from enums.navigation.navigation_screens import NavigationScreens

from model.action_model import ActionModel
from model.custom_event_model import CustomEventModel
from model.next_action import NextAction
from enums.recording.recording_requirements import RecordingRequirements

from rasa_sdk import Action, Tracker
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher

from enums.recording.bluetooth import Bluetooth
from enums.recording.car import Car
from enums.recording.gps import GPS
from model.response_model import ResponseModel


class ActionFollowup(Action):
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
        return "action_followup"

    @staticmethod
    def run(dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any], **kwargs):

        # get all slotss
        slots = tracker.slots

        print("slotss:", slots)

        recording_start_query = slots["recording_start_query"]
        recording_stop_query = slots["recording_stop_query"]
        location_permission = slots["location_permission"]
        is_dashboard_fragment = slots["is_dashboard_fragment"]
        gps = slots["gps"]
        car = slots["car"]
        bluetooth_permission = slots["bluetooth_permission"]
        bluetooth = slots["bluetooth"]
        obd_adapter = slots["obd_adapter"]

        # check if recording query is true
        if recording_start_query:
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
        # TODO reset only start recording slots, maybe a function `ResetStartRecordingSlots`
        return [AllSlotsReset()]


def navigate_dashboard_fragment(dispatcher: CollectingDispatcher) -> None:
    """
        Function to send response to navigate `Dashboard Fragment`.
    """
    response = ResponseModel(
        query="",
        reply="navigating to dashboard fragment",
        action=ActionModel(
            custom_event=CustomEventModel(
                type=CustomEventType.NavigationScreens.value,
                name=NavigationScreens.CAR_SELECTION.value
            ),
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
            custom_event=CustomEventModel(
                type=CustomEventType.RecordingRequirements.value,
                name=RecordingRequirements.LOCATION_PERMS.value
            ),
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
            custom_event=CustomEventModel(
                type=CustomEventType.RecordingRequirements.value,
                name=RecordingRequirements.GPS.value
            ),
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
            custom_event=CustomEventModel(
                type=CustomEventType.RecordingRequirements.value,
                name=RecordingRequirements.CAR.value
            ),
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
            custom_event=CustomEventModel(
                type=CustomEventType.RecordingRequirements.value,
                name=RecordingRequirements.BLUETOOTH_PERMS.value
            ),
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
            custom_event=CustomEventModel(
                type=CustomEventType.RecordingRequirements.value,
                name=RecordingRequirements.BLUETOOTH.value
            ),
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
            custom_event=CustomEventModel(
                type=CustomEventType.RecordingRequirements.value,
                name=RecordingRequirements.OBD.value
            ),
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
