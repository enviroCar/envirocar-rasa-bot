from dataclasses import dataclass

from model.recording_track.RecordingMetadata import RecordingMetadata
@dataclass
class MatadataModel:
    """data class for metadata model"""

    type: str
    recordingMetadata: RecordingMetadata = None



