DECRYPTED CIPHERTEXTS:
M1: Buffer overruns are dangerous
M2: Use two factor authentication
M3: Read secure coding guidelines
M4: Never reuse one time pad keys
M5: Update your systems regularly
M6: I shall write secure software


APPROACH:

ASCII value of space = 20 HEX / 32 DEC
ASCII values of lowercase letters start at 61 HEX / 97 DEC
ASCII values of uppercase letters start at 41 HEX / 65 DEC
c1 xor c2 = m1 xor m2
If a space exists in one message, xoring its byte with a byte from another message results in:
    1. a byte that is greater than 40 HEX / 64 DEC
    2. SPECIAL CASE: if it coincides that a space exists in the same pos in both strings, xoring them results in 0.
       NOTE: This is not the only case where the xored byte would be 0. If both strings contained the same char in
       the same position, then it would result in a 0 as well. In this case, to detect if the message really contained
       a space in that position, we obtain a space vector for the target ciphertext with each other ciphertext. A space 
       vector contains 1 in potential space positions that satisfy any of the 2 mentioned cases, 0 otherwise. We can then
       get the AND operation of all those space vectors to obtain the final spaces decided for the target ciphertext.
       
       
AUTOMATIC OUTPUT BEFORE ANY GUESSES (14 chars in each message):
message 1: bytearray(b'-u-fer o---r-ns --e d---e----')
message 2: bytearray(b'-s- two ---t-r a--hen---a----')
message 3: bytearray(b'-e-d sec--- -odi-- gu---l----')
message 4: bytearray(b'-e-er re--- -ne --me --- ----')
message 5: bytearray(b'-p-ate y--- -yst--s r---l----')
message 6: bytearray(b'- -hall ---t- se--re ---t----')


I used the input prompt several times to guess one full message:

1. Guessed 'I' as the first word in message 6. This was easy because only limited characters can fit here.
   This revealed the first column of chars in all messages.
   OUTPUT:
    bytearray(b'Bu-fer o---r-ns --e d---e----')
    bytearray(b'Us- two ---t-r a--hen---a----')
    bytearray(b'Re-d sec--- -odi-- gu---l----')
    bytearray(b'Ne-er re--- -ne --me --- ----')
    bytearray(b'Up-ate y--- -yst--s r---l----')
    bytearray(b'I -hall ---t- se--re ---t----')
   
2. Guessed 'Buffer' as the first word in message 1. There was only one missing char, 'f' which was straightforward.
   This revealed the first 6 chars in all messages.
   OUTPUT:
    bytearray(b'Buffer o---r-ns --e d---e----')
    bytearray(b'Use two ---t-r a--hen---a----')
    bytearray(b'Read sec--- -odi-- gu---l----')
    bytearray(b'Never re--- -ne --me --- ----')
    bytearray(b'Update y--- -yst--s r---l----')
    bytearray(b'I shall ---t- se--re ---t----')
    
3. Guessed 'one time pad' in message 4 (the input expects a sentence, so i filled the second word with random chars (re---)=>(rexyz))
   I already knew the first word was 'Never' from step 2.
   OUTPUT:
    bytearray(b'Buffer o{omruns are dange----')
    bytearray(b'Use two kk|tor authentica----')
    bytearray(b'Read secxxz coding guidel----')
    bytearray(b'Never rexyz one time pad ----')
    bytearray(b'Update yb\x7fm systems regul----')
    bytearray(b'I shall zxvte secure soft----')
    
4. Message 2 became obvious. (Use two kk|tor authentica----) => (Use two factor authentication)

5. Input guessed message 2 and check if all other messages made sense.
   OUTPUT:
    bytearray(b'Buffer overruns are dangerous')
    bytearray(b'Use two factor authentication')
    bytearray(b'Read secure coding guidelines')
    bytearray(b'Never reuse one time pad keys')
    bytearray(b'Update your systems regularly')
    bytearray(b'I shall write secure software')