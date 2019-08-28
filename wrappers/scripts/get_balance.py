#!/usr/bin/env python3.7
import sys
from ton import get_nano_grams

balance = get_nano_grams(sys.argv[1], sys.argv[2])

if balance == False:
    print("error")
else:
    print(balance)
