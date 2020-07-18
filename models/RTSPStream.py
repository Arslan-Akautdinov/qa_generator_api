import uuid


class RTSPStream:

    def __init__(self, data):
        self.uuid = uuid.uuid4().hex
        self.file_name = f'{data["file_name"]}'
        self.audio_codec = data["audio_codec"]
        self.video_codec = data["video_codec"]
        self.play_time = data["play_time"]
        self.file_type = data["file_type"]
        self.bit_rate = data["bit_rate"]
        self.quality = data["quality"]
        self.fps = data["fps"]
