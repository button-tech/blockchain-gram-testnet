#!/usr/bin/env python3.7
from ton import check_account_seqno
import sys

print(check_account_seqno(sys.argv[1], sys.argv[2]))