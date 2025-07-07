from user import *
from Keccak224 import *
import os, signal, inspect, utils, server, user

FLAG3 = os.environ.get('FLAG', 'r3ctf{dummy_flag}')

def _handle_timeout(signum, frame):
    raise TimeoutError('function timeout')

timeout = 600
signal.signal(signal.SIGALRM, _handle_timeout)
signal.alarm(timeout)

BANNER = br"""
                                                      01
                                                      0001           0
                                                      0000       11000
                                                      0001 1  11  0000
                                                      0000 10000   000
                                                      00001100001  000
                                                      0000000000000000
                                                      0111100000000000
                                                            0000   100
               1101                                         0000     1
            1000000001       01                             0000
           00000000000000000000                             0000
          000000000000000000000100000111                    1111
         1000000000000000000000000000000000001              1  1
          1000000000000000000011        111000001           0111
             000000000000000                  10001         1010
            100000000000001                      1001       1  1
            100000001111                           001      1110     1
             100000   11                       100  101     11 1   111
               000  10001     1001111110001    1001  10     000001  0
              1000   101    001           100         0011110000  1011
           1  1001         01   11     1    00      010111  0000   10
        0     1001        10    00    000   10     11 0 1 0 0000 101
       0 01  1100011       00               00      0 01    0000
         0  010 000  1111   101           101        0  11110000
         11 1    000       001 10000100001          0       0000
           1001 0 1000 001                        01        0000
               10 00000001                     100          0000
                      1000011              10001            0000
                          100000000000000001                0000
                                                            0000
"""

LOGIN_MENU = """[+] Nice day!
[1]. Log In [Password]
[2]. Log In [Token]
[3]. Sign Up
[4]. Guess Flag Token
[5]. Exit
"""

SYSTEM_MENU = """ 
[1]. Reset Password
[2]. Exchange keys with sb.
[3]. Get news on public channels
[4]. Get your private key & public key
[5]. Quit
"""

print(BANNER.decode())

FLAG_TOKEN, PoW_KinG = os.urandom(32), False

def PoW():
    global PoW_KinG
    print("Please give me 1 pairs of (x,y) to satisfy the following equation:")
    print("                Keccak224-4(x) == Keccak224-4(y)\n") 
    print("                len(x.hex()) < 1488, len(y.hex()) < 1488\n") 
    print("After that, I will give you all the source code. ")
    print("At the same time, if you can give me 22 pairs collision with x[0] is b'r', I will reward you as a PoW King!\n\n")
    msg = os.urandom(16)
    hashvalue = Keccak224(msg)
    print(f"e.g. Keccak224-4({msg}) == {hashvalue.hexdigest()}") 
    pairs, r_times = set(), 0
    for _ in range(22):
        x,y = bytes.fromhex(input("\nInput x[HEX]: ")[:1488]), bytes.fromhex(input("Input y[HEX]: ")[:1488]) 
        if (x,y) in pairs or x == y: print("Duplicate pair, try again.");continue
        if not (Keccak224(x).hexdigest() == Keccak224(y).hexdigest()): print("Wrong pair, try again.");continue
        if x[0] == 114: r_times+=1
        pairs.add((x,y))

    if input("Do you want to see the source code? [y/n]: ").lower() == 'y': 
        print("[+] Here is the utils.py code:")
        print("="*50+"\n"+inspect.getsource(utils)+"\n"+"="*50+"\n") 
        print("[+] Here is the user.py code:")
        print("="*50+"\n"+inspect.getsource(user)+"\n"+"="*50+"\n") 
        print("[+] Here is the server.py code:")
        print("="*50+"\n"+inspect.getsource(server)+"\n"+"="*50+"\n")

    if r_times >= 22:
        PoW_KinG = True
        print("Congratulations! You are the PoW King!")
    else:
        exit()

print("Welcome to R3CTF 2025 R3System!")
print("[Note]: Please do PoW first, or you can't see the source code.\n\n") 
PoW()

PublicChannels,login_tag,USER = b"",False,Users()

AliceUsername,BobUsername = b'AliceIsSomeBody',b'BobCanBeAnyBody'

