def op_xor(c1,c2):
    return bytearray([a ^ b for a, b in zip(c1, c2)])

def op_and(c1, c2):
    return bytearray([a & b for a, b in zip(c1, c2)])

def op_or(c1,c2):
    return bytearray([a | b for a, b in zip(c1, c2)])

def get_spaces(c1,c2,len):
    '''
    Args: 
    c1: int, c2: int (ciphertexts)
    len: int (length of cipher)
    
    Returns:
    spaces: list of zeros and ones corresponding to whether there is a potential space in that pos
    revealed: list containing revealed chars of msg1/msg2 that correspond to a space in the other message, zero otherwise
    
    '''
    xor = c1 ^ c2
    xor_bytes = xor.to_bytes(len, 'big')

    spaces = []
    revealed = []
  
    for byte in xor_bytes:
        
        if byte > 64:
            spaces.append(1)
            revealed.append(byte ^ 0x20)
            
        elif byte == 0:
            spaces.append(1)
            revealed.append(0)
            
        else:
            spaces.append(0)
            revealed.append(0)
            
 
    return spaces, revealed
                
    

def decrypt_cipher(c,pool,len):
    '''
    Args:
    c: int (ciphertext to decrypt)
    pool: list (ciphertexts encrypted using the same key)
    len: int (length of cipher)
    
    Returns:
    decrypted_chars: bytearray (successfully decrypted bytes, unknown bytes are replaced with '-')
    key: bytearray (successfully retrieved bytes of key, unknown bytes are denoted with 0)
    
    '''
    spaces = []
    revealed = []
    
    decrypted_chars = bytearray([0x2D]*len)
    decrypted_space = bytearray([0xFF]*len)
    key = bytearray([0x0]*len)
    
    for cipher in pool:
        if c == cipher:
            continue
        sp,rv = get_spaces(c,cipher,len)
        spaces.append(sp)
        revealed.append(rv)
        decrypted_space = op_and(decrypted_space, sp)
        

    for i,space in enumerate(spaces):
        rev=revealed[i]
        valid_rev = op_xor(space,decrypted_space)
        for j,pos in enumerate(valid_rev):
            if pos==1 and rev[j]!=0:
                decrypted_chars[j]=rev[j]
                
    for i,sp in enumerate(decrypted_space):
        if sp==1:
            decrypted_chars[i] = 0x20
            
    c_bytes = int.to_bytes(c,len,'big')
    for i,byte in enumerate(decrypted_chars):
        if not(byte == 0x2D):
            key[i] = byte ^ c_bytes[i]      
            
    return decrypted_chars,key

''' 
pool=[0xA84537EC762D276D2804F0051C76FBB61DA962A904055BCF56D2E08BA3,
      0xBF4334AA672868223800E103066AA8F709AF6FEC0E105CCB52D4E691BE,
      0xB85530EE332C62612B13E7570A77ECFF12BC27EE150D51CD5FC9E19BA3, 
      0xA45527EF617F75672B12E7570676EDB608B26AEC401454CC13CBEA87A3,
      0xBF4035EB673A277B3114F0571A61FBE219B674A9120152DD5FC1FD92A9,
      0xA31022E272336B222913EB030C38FBF31FAE75EC40175ACE47D7EE8CB5]    
'''
with open('ciphertexts.txt') as f: 
    pool = [int(line,16) for line in f]

len_cipher =  (pool[0].bit_length() + 7) // 8

# PRINTS THE DECRYPTED CHARACTERS BEFORE ANY GUESSES
for i,c in enumerate(pool):
    decrypted_chars,incomplete_key = (decrypt_cipher(c,pool,len_cipher))
    print(f'message {i+1}: {decrypted_chars}')

msg_idx = int(input('Choose a message to guess (1 - 6):\n'))
guess = input('Guess the message:\n')

key=bytearray([0]*len_cipher)
msg_bytes = bytearray(bytes(guess,'utf-8'))

# if input msg is shorter than actual message length, pad it
if len(msg_bytes)<len_cipher:
    pad_len=len_cipher-len(msg_bytes)
    padding = bytearray([0]*pad_len)
    msg_bytes.extend(padding)

# deduce the missing bytes of key based on input msg 
# note that characters revealed before any guesses will not change even if user incorrectly replaced them in input msg  
# therefore, key is robust to input errors in confirmed bytes
for i,byte in enumerate(incomplete_key):
    if byte==0 and msg_bytes[i]!=0 :
        key[i] = msg_bytes[i] ^  int.to_bytes(pool[msg_idx-1],len_cipher,'big')[i]
    else:
        key[i] = byte


print('\nDECRYPTED MESSAGES')
print('------------------\n')        
        
for cipher in pool:
    cipher_bytes = int.to_bytes(cipher,len_cipher,'big')
    msg = op_xor(key,cipher_bytes)
    for i,byte in enumerate(cipher_bytes):
        if byte == msg[i]:
            msg[i]=0X2D
    print(msg)
