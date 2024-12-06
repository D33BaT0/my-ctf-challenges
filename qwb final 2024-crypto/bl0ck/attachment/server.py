from aes import AES
from secret import flag 

def xor(a, b):
    return bytes([x ^ y for x, y in zip(a * 2, b)])

class HAeSH:
    def __init__(self, key):
        self.state = b'\x00' * 16 
        self.key = key
        self.blocks = []
    
    def update(self, block, backdoor = None):
        assert len(block) == 16 or len(block) == 24 or len(block) == 32, "🚫 Block length should be 16,24,32"
        self.blocks.append(block)
        mid_state = xor(self.state, block) 
        if len(self.blocks) > 1:
            assert mid_state not in self.blocks, "🚫 Block repetition detected"
        self.state = xor(self.state, 
                         AES(mid_state, backdoor).
                         encrypt_block(self.key))

    def digest(self):
        return self.state

def blocks_length_check(blocks):
    if len(blocks) <= 1: return True
    return len(blocks[-1]) == len(blocks[0])

def main():
    key = bytes.fromhex(input('🔑: '))
    assert len(key) == 16, "Key length should be 16" 
    hash = HAeSH(key)
    blocks = []
    for _ in "HAeSH"[2:4]:
        block = bytes.fromhex(input(f"🥢[{_}]: "))
        hash.update(block, True) 
        blocks.append(block)
        if not blocks_length_check(blocks):
            print("🚫 Block length mismatch")
            return
        quit_option = input("🔚 Quit? (y/n): ")
        if quit_option == "y":
            break
    
    if hash.digest() == b'\x00' * 16:
        print("🔓 Success!") 
        print(f'🏁 {flag}')
    else:
        print("🔒 Failed!")

if __name__ == '__main__': 
    main()
