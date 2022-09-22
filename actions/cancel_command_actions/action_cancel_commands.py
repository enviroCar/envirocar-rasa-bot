from typing import Any, Text, Dict, List

from rasa_sdk.events import AllSlotsReset, ActiveLoop
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionCancelCommands(Action):
    """This is the action that is called when the user says "cancel"."""

    @staticmethod
    def name(**kwargs) -> Text:
        return "action_cancel_commands"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any], **kwargs) -> List[
        Dict[Text, Any]
    ]:
        dispatcher.utter_message("Okay, cancelling running commands!")
        return [AllSlotsReset(), ActiveLoop(None)]
