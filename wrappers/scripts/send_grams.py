#!/usr/bin/env python3.7
import sys
from ton import send

data = {
    "senderId":sys.argv[1],
    "senderPub":sys.argv[2],
    "recipientPub":sys.argv[3],
    "amount":sys.argv[4],
    "network":sys.argv[5]
}

result = send(data)

if result == False:
    print("error")
else:
    print(result)