import enum


class RecordingRequirements(enum.Enum):
    GPS = "GPS"
    BLUETOOTH = "BLUETOOTH"
    CAR = "CAR"
    OBD = "OBD"
    DASHBOARD = "DASHBOARD"
    LOCATION_PERMS = "LOCATION_PERMS"
    BLUETOOTH_PERMS = "BLUETOOTH_PERMS"
