import time
import json
import socket
import sys
import os

AWS_XRAY_DAEMON_ADDRESS=os.getenv("AWS_XRAY_DAEMON_ADDRESS")

SEGMENT_DOC = json.loads(sys.argv[1])
del SEGMENT_DOC["in_progress"]
END_TIME = time.time()
SEGMENT_DOC["end_time"] = END_TIME
HEADER=json.dumps({"format": "json", "version": 1})
TRACE_DATA = HEADER + "\n" + json.dumps(SEGMENT_DOC)

UDP_IP=AWS_XRAY_DAEMON_ADDRESS.split(":")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(TRACE_DATA, (UDP_IP[0], int(UDP_IP[1])))

print json.dumps(SEGMENT_DOC)