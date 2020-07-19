import os
import json
import config

from flask_cors import CORS
from flasgger import Swagger


from flask import Flask, request, Response
from impl.FFMPEGClient import FFMPEGClient
from models.RTSPStream import RTSPStream

app = Flask(__name__, static_folder='static')
cors = CORS(app)


def get_streams(stream_uuid=None):
    streams = json.load(open(os.path.join(config.DIR_ROOT, "streams.json")))
    stream_result = None
    code = 404
    if stream_uuid is None:
        stream_result = json.dumps(streams)
        code = 200
    else:
        for stream in streams:
            if stream["uuid"] == stream_uuid:
                stream_result = json.dumps(stream)
                code = 200
                break
    return Response(stream_result, code, mimetype="application/json")


def add_streams(stream: RTSPStream):
    FFMPEGClient(config.BIN_FFMPEG).create_video(stream)
    streams: list = json.load(open(os.path.join(config.DIR_ROOT, "streams.json")))
    streams.append(stream.__dict__)
    open(os.path.join(config.DIR_ROOT, "streams.json"), "w").write(json.dumps(streams, indent=4, sort_keys=True))
    resp = Response(f"rtsp://10.50.6.127:21554/stream/{stream.file_name}.{stream.file_type}/live")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    resp.status_code = 201
    return resp


def del_streams(stream_uuid):
    streams: list = json.load(open(os.path.join(config.DIR_ROOT, "streams.json")))
    for stream in streams:
        if stream["uuid"] == stream_uuid:
            streams.remove(stream)
            os.remove(os.path.join(config.DIR_VIDEO, f'{stream["file_name"]}.{stream["file_type"]}'))
            break
    open(os.path.join(config.DIR_ROOT, "streams.json"), "w").write(json.dumps(streams, indent=4, sort_keys=True))
    return "Stream deleted"


@app.route("/api/v1/streams", methods=['GET'])
def streams_select():
    return get_streams()


@app.route("/api/v1/streams/<stream_uuid>", methods=['GET'])
def streams_select_by_uuid(stream_uuid):
    return get_streams(stream_uuid)


@app.route("/api/v1/streams/<stream_uuid>", methods=['DELETE'])
def streams_delete(stream_uuid):
    return del_streams(stream_uuid), 200


@app.route("/api/v1/streams", methods=['POST'])
def streams_create():
    return add_streams(RTSPStream(request.get_json()))


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True, port=5500)
