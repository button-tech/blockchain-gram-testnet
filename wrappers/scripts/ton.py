import subprocess
import os
import json
import time

workdir = os.environ["WORKDIR"]

def generate_addr(catalog_id, network="-1"):
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

            if len(public_key_f) != 64 or public_key_f[len(public_key_f)-1] == " ":
                return False

            addresses_list = get_three_addresses(public_key_f, catalog_id, network)

            if len(addresses_list) == False or len(addresses_list) != 3:
                return False

            data["publicKeyF"] = public_key_f

            data["publicKeyS"] = addresses_list[2]

            data["forInit"] = addresses_list[1]

            data["catalogId"] = catalog_id

            os.system(f"rm {workdir}/{chain}/{catalog_id}/*.fift")

            with open(f'{workdir}/{chain}/{catalog_id}/pub.json', 'w') as f:
                json.dump(data, f)   
            return data
    except:
        return False

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

            if len(public_key_f) != 64 or public_key_f[len(public_key_f)-1] == " ":
                return False

            addresses_list = get_three_addresses(public_key_f, catalog_id, network)

            if len(addresses_list) == False or len(addresses_list) != 3:
                return False

            data["publicKeyF"] = public_key_f

            data["publicKeyS"] = addresses_list[2]

            data["forInit"] = addresses_list[1]

            data["catalogId"] = catalog_id

            nonce_first = get_nonce("fcb91a3a3816d0f7b8c2c76108b8a9bc5a6b7a55bd79f8ab101c52db29232260")

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

            os.system(f"{workdir}/liteclient-build/crypto/fift -I {workdir}/lite-client/crypto/fift/lib/ -s {workdir}/{chain}/{sender_id}/send.fift {sender_id} {network + pub_rec} {nonce} {amount} 1>/dev/null")
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
            Masterchain 0xfcb91a3a3816d0f7b8c2c76108b8a9bc5a6b7a55bd79f8ab101c52db29232260
            2constant giver_addr
            ."Test giver address = " giver_addr 2dup .addr cr 6 .Addr cr

            ''' + network + ''' 0x'''+ pub +'''
            2constant dest_addr 
            false constant bounce

            0x'''+ nonce +''' constant seqno

            GR$2.666 constant amount
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

    text =  '''
    "TonUtil.fif" include

{ ."usage: " @' $0 type ." <filename-base> <dest-addr> <seqno> <amount> [-B <body-boc>] [<savefile>]" cr
  ."Creates a request to simple wallet created by new-wallet.fif, with private key loaded from file <filename-base>.pk "
  ."and address from <filename-base>.addr, and saves it into <savefile>.boc ('wallet-query.boc' by default)" cr 1 halt
} : usage
  $# dup 4 < swap 5 > or ' usage if
  def? $6 { @' $5 "-B" $= { @' $6 =: body-boc-file [forget] $6 def? $7 { @' $7 =: $5 [forget] $7 } { [forget] $5 } cond
   @' $# 2- =: $# } if } if

   true constant bounce

   $1 =: file-base
   $2 bounce parse-load-address =: bounce 2=: dest_addr
    $3 =: seqno
$4 $>GR =: amount
def? $5 { @' $5 } { "wallet-query" } cond constant savefile

file-base +".addr" load-address
2dup 2constant wallet_addr
."Source wallet address = " 2dup .addr cr 6 .Addr cr
file-base +".pk" load-keypair nip constant wallet_pk

def? body-boc-file { @' body-boc-file file>B B>boc } { <b "TEST" $, b> } cond
constant body-cell

."Transferring " amount .GR ."to account "
dest_addr 2dup bounce 7 + .Addr ." = " .addr 
."bounce=" bounce . cr
."Body of transfer message is " body-cell <s csr. cr
  
// create a message
<b b{01} s, bounce 1 i, b{000100} s, dest_addr addr, amount Gram, 0 9 64 32 + + 1+ u, 
  body-cell <s 2dup s-fits? not rot over 1 i, -rot { drop body-cell ref, } { s, } cond
b>
<b seqno 32 u, 1 8 u, swap ref, b>
dup ."signing message: " <s csr. cr
dup hash wallet_pk ed25519_sign_uint
<b b{1000100} s, wallet_addr addr, 0 Gram, b{00} s,
   swap B, swap <s s, b>
dup ."resulting external message: " <s csr. cr
2 boc+>B dup Bx. cr
"send-''' + pub_sender + "-" + pub_rec + '''.boc" tuck B>file
."(Saved to file " type .")" cr
'''
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
def get_three_addresses(pub, catalog_id, network="-1",):
    chain = ""

    if network == "-1":
        chain = "masterchain"
    elif network == "0":
        chain = "basechain"
   
    text = '''
    "TonUtil.fif" include

    '''+ network +''' constant bounce
    0x'''+ pub +''' constant wallet_addr

    wallet_addr
    ."" bounce ._ .":" x. cr
    bounce wallet_addr 2dup 7 .Addr cr
    6 .Addr
    '''
    try:
        with open(f'{workdir}/{chain}/{catalog_id}/get_addresses.fift', "w") as f:
            f.write(text)
        stdoutdata = subprocess.getoutput(f"{workdir}/liteclient-build/crypto/fift -I {workdir}/lite-client/crypto/fift/lib/ {workdir}/{chain}/{catalog_id}/get_addresses.fift")
        os.system(f"rm {workdir}/{chain}/{catalog_id}/get_addresses.fift")
        return stdoutdata.split("\n")
    except:
        return False

def reg_account(catalog_id, network="-1"):
    chain = ""

    if network == "-1":
        chain = "masterchain"
    elif network == "0":
        chain = "basechain"
    try:
        subprocess.getoutput(f"{workdir}/cli_exec/send_address {workdir} {catalog_id} {chain}")
        subprocess.getoutput(f"{workdir}/cli_exec/last {workdir}")
        return True
    except:
        return False

def check_account_seqno(pub, network):
    stdoutdata = subprocess.getoutput(f"{workdir}/cli_exec/getaccount {workdir} {network} {pub}")

    if stdoutdata.find("data:") == -1:
        return False

    return True    

