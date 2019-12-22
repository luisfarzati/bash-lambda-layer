import time
import json
import socket
import sys
import binascii
import os

AWS_XRAY_DAEMON_ADDRESS=os.getenv("AWS_XRAY_DAEMON_ADDRESS")

SEGMENT_DOC = json.loads(sys.argv[1])
EXCEPTION_ID = binascii.b2a_hex(os.urandom(8))
WORKING_DIRECTORY = os.getcwd()
LOG = sys.argv[2]
MESSAGE = LOG.split('* What went wrong:')[0]
ERROR = { "working_directory": WORKING_DIRECTORY, "exceptions": [ { "id": EXCEPTION_ID, "message": MESSAGE } ] }
del SEGMENT_DOC["in_progress"]
END_TIME = time.time()
SEGMENT_DOC["end_time"] = END_TIME
SEGMENT_DOC["error"] = True
SEGMENT_DOC["cause"] = ERROR

HEADER=json.dumps({"format": "json", "version": 1})
TRACE_DATA = HEADER + "\n" + json.dumps(SEGMENT_DOC)

UDP_IP=AWS_XRAY_DAEMON_ADDRESS.split(":")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(TRACE_DATA, (UDP_IP[0], int(UDP_IP[1])))

print json.dumps(SEGMENT_DOC)