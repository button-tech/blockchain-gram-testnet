#!/usr/bin/env python3.7
import uuid
from ton import generate_addr
import sys

def generate():
    rand_value = str(uuid.uuid4().hex)

    print(generate_addr(rand_value, sys.argv[1]))

if __name__=='__main__':
        generate()
