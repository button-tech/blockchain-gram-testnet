#!/usr/bin/env python3.7
import uuid
from ton import gen_addr_and_get_faucet
import sys

def generate():
    rand_value = str(uuid.uuid4().hex)

    account_data = gen_addr_and_get_faucet(rand_value, sys.argv[1])

    if account_data == False:
        account_data = gen_addr_and_get_faucet(rand_value, sys.argv[1])
        if account_data == False:
                print("error")
        else:
                print(account_data)        
    else:
        print(account_data)

if __name__=='__main__':
        generate()