USER.register(AliceUsername,os.urandom(166)) 
USER.register(BobUsername,os.urandom(166))

def LoginSystem(USER): 
    global login_tag, FLAG_TOKEN, PoW_KinG
    option = int(input("Now input your option: "))
    if option == 1:
        username = bytes.fromhex(input("Username[HEX]: "))
        password = bytes.fromhex(input("Password[HEX]: "))
        login_tag,msg = USER.login_by_password(username,password)
        print(msg.decode())
        if login_tag: return username 

    elif option == 2:
        username = bytes.fromhex(input("Username[HEX]: "))
        if username == AliceUsername or username == BobUsername:
            print("You can't login with token!")
            return
        token = bytes.fromhex(input("Token[HEX]: "))
        login_tag,msg = USER.login_by_token(username,token)
        print(msg.decode())
        if login_tag: return username 

    elif option == 3:
        username = bytes.fromhex(input("Username[HEX]: "))
        if username == AliceUsername or username == BobUsername:
            print("You can't register with this username!")
            return
        password = bytes.fromhex(input("Password[HEX]: "))
        register_tag,msg = USER.register(username,password) 
        if register_tag: print(f"Register successfully, {username} 's token is {msg.hex()}.")
        else: print(msg.decode())

    elif option == 4:
        guess_flag_token = bytes.fromhex(input("Flag Token[HEX]: "))
        if guess_flag_token == FLAG_TOKEN and PoW_KinG:
            print(f"Congratulations! You guessed the flag token correctly! The flag is: {FLAG3}")
            exit()

    else: exit()

def R3System(USERNAME): 
    global login_tag,PublicChannels
    option = int(input(f"Hello {USERNAME.decode()}, do you need any services? "))

    if option == 1: 
        new_password = bytes.fromhex(input(f"New Password[HEX]: "))
        tag,msg = USER.reset_password(USERNAME,new_password)
        print(msg.decode())

    elif option == 2:
        ToUsername = bytes.fromhex(input(f"ToUsername[HEX]: "))
        if ToUsername not in USER.usernames: print("ERROR");return False
        PublicChannels += transfer_A2B(USER,USERNAME,ToUsername,b" My Pubclic key is: " + USER.getsb_public_key(USERNAME).hex().encode()) + \
            transfer_A2B(USER,ToUsername,USERNAME,b" My Pubclic key is: " + USER.getsb_public_key(ToUsername).hex().encode())
        ToPublickey = b2p(USER.getsb_public_key(ToUsername))
        change_key = USER.ecdhs[USERNAME].exchange_key(ToPublickey)
        print((f"Exchanged Key is: {change_key.hex()}"))
    elif option == 3: print(PublicChannels.decode())
    elif option == 4: print(f"Your private key is: {USER.view_private_key(USERNAME).hex()}\nYour public key is: {USER.getsb_public_key(USERNAME).hex()}")
    elif option == 5: login_tag = False

def Alice_transfer_flag_to_Bob(AliceUsername,BobUsername):
    global PublicChannels, FLAG_TOKEN
    PublicChannels += transfer_A2B(USER,AliceUsername,BobUsername,b" Halo bob, I will give your my flag after we exchange keys.") + \
        transfer_A2B(USER,BobUsername,AliceUsername, b" OK, I'm ready.") + \
        transfer_A2B(USER,AliceUsername,BobUsername, b" My Pubclic key is: " + USER.getsb_public_key(AliceUsername).hex().encode()) + \
        transfer_A2B(USER,BobUsername,AliceUsername, b" My Pubclic key is: " + USER.getsb_public_key(BobUsername).hex().encode()) + \
        transfer_A2B(USER,AliceUsername,BobUsername, b" Now its my encrypted flag:") + \
        transfer_A2B(USER,AliceUsername,BobUsername, FLAG_TOKEN , enc=True) + \
        transfer_A2B(USER,BobUsername,AliceUsername, b" Wow! I know your flag now! ")

Alice_transfer_flag_to_Bob(AliceUsername,BobUsername)

while 1: 
    if not login_tag: print(LOGIN_MENU); USERNAME = LoginSystem(USER) 
    else: print(SYSTEM_MENU); R3System(USERNAME)