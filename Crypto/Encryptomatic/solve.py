from pwn import *
from string import printable
r = remote("0.cloud.chals.io", 28962)

# Block length is always 16 for AES-ECB
block_length = 16

# Function to test a plaintext attack
# Takes in connection, crib (known plaintext), block length, and total length
def test_crib(r, crib, l, end = 32):
	# Pad input with "a" character and add our guess
	plaintext = "a" * (l - len(crib)) + crib
	# Write our control plaintext to the TCP connection
	r.write(plaintext.encode() + b'\n')
	# Get first characters of returned ciphertext as control
	control = r.recv().decode().split(': ')[1].split("\n")[0][0:end]
	
	# Now, another input without our guess
	# Instead of our guess, the end of the block will be letters from the flag, which we can compare
	plaintext = "a" * (l - len(crib))
	# Write our test plaintext to the TCP connection
	r.write(plaintext.encode() + b'\n')
	# Get first characters of ciphertext as test case
	test_dat = r.recv().decode().split(': ')[1].split("\n")[0][0:end]
	
	# If our control is equal to our test case, we have a good guess!
	return control == test_dat

# Initialize our guess
crib = ""
# Variable to store the number of characters
enc_chars = 0
# Assuming the flag is less than 32 characters, we'll only need 2 blocks of 16 characters
for j in range(2):
	# Add the number of characters in the ciphertext block size (32 chars for 16 bytes of hex)
	enc_chars += 32
	# Loop through our block size
	for i in range(block_length):
		# Print progress for debugging
		print("Progress:", crib)
		# Loop through possible printable characters for the next character
		for curr_char in printable:
			# Store our temporary testing plaintext guess for the flag (current progress + new test character)
			curr_crib = crib + curr_char
			# Test our guess, and if it's right, we have more progress!
			# The block length needs to be multiplied by the number of blocks to account for the second block
			if test_crib(r, curr_crib, block_length * (enc_chars // 32), enc_chars):
				crib = curr_crib
				break

# Print our flag:
print("Flag:", crib)