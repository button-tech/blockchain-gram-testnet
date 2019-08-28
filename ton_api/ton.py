import subprocess
import os
import json
import time

workdir = os.environ["WORKDIR"]

def gen_addr_and_get_faucet(catalog_id, network="-1"):
    try:

        chain = ""

        if network == "-1":
            chain = "masterchain"
        elif network == "0":
            chain = "basechain"

        data = {}

        if os.path.isdir(f'{workdir}/{chain}/{catalog_id}') == False:
            os.system(f'mkdir -p {workdir}/{chain}/{catalog_id}')
            if create_new_wallet_file(catalog_id, network) != True:
                return False

            stdoutdata = subprocess.getoutput(f"{workdir}/liteclient-build/crypto/fift -I {workdir}/lite-client/crypto/fift/lib/ {workdir}/{chain}/{catalog_id}/create_wallet.fift")

            os.system(f"mv {workdir}/{catalog_id}.* {workdir}/{chain}/{catalog_id}")

            begin = stdoutdata.find(f"new wallet address = {network} :")

            if network == "0":
                begin += 25
            else:
                begin += 26    

            public_key_f = stdoutdata[begin:begin + 64]

            public_key_s = stdoutdata[begin + 66:begin + 114]

            data["publicKeyF"] = public_key_f

            data["publicKeyS"] = public_key_s

            data["catalogId"] = catalog_id

            nonce_first = get_nonce("8156775b79325e5d62e742d9b96c30b6515a5cd2f1f64c5da4b193c03f070e0d")

            ### get test grams

            # create giver.fift
            if create_giver_file(str(catalog_id), public_key_f, str(nonce_first), network) != True:
                os.system(f"rm -r {workdir}/{chain}/{catalog_id}")
                return False

            # compile giver.fift
            os.system(f"{workdir}/liteclient-build/crypto/fift -I {workdir}/lite-client/crypto/fift/lib/ {workdir}/{chain}/{catalog_id}/giver.fift 1>/dev/null")
            os.system(f"mv {workdir}/{catalog_id}-wallet.* {workdir}/{chain}/{catalog_id}")

            # get grams
            subprocess.getoutput(f"{workdir}/cli_exec/last {workdir}")
            subprocess.getoutput(f"{workdir}/cli_exec/send_wallet_query {workdir} {catalog_id} {chain}")
            subprocess.getoutput(f"{workdir}/cli_exec/last {workdir}")
            subprocess.getoutput(f"{workdir}/cli_exec/send_address {workdir} {catalog_id} {chain}")
            subprocess.getoutput(f"{workdir}/cli_exec/last {workdir}")


            # first request show incorrect balance
            subprocess.getoutput(f"{workdir}/cli_exec/last {workdir}")
            
            time.sleep(2)
            
            subprocess.getoutput(f"{workdir}/cli_exec/last {workdir}")

            time.sleep(2)
            
            balance = get_nano_grams(public_key_f, network)

            if balance != False:
                os.system(f"rm {workdir}/{chain}/{catalog_id}/*.boc")
                os.system(f"rm {workdir}/{chain}/{catalog_id}/*.fift")
                with open(f'{workdir}/{chain}/{catalog_id}/pub.json', 'w') as f:
                    json.dump(data, f)   
                return data
            else:
                time.sleep(2)
                subprocess.getoutput(f"{workdir}/cli_exec/last {workdir}")
                time.sleep(2)
                subprocess.getoutput(f"{workdir}/cli_exec/last {workdir}")
                balance = get_nano_grams(public_key_f, network)
                if balance != False:
                    os.system(f"rm {workdir}/{chain}/{catalog_id}/*.boc")
                    os.system(f"rm {workdir}/{chain}/{catalog_id}/*.fift")
                    with open(f'{workdir}/{chain}/{catalog_id}/pub.json', 'w') as f:
                         json.dump(data, f)
                    return data
                else:    
                    os.system(f"rm -r {workdir}/{chain}/{catalog_id}")
                    return False
    except:
        return False

