from flask_cors import CORS
from models.RTSPStream import RTSPStream
from flask import Flask, request, Response
from impl.StreamManager import StreamManager
import config

stream_manager = StreamManager()
app = Flask(__name__, static_folder='static')
cors = CORS(app)
headers = {
    'Access-Control-Allow-Origin': '*',
    'Content-Type': 'application/json'
}


@app.route("/api/v1/streams", methods=['GET'])
def streams_select():
    return Response(stream_manager.get_streams(), headers=headers, status=200)


@app.route("/api/v1/streams/<stream_uuid>", methods=['GET'])
def streams_select_by_uuid(stream_uuid):
    streams = stream_manager.get_streams_by_uuid(stream_uuid)
    code = 404 if len(streams) == 0 else 200
    streams = streams[0] if len(streams) != 0 else None
    return Response(streams, status=code, headers=headers)


@app.route("/api/v1/streams/<stream_uuid>", methods=['DELETE'])
def streams_delete(stream_uuid):
    status = stream_manager.del_streams(stream_uuid)
    return Response(status=status, headers=headers)


@app.route("/api/v1/streams", methods=['POST'])
def streams_create():
    stream = RTSPStream(request.get_json(), config.HOST)
    stream_manager.add_streams(stream)
    return Response(stream.uuid, status=200, headers=headers)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5600)
