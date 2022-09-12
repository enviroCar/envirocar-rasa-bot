from typing import Dict, Text, Any, List

from rasa_sdk.events import FollowupAction
from rasa_sdk.executor import CollectingDispatcher

from enums.custom_event_type import CustomEventType
from model.custom_event_model import CustomEventModel

from enums.navigation.navigation_screens import NavigationScreens
from model.action_model import ActionModel
from model.next_action import NextAction
from model.response_model import ResponseModel



def nav_to_recording_screen(dispatcher: CollectingDispatcher, message: str, reply: str, intent: str) -> None:
    response = ResponseModel(
        query=message,
        reply=reply,
        action=ActionModel(
            activity_class_name="org.envirocar.app.views.recordingscreen.RecordingScreenActivity",
            custom_event=CustomEventModel(
                type=CustomEventType.NavigationScreens.value,
                name=NavigationScreens.RECORDING.value
            ).as_dict(),
            next_action=NextAction.STANDBY.value
        ),
        data={"intent": intent}
    )
    dispatcher.utter_message(
        json_message={"query": response.query, "reply": response.reply, "action": response.action.as_dict(),
                      "data": response.data}
    )
