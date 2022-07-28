from typing import Any, Text, Dict, List
from matplotlib.pyplot import text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHelloWorld(Action):

    @staticmethod
    def name() -> Text:
        return "action_hello_world"

    @staticmethod
    def run(dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any], **kwargs) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="Hello world!"
        )

        return []
