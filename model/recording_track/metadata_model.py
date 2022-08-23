from dataclasses import dataclass

from model.recording_track.recording_metadata import RecordingMetadata


@dataclass
class MetadataModel:
    """data class for metadata model"""

    type: str
    recordingMetadata: RecordingMetadata = None
