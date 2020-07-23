import os

DIR_ROOT = os.path.dirname(os.path.abspath(__file__))
DIR_VIDEO = os.path.join(DIR_ROOT, "videos")

BIN_FFMPEG = "ffmpeg"
BIN_FFPROBE = "ffprobe"

# mashine ip
HOST = os.environ.get("VIDEO_HOSTING")

PORT = 21554
RANGE_START = 10000
RANGE_END = 11000
