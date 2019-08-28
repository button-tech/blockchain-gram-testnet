#!/usr/bin/env python3.7
import sys
from ton import get_last_tx_hash

tx_hash = get_last_tx_hash(sys.argv[1], sys.argv[2])

if tx_hash == False:
    print("error")
else:
    print(tx_hash)

