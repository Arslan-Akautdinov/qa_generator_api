import os
from models.RTSPStream import RTSPStream


class FFMPEGClient:

    def __init__(self, ffmpeg):
        self.ffmpeg = ffmpeg

    def create_video(self, stream: RTSPStream):

        com =\
            f'''
                {self.ffmpeg} -f lavfi
                -i testsrc=s={stream.quality}:r={stream.fps}:sar=486/365
                -profile:v Main -c:v {stream.video_codec}
                -x264-params "nal-hrd=cbr"
                -g 125 -pix_fmt yuvj420p -c:a {stream.audio_codec} 
                -ac 1 -ar 16000
                -b:v 512k
                -bufsize 512k
                -maxrate {stream.bit_rate}
                -minrate {stream.bit_rate}
                -filter_complex "aevalsrc=-2+random(0)"
                -vf noise=all_seed=214:alls=100:allf=t
                -t {stream.play_time} videos/{stream.file_name}.{stream.file_type}
            '''

        os.system(com.replace("\n", ""))
