from os import popen

crib = "S"

while True:
	for guess in "1234567890qwertyuiopsdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM!@#$%^&*()_-=+{}":
		output = popen("echo '"+(crib + guess)+"' | python3 runProgram.py").read()
		length = int(output.split('\n')[-2]) - 1
		if length == len(crib) + 1:
			crib += guess
			print(crib)