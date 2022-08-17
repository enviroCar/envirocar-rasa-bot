from dataclasses import dataclass

@dataclass
class RecordingMetadata:
    """data class for recording metadata model"""

    recording_mode: str
    gps: bool
    car: bool
    bluetooth: bool
    obd_adapter: bool
    className: str = None
