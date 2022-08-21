from dataclasses import dataclass
from json import JSONEncoder
from dataclasses_json import dataclass_json

from model.activity_extras_model import ActivityExtrasModel


@dataclass_json
@dataclass
class ActionModel:
    """data class for action model"""

    custom_event: str
    activity_class_name: str
    activity_extras: ActivityExtrasModel = None
