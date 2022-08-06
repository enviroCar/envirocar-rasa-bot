from typing import Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher


class ActionAskRecordingMode(Action):
    """This is the action that is called when the user says "start recording"."""

    @staticmethod
    def name(**kwargs) -> Text:
        return "action_ask_recording_mode"

    async def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        dispatcher.utter_message(
            text="checking the recording mode"
        )

        return []


class ActionAskGPS(Action):
    """This is the action that is called when slot `recording_mode` is filled."""

    @staticmethod
    def name(**kwargs) -> Text:
        return "action_ask_gps"

    async def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        dispatcher.utter_message(
            text="checking if gps is on..."
        )

        return []


class ActionAskCar(Action):
    """This is the action that is called when slot `gps` is filled."""

    @staticmethod
    def name(**kwargs) -> Text:
        return "action_ask_car"

    async def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        dispatcher.utter_message(
            text="checking if car is selected"
        )

        return []


class ActionAskBluetooth(Action):
    """This is the action that is called when slot `car` is filled."""

    @staticmethod
    def name(**kwargs) -> Text:
        return "action_ask_bluetooth"

    async def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        dispatcher.utter_message(
            text="checking if bluetooth is turned on"
        )

        return []


class ActionAskOBDAdapter(Action):
    """This is the action that is called when slot `bluetooth` is filled."""

    @staticmethod
    def name(**kwargs) -> Text:
        return "action_ask_obd_adapter"

    async def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        dispatcher.utter_message(
            text="checking if obd adapter is selected"
        )

        return []
