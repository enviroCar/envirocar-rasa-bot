from dataclasses import dataclass
import json
from model.action_model import ActionModel


@dataclass
class ResponseModel:
    """data class for response model"""

    query: str
    reply: str
    data: json
    action: ActionModel = None
