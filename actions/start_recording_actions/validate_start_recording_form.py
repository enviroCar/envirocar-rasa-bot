from abc import ABC
from typing import Text, Dict, Any

from rasa.shared.core.events import FollowupAction
from rasa_sdk import FormValidationAction, Tracker
from rasa_sdk.executor import CollectingDispatcher

from model.recording_track.Bluetooth import Bluetooth
from model.recording_track.Car import Car
from model.recording_track.GPS import GPS
from model.recording_track.OBDAdapter import OBDAdapter

from model.recording_track.RecordingMode import RecordingMode


# TODO making slot `recording` synced with mobile app...
class ValidateStartRecordingForm(FormValidationAction, ABC):

    def name(self) -> Text:
        return "validate_start_recording_form"

    @staticmethod
    def validate_recording_mode(slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) \
            -> Dict[Text, Any]:
        """
        Validate `recording_mode` value.
        1. If `recording_mode` is OBD then return slot value
        2. If `recording_mode` is GPS then return slot value
        """

        if slot_value == RecordingMode.OBD.value:
            dispatcher.utter_message(text=f"Recording mode is {slot_value}")
            return {"recording_mode": slot_value}
        elif slot_value == RecordingMode.GPS.value:
            dispatcher.utter_message(text=f"Recording mode is {slot_value}")
            return {"recording_mode": slot_value}
        else:
            dispatcher.utter_message(text="Incorrect recording mode selected. please try again.")
            return {"recording_mode": None, "requested_slot": None}

    @staticmethod
    def validate_gps(slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) \
            -> Dict[Text, Any]:
        """
        Validate `gps` value.
        1. If `gps` is on and recording mode is `GPS` or `OBD` then return `gps` and continue the story
        2. If `gps` is off then return `gps` and `requested_slot` None i.e. exit form
        """

        if slot_value == GPS.ON.value:
            dispatcher.utter_message(text="GPS is on")

            return {"gps": slot_value}
        else:
            dispatcher.utter_message(text="GPS is not on")
            return {"recording_mode": None, "gps": None, "requested_slot": None}

    @staticmethod
    def validate_car(slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) \
            -> Dict[Text, Any]:
        """Validate `car` value.
        1. If `car` is selected and `recording mode` was `gps` then start recording
        2. If `car` is selected and `recording mode` was `obd` then continue the story
        2. If `car` is not selected then return all slots and `requested_slot` None i.e. exit form"""

        recording_mode = tracker.get_slot("recording_mode")
        gps = tracker.get_slot("gps")

        if gps == GPS.ON.value and recording_mode == RecordingMode.GPS.value and slot_value == Car.Selected.value:
            dispatcher.utter_message(text="Car is selected")

            # return {"recording_mode": None, "gps": None, "car": None, "requested_slot": None}
            return {"requested_slot": None}
        elif gps == GPS.ON.value and recording_mode == RecordingMode.OBD.value and slot_value == Car.Selected.value:
            dispatcher.utter_message(text="Car is selected")

            return {"car": slot_value}
        elif slot_value == Car.Not_Selected.value:
            # Car is not selected
            dispatcher.utter_message(text="Car is not selected")
            return {"recording_mode": None, "gps": None, "car": None, "requested_slot": None}
        else:
            # GPS is not ON
            dispatcher.utter_message(text="GPS is not on")
            return {"recording_mode": None, "gps": None, "car": None, "requested_slot": None}

    @staticmethod
    def validate_bluetooth(slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) \
            -> Dict[Text, Any]:
        """Validate `bluetooth` value.
        1. If `bluetooth` is on then start recording
        2. If `bluetooth` is off then return all slots and `requested_slot` None i.e. exit form"""

        recording_mode = tracker.get_slot("recording_mode")
        gps = tracker.get_slot("gps")
        car = tracker.get_slot("car")

        if gps == GPS.ON.value and recording_mode == RecordingMode.OBD.value \
                and car == Car.Selected.value and slot_value == Bluetooth.ON.value:
            dispatcher.utter_message(text="Bluetooth is on")

            return {"bluetooth": slot_value}
        elif slot_value == Bluetooth.OFF.value:
            dispatcher.utter_message(text="Bluetooth is off")
            return {"recording_mode": None, "gps": None, "car": None, "bluetooth": None, "requested_slot": None}
        elif car == Car.Not_Selected.value:
            # Car is not selected
            dispatcher.utter_message(text="Car is not selected")
            return {"recording_mode": None, "gps": None, "car": None, "bluetooth": None, "requested_slot": None}
        else:
            # GPS is not ON
            dispatcher.utter_message(text="GPS is not on")
            return {"recording_mode": None, "gps": None, "car": None, "bluetooth": None, "requested_slot": None}

    @staticmethod
    def validate_odb_adapter(slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) \
            -> Dict[Text, Any]:
        """Validate `odb_adapter` value.
        1. If `odb_adapter` is selected then start recording
        2. If `odb_adapter` is not selected then return all slots and `requested_slot` None i.e. exit form"""

        recording_mode = tracker.get_slot("recording_mode")
        gps = tracker.get_slot("gps")
        car = tracker.get_slot("car")
        bluetooth = tracker.get_slot("bluetooth")

        if gps == GPS.ON.value and recording_mode == RecordingMode.OBD.value \
                and car == Car.Selected.value and bluetooth == Bluetooth.ON.value \
                and slot_value == OBDAdapter.Selected.value:

            dispatcher.utter_message(text="OBDAdapter is selected")

            # making all slots `None` so that it's not pre-filled for next times
            return {"recording_mode": None, "gps": None, "car": None, "bluetooth": None, "obd_adapter": None,
                    "requested_slot": None}

        elif bluetooth == Bluetooth.OFF.value:
            dispatcher.utter_message(text="Bluetooth is off")
            return {"recording_mode": None, "gps": None, "car": None, "bluetooth": None, "obd_adapter": None,
                    "requested_slot": None}
        elif car == Car.Not_Selected.value:
            # Car is not selected
            dispatcher.utter_message(text="Car is not selected")
            return {"recording_mode": None, "gps": None, "car": None, "bluetooth": None, "obd_adapter": None,
                    "requested_slot": None}
        elif gps == GPS.OFF.value:
            # GPS is not ON
            dispatcher.utter_message(text="GPS is not on")
            return {"recording_mode": None, "gps": None, "car": None, "bluetooth": None, "obd_adapter": None,
                    "requested_slot": None}
        else:
            dispatcher.utter_message(text="ODB Adapter is not selected")
            return {"recording_mode": None, "gps": None, "car": None, "bluetooth": None, "obd_adapter": None,
                    "requested_slot": None}
