import enum


class NextAction(enum.Enum):
    """
        Defines what will happen once speech synthesis is completed.
    """
    # Go to standby state.
    STANDBY = "STANDBY"
    # Start speech recognition.
    RECOGNITION = "RECOGNITION"
    # Do nothing after synthesis.
    NOTHING = "NOTHING"
