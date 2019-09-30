#!/usr/bin/env python3.7
import uuid
from ton import generate_addr
import sys

print(generate_addr(str(uuid.uuid4().hex), sys.argv[1]))
