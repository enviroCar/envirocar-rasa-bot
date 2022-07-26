from dataclasses import dataclass

from model.activity_extras_model import ActivityExtrasModel


@dataclass
class ActionModel:
    """data class for action model"""

    activity_class_name: str
    activity_extras: ActivityExtrasModel
