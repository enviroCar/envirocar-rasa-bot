import json
from enums.custom_event_type import CustomEventType
from model.custom_event_model import CustomEventModel

from rasa_sdk.executor import CollectingDispatcher

from enums.navigation.navigation_screens import NavigationScreens
from model.action_model import ActionModel
from model.next_action import NextAction
from model.response_model import ResponseModel


def nav_to_car_selection_screen(dispatcher: CollectingDispatcher, message: str, intent: str, entities: json) -> None:
    response = ResponseModel(
        query=message,
        reply="You are not on car selection screen, navigating to car selection screen. Please ask for car selection again",
        action=ActionModel(
            activity_class_name="org.envirocar.app.views.carselection.CarSelectionActivity",
            custom_event=CustomEventModel(
                type=CustomEventType.NavigationScreens.value,
                name=NavigationScreens.CAR_SELECTION.value
            ),
            next_action=NextAction.RECOGNITION.value
        ),
        data={"intent": intent}
    )
    dispatcher.utter_message(
        json_message={"query": response.query, "reply": response.reply, "action": response.action.as_dict(),
                      "data": response.data}
    )
