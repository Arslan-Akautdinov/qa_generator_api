import config
import json
import os

from impl.FFMPEGClient import FFMPEGClient
from models.RTSPStream import RTSPStream


class StreamManager:

    def __init__(self):
        self.ffmpeg = FFMPEGClient(config.BIN_FFMPEG)
        self.streams = json.load(open(os.path.join(config.DIR_ROOT, "streams.json")))

    def get_streams(self):
        return json.dumps(self.streams)

    def get_streams_by_uuid(self, uuid):
        return [stream for stream in self.streams if stream.uuid == uuid]

    def add_streams(self, stream: RTSPStream):
        self.ffmpeg.create_video(stream)
        self.streams.append(stream.__dict__)
        self.write_stream()

    def del_streams(self, stream_uuid):
        stream = [stream for stream in self.streams if stream["uuid"] == stream_uuid]
        if len(stream) != 0:
            self.del_video(stream[0])
            return 200
        else:
            return 404

    def del_video(self, stream):
        self.streams.remove(stream)
        os.remove(os.path.join(config.DIR_VIDEO, f'{stream["file_name"]}.{stream["file_type"]}'))
        self.write_stream()

    def write_stream(self):
        open(os.path.join(config.DIR_ROOT, "streams.json"), "w").write(
            json.dumps(self.streams, indent=4, sort_keys=True))
