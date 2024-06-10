# Example character set for the flag
charset = "1234567890~!@#$%^&*()_-=+{}qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"

# Initialize lists for flag, polynomial 1, and polynomial 2:
# Flag has degree 30, so length 31
f = [0] * 31
# Polynomials have degree 10, so length 11
a1 = [0] * 11
a2 = [0] * 11

# Define highest degree terms
# Highest degree character of flag is 125
f[30] = 125
# Highest degree of first polynomial is 1
a1[10] = 1
# Highest degree of second polynomial is 14
a2[10] = 14

# Initialize our two output polynomials, using the coefficients from left to right
c1 = [125, 358, 577, 1299, 1316, 1164, 1029, 1095, 1309, 5569, 5170, 5290, 5240, 4826, 4570, 4644, 4658, 4663, 4593, 4821, 4592, 5335, 5044, 2946, 3597, 3400, 3750, 4394, 5228, 4881, 5021, 3911, 4993, 3154, 2524, 2995, 3136, 3237, 2735, 2896, 92]
c2 = [1750, 1512, 1429, 1821, 1724, 1785, 1186, 1284, 1633, 1641, 1215, 1178, 1408, 1256, 355, 786, 815, 726, 921, 1289, 1437, 1461, 941, 1557, 1023, 606, 1104, 1037, 1073, 555, 965, -100, -163, -304, -325, -298, -488, -107, -106, -209, -351]

# Define function to get the known components for a1 to then subtract from our output coefficent
# Requires the current degree as parameter
def getBetween1(curr_num):
	# Variable to accumulate sum of terms
	acc = 0
	# Stores index of flag, which starts at 29 since index 30 is multiplied by our unknown coefficient of a1
	fptr = 29
	# Stores index of a1 to get the current degree when multiplied by the given term of the flag
	aptr = curr_num - 29
	# Loop through the inside known terms
	# 39 - curr_num is used because the highest degree term is multiplied by our unknown coefficient of a1 and the constant is multiplied by the highest degree term of the flag, so we need 41 - 2 = 39 coefficients at a maximum, and less for higher degrees at the current step
	for i in range(39 - curr_num):
		# Add product of terms of a1 and flag to accumulator
		acc += a1[aptr] * f[fptr]
		# Increment aptr (goes from 0 to 10)
		aptr += 1
		# Decrement fptr (Goes from 29 to 0, except only to 19 because of limit on a)
		fptr -= 1
	# Return final sum
	return acc
	
# Define function to get the known components for a2 to then subtract from our output coefficent
# Requires the current degree as parameter
def getBetween2(curr_num):
	# Variable to accumulate sum of terms
	acc = 0
	# Stores index of flag, which starts at 29 since index 30 is multiplied by our unknown coefficient of a2
	fptr = 29
	# Stores index of a2 to get the current degree when multiplied by the given term of the flag
	aptr = curr_num - 29
	# Loop through the inside known terms
	# 39 - curr_num is used because the highest degree term is multiplied by our unknown coefficient of a2 and the constant is multiplied by the highest degree term of the flag, so we need 41 - 2 = 39 coefficients at a maximum, and less for higher degrees at the current step
	for i in range(39 - curr_num):
		# Add product of terms of a2 and flag to accumulator
		acc += a2[aptr] * f[fptr]
		# Increment aptr (goes from 0 to 10)
		aptr += 1
		# Decrement fptr (Goes from 29 to 0, except only to 19 because of limit on a)
		fptr -= 1
	# Return final sum
	return acc

# Calculate multiplied random polynomials

# Start at degree 39 since 40 is already solved
n = 39

# 10 iterations for 10 more unknown polynomial coefficients
for _ in range(10):
	# Get right hand side of first polynomial equation times 14
	# Multiplying by 14 makes the equation even for elimination
	compare1 = 14 * (c1[40 - n] - getBetween1(n))
	# Get right hand side of second polynomial equation
	compare2 = (c2[40 - n] - getBetween2(n))
	# Get difference in two equations divided by 125 for simplicity
	# This is equal to 14a1 - a2
	compareTotal = (compare1 - compare2) // 125
	
	# Guess character starting outside of the character set
	tempChar = ord("`")
	# Random value to start at for the polynomial coefficient
	tempVal = -10
	# Loop until a valid character and in the given charset
	while tempChar > 256 or tempChar < 2 or chr(tempChar) not in charset:
		# Find character using first equation
		tempChar = (compare1 // 14) - (125 * tempVal)
		# Increment tempVal to test the next value
		tempVal += 1
	
	# Decrement tempVal to get the working value
	tempVal -= 1
	# Print the new character for debugging
	print("New char:", tempChar, chr(tempChar))
	
	# Set character of flag
	f[n - 10] = tempChar
	# Set coefficients of polynomials
	a1[n - 30] = tempVal
	a2[n - 30] = 14 * tempVal - compareTotal
	# Decrease degree
	n -= 1

# Get rest of flag from polynomials
for _ in range(20):
	# Accumulator to add the inner terms
	acc = 0
	# There are 10 known terms of the product of the two polynomials at this degree
	for i in range(10):
		# Add product of coefficients in corresponding terms
		acc += a1[i] * f[n - i]
	
	# Set flag character
	f[n - 10] = (c1[40 - n] - acc)
	# Decrease degree
	n -= 1
	
# Print the flag
print("Flag:", "".join(map(chr, f)))