def send(content):
      try:
            sender_id = content["senderId"]
            pub_sender = content["senderPub"]
            pub_rec = content["recipientPub"]
            amount = content["amount"]
            network = content["network"]

            chain = ""
            if network == "-1":
                chain = "masterchain"
            elif network == "0":
                chain = "basechain"
            elif network == "":
                chain = "masterchain"
                network = "-1"

            sender_last_tx_hash_before = get_last_tx_hash(pub_sender, network)
            if sender_last_tx_hash_before == False:
                return False
            
            nonce = get_nonce(pub_sender, network)

            if create_send_fift(sender_id, pub_rec, pub_sender, amount, nonce, network) != True:
                    return False

            os.system(f"{workdir}/liteclient-build/crypto/fift -I {workdir}/lite-client/crypto/fift/lib/ {workdir}/{chain}/{sender_id}/send.fift 1>/dev/null")
            os.system(f"mv {workdir}/send-{pub_sender}-{pub_rec}.boc {workdir}/{chain}/{sender_id}")

            _ = subprocess.getoutput(f"{workdir}/cli_exec/last {workdir}")
            _ = subprocess.getoutput(f"{workdir}/cli_exec/last {workdir}")
            _ = subprocess.getoutput(f"{workdir}/cli_exec/send_grams {workdir} {sender_id} {pub_sender} {pub_rec} {chain}")
            _ = subprocess.getoutput(f"{workdir}/cli_exec/last {workdir}")
            _ = subprocess.getoutput(f"{workdir}/cli_exec/last {workdir}")

            time.sleep(2)
            sender_last_tx_hash_after = get_last_tx_hash(pub_sender, network)
            if sender_last_tx_hash_after == False:
                return False

            if sender_last_tx_hash_before != sender_last_tx_hash_after:
                os.system(f"rm {workdir}/{chain}/{sender_id}/send-*")
                os.system(f"rm {workdir}/{chain}/{sender_id}/send.fift")

                _ = subprocess.getoutput(f"{workdir}/cli_exec/last {workdir}")

                recipient_last_tx_hash = get_last_tx_hash(pub_rec, network)

                return {"senderTxHash":sender_last_tx_hash_after, "recipientTxHash":recipient_last_tx_hash}

            else:
                time.sleep(2)
                second_try = get_last_tx_hash(pub_sender, network)
                if sender_last_tx_hash_before != second_try:
                    os.system(f"rm {workdir}/{chain}/{sender_id}/send-*")
                    os.system(f"rm {workdir}/{chain}/{sender_id}/send.fift")

                    _ = subprocess.getoutput(f"{workdir}/cli_exec/last {workdir}")

                    recipient_last_tx_hash = get_last_tx_hash(pub_rec, network)

                    return {"senderTxHash":second_try, "recipientTxHash":recipient_last_tx_hash}
                else:    
                    os.system(f"rm {workdir}/{chain}/{sender_id}/send-*")
                    os.system(f"rm {workdir}/{chain}/{sender_id}/send.fift")
                    return False
      except:
          return False


# for file creation
def create_new_wallet_file(catalog_id, network="-1"):
    
    chain = ""
    if network == "-1":
        chain = "masterchain"
    elif network == "0":
        chain = "basechain"
    
    text = ''' 
    "Asm.fif" include

    '''+ network +''' constant wc  // create a wallet in workchain 0 (basechain)

    // Create new simple wallet
    <{  SETCP0 DUP IFNOTRET INC 32 THROWIF  // return if recv_internal, fail unless recv_external
    512 INT LDSLICEX DUP 32 PLDU   // sign cs cnt
    c4 PUSHCTR CTOS 32 LDU 256 LDU ENDS  // sign cs cnt cnt' pubk
    s1 s2 XCPU            // sign cs cnt pubk cnt' cnt
    EQUAL 33 THROWIFNOT   // ( seqno mismatch? )
    s2 PUSH HASHSU        // sign cs cnt pubk hash
    s0 s4 s4 XC2PU        // pubk cs cnt hash sign pubk
    CHKSIGNU              // pubk cs cnt ?
    34 THROWIFNOT         // signature mismatch
    ACCEPT
    SWAP 32 LDU NIP
    DUP SREFS IF:<{
      8 LDU LDREF         // pubk cnt mode msg cs
      s0 s2 XCHG SENDRAWMSG  // pubk cnt cs ; ( message sent )
    }>
    ENDS
    INC NEWC 32 STU 256 STU ENDC c4 POPCTR
    }>c
    // code
    <b 0 32 u,
   newkeypair swap dup constant wallet_pk
   "''' + catalog_id + '''.pk" B>file
   B,
    b> // data
    // no libraries
    <b b{00110} s, rot ref, swap ref, b>  // create StateInit
    dup ."StateInit: " <s csr. cr
    dup hash dup constant wallet_addr
    ."new wallet address = " wc . .": " dup x. cr
    wc over 7 smca>$ type cr
    256 u>B "''' + catalog_id + '''.addr" B>file
    <b 0 32 u, b>
    dup ."signing message: " <s csr. cr
    dup hash wallet_pk ed25519_sign_uint rot
    <b b{1000100} s, wc 8 i, wallet_addr 256 u, b{000010} s, swap <s s, b{0} s, swap B, swap <s s, b>
    dup ."External message for initialization is " <s csr. cr
    2 boc+>B dup Bx. cr
    "''' + catalog_id + '''.boc" tuck B>file
    ."(Saved to file " type .")" cr
    '''

    try:
        with open(f'{workdir}/{chain}/{catalog_id}/create_wallet.fift', "w") as f:
            f.write(text)
        return True

    except:
        return False


