from enums.recording.metadata_type import MetadataType
from model.action_model import ActionModel
from model.next_action import NextAction
from model.response_model import ResponseModel
from utils.car_utils.navigation_to_car_screen import nav_to_car_selection_screen


class CarUtils:

    @staticmethod
    def get_car_index(select_car_iteration) -> int:
        return int(select_car_iteration) * 3

    @staticmethod
    def get_cars(cars, car_index):
        if len(cars) >= (3 + car_index - 1):
            return 3
        if len(cars) == (2 + car_index - 1):
            return 2
        if len(cars) == (1 + car_index - 1):
            return 1
        return 1

    def get_available_car_status(self, cars: list, car_index: int):
        no_of_cars = self.get_cars(cars, car_index)
        if no_of_cars == 3:
            available_cars = cars[car_index:car_index + 3]
            return {
                "three": True,
                "cars": available_cars,
                "message": self._get_utter_message(available_cars)
            }
        if no_of_cars == 2:
            available_cars = cars[car_index:car_index + 2]
            return {
                "two": True,
                "cars": available_cars,
                "message": self._get_utter_message(available_cars)
            }
        if no_of_cars == 1:
            available_cars = cars[car_index:car_index + 1]
            return {
                "one": True,
                "cars": available_cars,
                "message": self._get_utter_message(available_cars)
            }
        return {
            "zero": True,
            "message": self._get_utter_message([])

        }

    def get_prev_available_car_message(self, cars, select_car_iteration):
        car_index = self.get_car_index(select_car_iteration)
        available_cars = []
        for i in range(car_index, car_index + 3, 3):
            available_cars = cars[i:i + 3]
        return self._get_utter_message(available_cars)

    def get_next_utter_status(self, select_car_iteration, cars):
        car_index = self.get_car_index(select_car_iteration + 1)
        available_cars = self.get_available_car_status(cars, car_index)["cars"]

        if len(available_cars) == 3:
            return {
                "index": 3,
                "message": f"""
                    In the next list, say first to select {available_cars[0]} say second to select {available_cars[1]} and say third to select {available_cars[2]}, if your car is not in this list say next to select from next list or say previous to select from the previous list.
                """
            }

        if len(available_cars) == 2:
            return {
                "index": 2,
                "message": f"""
                    In the next list, say first to select {available_cars[0]} and say second to select {available_cars[1]} if your car is not in this list say previous to select from the previous list.
                """
            }
        if len(available_cars) == 1:
            return {
                "index": 1,
                "message": f"""
                    There is only one car in the next list, that is {available_cars[0]} say first to select it. if your car is not in this list say previous to select from the previous list.
                """

            }
        return {
            "index": 0,
            "message": """
                There are no cars left, say previous to select from the previous list.
            """
        }

    @staticmethod
    def _get_utter_message(available_cars: list):
        if len(available_cars) == 3:
            return (
                f"""
                    there are 3 cars, say first to select {available_cars[0]}, and say second to select {available_cars[1]} and say third to select {available_cars[2]}, if your car is not in this list say next to select from the next list or say previous to select from the previous list.
                """
            )

        if len(available_cars) == 2:
            return (
                f"""
                    there are 2 cars, say first to select {available_cars[0]}, and say second to select {available_cars[1]}, if your car is not in this list say next to select from the next list or say previous to select from the previous list.
                """
            )
        if len(available_cars) == 1:
            return (
                f"""
                    there is only 1 car, say first to select {available_cars[0]}.
                """
            )
            # TODO OR
            #  """
            # return (
            # f"there is only 1 car, selecting {available_cars[0]}."
            # )
            # """
        return (
            """You have not added any cars yet. Please add a new car first."""
        )

    @staticmethod
    def ask_car_number(metadata, dispatcher, tracker, intent, entities, message) -> bool:
        # if the metadata type is car selection
        # if metadata["type"] == MetadataType.CAR_SELECTION.value:
        if metadata["isDashboardFragment"] and \
                not metadata["car_selection_metadata"]["is_car_selection_fragment"]:
            # if the user is on dashboard fragment, then navigate them to car selection screen
            nav_to_car_selection_screen(dispatcher, message, intent)
        elif metadata["car_selection_metadata"]["is_car_selection_fragment"]:
            # if the user is on car selection screen, start the form
            select_car_iteration = tracker.get_slot("select_car_iteration")

            cars = metadata["car_selection_metadata"]["cars"]

            car_utils = CarUtils()
            car_index = car_utils.get_car_index(select_car_iteration)

            available_car_status = car_utils.get_available_car_status(
                cars, car_index)
            response = car_utils.return_response(
                available_car_status["message"])
            dispatcher.utter_message(json_message={
                "query": response.query,
                "reply": response.reply,
                "action": response.action.as_dict(),
                "data": response.data
            })
        return True
        # else:
        # return False

    def return_response(self, reply: str):
        response = ResponseModel(
            query="",
            reply=reply,
            action=ActionModel(
                next_action=NextAction.RECOGNITION.value
            ),
            data={}
        )
        return response
