#!/usr/bin/env python3.7
import uuid
from ton import reg_account
import sys

print(reg_account(sys.argv[1], sys.argv[2]))
