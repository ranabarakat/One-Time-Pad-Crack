# One-Time Pad Crack

## Background
The one-time pad is a cryptographic technique known for its theoretical security when used correctly. It involves the encryption of messages using a secret key that is at least as long as the plaintext. Each character in the plaintext is XORed with the corresponding character in the key, resulting in a ciphertext.

The key is crucial in the one-time pad encryption. It must be random, used only once, and kept secret. The fundamental principle behind the one-time pad's security is that if the key is truly random and used only once, it becomes computationally infeasible for an adversary to decrypt the ciphertext without the key.

However, the problem arises when the same key is used to encrypt multiple messages. In such a scenario, the security of the one-time pad is compromised. If two ciphertexts are generated using the same key, an attacker can XOR those ciphertexts to cancel out the key, revealing the XOR of the two plaintexts. If the plaintexts are in English or another known language, this XORed result can be analyzed to potentially recover parts of the plaintexts, including spaces and common letters.

## Problem Statement
In this challenge, there are six English sentences encrypted using a one-time pad with the same key. They are provided in `ciphertexts.txt` in hexadecimal format. All the sentences have the same length and contain only English letters and spaces. The task is to decrypt the complete plaintexts and deduce the key used for encryption.

## Constraints

- The ciphertexts use hexadecimal representation.
- The length of each ciphertext is the same, containing both English letters and spaces.
- Punctuation and special characters were not used in the plaintexts.

## Approach

Started by understanding the properties of XOR operations on ASCII values. Specifically, I noted that:

- The ASCII value of a space is 0x20 or 32 in decimal.
- The ASCII values of lowercase letters start at 0x61 or 97 in decimal.
- The ASCII values of uppercase letters start at 0x41 or 65 in decimal.
- XORing two ciphertexts c1 and c2 results in a plaintext m1 XOR m2.
- If a space exists in one message, xoring its byte with a byte from another message results in:
    1. A byte that is greater than 0x40 or 64 in decimal.
    2. A special case where if a space exists in the same position in both messages, xoring them results in 0.
        - This is not the only case where the xored byte would be 0. If both strings contained the same char in the same position, then it would result in a 0 as well.

- Identified potential space positions and used these to reveal letters in other sentences. Determined the possible locations of spaces using the two cases above on each byte.

- Calculated a space vector for each target ciphertext by comparing it with each of the other ciphertexts. The space vector contained 1 in potential space positions, and 0 in other positions.

- Applied the AND operation on all space vectors to obtain the final spaces for the target ciphertext.

- Iterated this process to reveal spaces and characters in all ciphertexts. I guessed the remaining characters only at the end.


  
__Automatic output before any guesses (14 chars in each message):__
```
message 1: bytearray(b'-u-fer o---r-ns --e d---e----')

message 2: bytearray(b'-s- two ---t-r a--hen---a----')

message 3: bytearray(b'-e-d sec--- -odi-- gu---l----')

message 4: bytearray(b'-e-er re--- -ne --me --- ----')

message 5: bytearray(b'-p-ate y--- -yst--s r---l----')

message 6: bytearray(b'- -hall ---t- se--re ---t----')
```


__I used the input prompt several times to guess one full message:__

1. Guessed 'I' as the first word in message 6. This was easy because only limited characters can fit here.
   This revealed the first column of chars in all messages.
   
   Output:
   ```
    bytearray(b'Bu-fer o---r-ns --e d---e----')
    bytearray(b'Us- two ---t-r a--hen---a----')
    bytearray(b'Re-d sec--- -odi-- gu---l----')
    bytearray(b'Ne-er re--- -ne --me --- ----')
    bytearray(b'Up-ate y--- -yst--s r---l----')
    bytearray(b'I -hall ---t- se--re ---t----')
   ```
   
3. Guessed 'Buffer' as the first word in message 1. There was only one missing char, 'f' which was straightforward.
   This revealed the first 6 chars in all messages.
   
   Output:
   ```
    bytearray(b'Buffer o---r-ns --e d---e----')
    bytearray(b'Use two ---t-r a--hen---a----')
    bytearray(b'Read sec--- -odi-- gu---l----')
    bytearray(b'Never re--- -ne --me --- ----')
    bytearray(b'Update y--- -yst--s r---l----')
    bytearray(b'I shall ---t- se--re ---t----')
   ```
    
5. Guessed 'one time pad' in message 4 (the input expects a sentence, so i filled the second word with random chars (re---)=>(rexyz))
   I already knew the first word was 'Never' from step 2.
   
   Output:
   ```
    bytearray(b'Buffer o{omruns are dange----')
    bytearray(b'Use two kk|tor authentica----')
    bytearray(b'Read secxxz coding guidel----')
    bytearray(b'Never rexyz one time pad ----')
    bytearray(b'Update yb\x7fm systems regul----')
    bytearray(b'I shall zxvte secure soft----')
   ```
    
7. Message 2 became obvious. (Use two kk|tor authentica----) => (Use two factor authentication)

8. Input guessed message 2 and check if all other messages made sense.
   
   Output:
   ```
    bytearray(b'Buffer overruns are dangerous')
    bytearray(b'Use two factor authentication')
    bytearray(b'Read secure coding guidelines')
    bytearray(b'Never reuse one time pad keys')
    bytearray(b'Update your systems regularly')
    bytearray(b'I shall write secure software')
   ```

## Results

Using this approach, I was able to obtain all six plaintext messages:

1. Buffer overruns are dangerous
2. Use two factor authentication
3. Read secure coding guidelines
4. Never reuse one-time pad keys
5. Update your systems regularly
6. I shall write secure software

