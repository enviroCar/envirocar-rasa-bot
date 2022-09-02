from typing import Text, Any, Dict

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from enums.recording.metadata_type import MetadataType
from utils.car_utils.CarUtils import CarUtils

ALLOWED_CAR_NUMBER = ["first", "second", "third", "next", "previous"]


class ValidateCarSelectionForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_car_selection_form"

    @staticmethod
    def validate_car_number(
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `car_number` value."""

        # get the car iteration number slot and other required slots
        # TODO - get an object for all required car selection slots
        select_car_iteration = tracker.get_slot("select_car_iteration")
        next_car = tracker.get_slot("next_car")
        previous_car = tracker.get_slot("previous_car")

        print("Printing `ValidateCarSelectionForm` slots: \n",
              "`select_car_iteration`", select_car_iteration,
              "`next_car`", next_car,
              "`previous_car`", previous_car)

        metadata = tracker.latest_message.get("metadata")

        global next_index
        next_index = 0

        # check the metadata type is `CAR_SELECTION`
        if metadata["type"] == MetadataType.CAR_SELECTION.value:
            if metadata["car_selection_metadata"]["is_car_selection_fragment"]:
                cars = metadata["car_selection_metadata"]["cars"]
                car_utils = CarUtils()
                car_index = car_utils.get_car_index(select_car_iteration=select_car_iteration)
                available_car_status = car_utils.get_available_car_status(cars=cars, car_index=car_index)
                available_message = available_car_status["message"]
                # if s
                if slot_value.lower() not in ALLOWED_CAR_NUMBER:
                    dispatcher.utter_message(text="Please specify a correct number that is one, two or three")
                    return {"car_number": None}
                if slot_value.lower() == "next":
                    next_utter_status = car_utils.get_next_utter_status(select_car_iteration=select_car_iteration,
                                                                        cars=cars)
                    utter_message = next_utter_status["message"]

                    next_index = return_select_car_iteration = select_car_iteration \
                        if next_utter_status["index"] == 0 else select_car_iteration + 1.0
                    dispatcher.utter_message(text=utter_message)
                    return {"car_number": None, "next_car": True, "previous_car": False,
                            "select_car_iteration": return_select_car_iteration}
                if slot_value.lower() == "previous" and select_car_iteration == 0:
                    dispatcher.utter_message(text="You are on the first list, you can't go previous")
                    dispatcher.utter_message(text=available_message)

                    return {"car_number": None, "next_car": False, "previous_car": False}
                if slot_value.lower() == "previous":
                    utter_message = car_utils.get_prev_available_car_message(cars, select_car_iteration)
                    dispatcher.utter_message(text=utter_message)

                    return {"car_number": None, "previous_car": True,
                            "select_car_iteration": select_car_iteration - 1.0}

                return validate_car_selection(dispatcher, slot_value.lower(), cars, select_car_iteration,
                                              car_utils, next_car, previous_car, next_index)
        return {}


def validate_car_selection(dispatcher: CollectingDispatcher, slot_value: str, cars: list, select_car_iteration: int,
                           car_utils: CarUtils, next_car: bool, previous_car: bool, next_car_index: int) -> Dict[
    Text, Any]:
    car_index = car_utils.get_car_index(select_car_iteration=select_car_iteration)
    available_car_status = car_utils.get_available_car_status(cars=cars, car_index=car_index)
    available_cars = available_car_status["cars"]

    # We increment or decrement every time the user selects the next or previous car(depending on the index of car list),
    # so below snippet is there to get available cars for last iteration for selecting correct car.
    new_select_car_iteration = select_car_iteration

    if next_car_index != select_car_iteration and next_car:
        new_select_car_iteration -= 1
    elif previous_car:
        new_select_car_iteration += 1

    # get available cars based on `new_select_car_iteration`
    if new_select_car_iteration > 0:
        car_index = car_utils.get_car_index(select_car_iteration=new_select_car_iteration)
        available_car_status = car_utils.get_available_car_status(cars=cars, car_index=car_index)
        available_cars = available_car_status["cars"]
    elif new_select_car_iteration > 0:
        car_index = car_utils.get_car_index(select_car_iteration=new_select_car_iteration)
        available_car_status = car_utils.get_available_car_status(cars=cars, car_index=car_index)
        available_cars = available_car_status["cars"]

    # TODO: new function-> reset only car selection related slots
    if slot_value == "third" and len(available_cars) >= 3:
        # dispatcher.utter_message(text=f"{available_cars[2]} car is available")
        return {"car_number": True, "car_name": available_cars[2]}
    if slot_value == "second" and len(available_cars) >= 2:
        # dispatcher.utter_message(text=f"{available_cars[1]} car is available")
        return {"car_number": True, "car_name": available_cars[1]}
    if slot_value == "first" and len(available_cars) >= 1:
        # dispatcher.utter_message(text=f"{available_cars[0]} car is available")
        return {"car_number": True, "car_name": available_cars[0]}

    dispatcher.utter_message(text="Something went wrong")
    return {"car_number": None}
