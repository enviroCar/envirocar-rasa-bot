import enum


class CarSelection(enum.Enum):
    """
        Defines various car selection actions.
    """
    SELECT = "SELECT"
    DESELECT = "DESELECT"
    DELETE = "DELETE"
