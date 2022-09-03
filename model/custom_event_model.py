from dataclasses import dataclass


@dataclass
class CustomEventModel:
    """data class for custom event model"""

    type: str
    name: str

    def as_dict(self):
        return {'type': self.type,
                'name': self.name
                }