def create_giver_file(sender_id, pub, nonce, network="-1"):
    
    chain = ""

    if network == "-1":
        chain = "masterchain"
    elif network == "0":
        chain = "basechain"

    text = '''
            "''' + workdir + '''/lite-client/crypto/fift/lib/TonUtil.fif" include
            // "testgiver.addr" load-address 
            Masterchain 0x8156775b79325e5d62e742d9b96c30b6515a5cd2f1f64c5da4b193c03f070e0d
            2constant giver_addr
            ."Test giver address = " giver_addr 2dup .addr cr 6 .Addr cr

            ''' + network + ''' 0x'''+ pub +'''
            2constant dest_addr 
            false constant bounce

            0x'''+ nonce +''' constant seqno

            GR$6.666 constant amount
            ."Requesting " amount .GR ."to account "
            dest_addr 2dup bounce 7 + .Addr ." = " .addr
            ."seqno=0x" seqno x. ."bounce=" bounce . cr

            // create a message (NB: 01b00.., b = bounce)
            <b b{01} s, bounce 1 i, b{000100} s, dest_addr addr,
            amount Gram, 0 9 64 32 + + 1+ 1+ u, "GIFT" $, b>
            <b seqno 32 u, 1 8 u, swap ref, b>
            dup ."enveloping message: " <s csr. cr
            <b b{1000100} s, giver_addr addr, 0 Gram, b{00} s,
            swap <s s, b>
            dup ."resulting external message: " <s csr. cr
            2 boc+>B dup Bx. cr

            "'''+ sender_id +'''-wallet.boc" tuck B>file
            // savefile +".boc" tuck B>file
            ."(Saved to file " type .")" cr
    '''
    try:
        with open(f'{workdir}/{chain}/{sender_id}/giver.fift', "w") as f:
            f.write(text)  
        return True

    except:
        return False


def create_send_fift(catalog_id, pub_rec, pub_sender, amount, nonce, network="-1"):

    chain = ""

    if network == "-1":
        chain = "masterchain"
    elif network == "0":
        chain = "basechain"

    path = f"{workdir}/{chain}/{catalog_id}/"

    text = ''' "''' + path + catalog_id + '''.addr" file>B 256 B>u@ dup constant wallet_addr
    ."Wallet address = " x. cr
    "''' + path + catalog_id + '''.pk" file>B dup Blen 32 <> abort"Private key must be exactly 32 bytes long"
    constant wallet_pk

    0x''' + pub_rec + ''' constant dest_addr
    ''' + network +''' constant wc
    0x''' + nonce + ''' constant seqno

    1000000000 constant Gram
    { Gram swap */ } : Gram*/

    '''+ amount + ''' Gram*/ constant amount

    // b x --> b'  ( serializes a Gram amount )
    { -1 { 1+ 2dup 8 * ufits } until
    rot over 4 u, -rot 8 * u, } : Gram,

    // create a message
    <b b{011000100} s, wc 8 i, dest_addr 256 u, amount Gram, 0 9 64 32 + + 1+ 1+ u, "TEST" $, b>
    <b seqno 32 u, 1 8 u, swap ref, b>
    dup ."signing message: " <s csr. cr
    dup hash wallet_pk ed25519_sign_uint
    <b b{1000100} s, wc 8 i, wallet_addr 256 u, 0 Gram, b{00} s,
    swap B, swap <s s, b>
    dup ."resulting external message: " <s csr. cr
    2 boc+>B dup Bx. cr
    "send-''' + pub_sender + "-" + pub_rec + '''.boc" B>file'''

    try:
        with open(f'{workdir}/{chain}/{catalog_id}/send.fift', "w") as f:
            f.write(text)
        return True
    except:
        return False

def get_nonce(pub, network="-1"):
    stdoutdata = subprocess.getoutput(f"{workdir}/cli_exec/getaccount {workdir} {network} {pub}")

    begin = stdoutdata.find("data:")    
             
    begin += 70

    nonce = stdoutdata[begin:begin + 8]

    return nonce

def get_nano_grams(pub, network="-1"):
       stdoutdata = subprocess.getoutput(f"{workdir}/cli_exec/getaccount {workdir} {network} {pub}")

       begin = stdoutdata.find("balance:")

       if begin == -1:
           return False
           
       begin += 80

       f = stdoutdata[begin:]

       return stdoutdata[begin:f.find(")") + begin]

def get_last_tx_hash(pub, network="-1"):
       stdoutdata = subprocess.getoutput(f"{workdir}/cli_exec/getaccount {workdir} {network} {pub}")

       begin = stdoutdata.find("hash = ")

       if begin == -1:
           return False

       begin += 7    

       result = stdoutdata[begin:begin + 64]

       if len(result) != 64:
           return False 

       return result