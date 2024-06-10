# This should be changed to just runtime if in the same directory as the files
from Files.runtime import EmoProgram
import atexit

counter = 0

def closeProg():
	print(counter)

atexit.register(closeProg)

# This should be changed to "program.emo" if in the same directory as the files
with open("Files/program.emo") as file:
	raw = file.read()
	prog = EmoProgram(raw)
	
	prog.PC = 4
	while True:
		instr = prog.P[prog.PC]
		fn = prog.EMO[instr[0]]
		fn(instr)
		if instr[0] == "📥":
			counter += 1
		prog.PC += 1