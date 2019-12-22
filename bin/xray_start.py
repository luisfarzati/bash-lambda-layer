import time
import json
import socket
import os
import binascii

AWS_LAMBDA_FUNCTION_NAME=os.getenv("AWS_LAMBDA_FUNCTION_NAME")
AWS_XRAY_DAEMON_ADDRESS=os.getenv("AWS_XRAY_DAEMON_ADDRESS")
TRACE_ID=sys.argv[1] # os.getenv("AWS_LAMBDA_TRACE_ID")

START_TIME = time.time()
SEGMENT_ID=binascii.b2a_hex(os.urandom(8))
SEGMENT_DOC=json.dumps({"trace_id": TRACE_ID, "id": SEGMENT_ID, "start_time": START_TIME, "in_progress": True, "name": AWS_LAMBDA_FUNCTION_NAME})
HEADER=json.dumps({"format": "json", "version": 1})
TRACE_DATA = HEADER + "\n" + SEGMENT_DOC

UDP_IP=AWS_XRAY_DAEMON_ADDRESS.split(":")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(TRACE_DATA, (UDP_IP[0], int(UDP_IP[1])))

print SEGMENT_DOC