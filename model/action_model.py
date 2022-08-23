from dataclasses import dataclass

from model.activity_extras_model import ActivityExtrasModel
from model.next_action import NextAction


@dataclass
class ActionModel:
    """data class for action model"""

    custom_event: str
    next_action: NextAction
    activity_class_name: str = None
    activity_extras: ActivityExtrasModel = None

    def as_dict(self):
        return {'custom_event': self.custom_event, 'activity_class_name': self.activity_class_name,
                'activity_extras': self.activity_extras}
