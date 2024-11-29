def brute_force_caeser_cipher(encrypted_flag):
 alphabet = "abcdefghijklmnopqrstuvwxyz"  # Define the alphabet - in this case is the latin alphabet

 length_text = len(encrypted_flag)

 for shift in range(26):
     decrypted_message = ""
     for char in encrypted_flag:
      if char in alphabet:
       new_char = chr(((ord(char) - 97 - shift) % 26) + 97) # Decrypt the character using modular arithmetic
       decrypted_message += new_char
      else:
       decrypted_message += char  # Keep non-alphabet characters unchanged
     print(f"Shift {shift}: {decrypted_message}")  # Print the result for this shift

brute_force_caeser_cipher("gvswwmrkxlivyfmgsrhnrisegl")