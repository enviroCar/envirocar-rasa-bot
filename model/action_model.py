from dataclasses import dataclass

from model.activity_extras_model import ActivityExtrasModel
from model.custom_event_model import CustomEventModel


@dataclass
class ActionModel:
    """data class for action model"""

    next_action: str
    custom_event: CustomEventModel = None
    activity_class_name: str = None
    activity_extras: ActivityExtrasModel = None

    def as_dict(self):
        return {'custom_event': self.custom_event,
                'next_action': self.next_action,
                'activity_class_name': self.activity_class_name,
                'activity_extras': self.activity_extras}
