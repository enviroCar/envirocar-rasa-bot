import enum


class Recording(enum.Enum):
    START = "START"
    STOP = "STOP"
    CHANGE_VIEW = "CHANGE_VIEW"
    DISTANCE = "DISTANCE"
    TRAVEL_TIME = "TRAVEL_TIME"
