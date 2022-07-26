from dataclasses import dataclass


@dataclass
class ActivityExtrasModel:
    """data class for activity extras model"""

    name: str
    is_mandatory: bool
