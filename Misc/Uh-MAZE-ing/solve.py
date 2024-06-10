from pwn import *

maze = """████████████████████████████████████████ ████████
█   █         █             █     █         █   █
███ █████ ███ ███ █████████ █ ███ █ █████ ███ █ █
█   █     █ █   █ █       █   █ █ █ █   █     █ █
█ ███ █████ ███ █ ███████ █████ █ █ █ █ ███████ █
█     █     █   █   █   █       █ █ █ █     █ █ █
███████ ███ █ █████ █ █ ███████ █ █ █████ █ █ █ █
█   █   █ █   █   █   █     █   █ █     █ █   █ █
█ █ █ ███ ███████ █████████ █ ███ █████ █ █████ █
█ █   █ █       █           █ █   █   █ █ █   █ █
█ █████ █ █ ███ █████ ███████ █ ███ █ █ █ █ █ █ █
█     █   █ █ █     █ █   █   █     █   █   █ █ █
█████ █████ █ █████ █ █ █ ███ ███████████ ███ █ █
█   █ █     █ █     █   █       █       █   █ █ █
█ ███ █ █████ █ ███████████████ █████ █ █████ █ █
█     █     █     █     █     █     █ █       █ █
█ █████ ███ █████ █ █ █ █ ███ █████ █ ███████ █ █
█   █     █   █   █ █ █ █ █   █   █   █     █ █ █
███ ███ █████ ███ ███ █ ███ ███ █ █ ███ ███ █ █ █
█ █   █ █   █   █     █   █     █   █   █   █ █ █
█ ███ ███ █ █ █ █████████ █ █████████ ███ █████ █
█ █   █   █ █ █   █     █ █       █   █ █     █ █
█ █ ███ ███ █████ █ ███ █ ███████ █ ███ █████ █ █
█ █ █   █ █ █   █ █   █ █     █   █   █ █     █ █
█ █ █ ███ █ █ █ █ ███ █ █████ █ █████ █ █ █████ █
█ █ █ █ █   █ █ █     █ █   █ █ █     █   █     █
█ █ █ █ █ ███ █ ███████ █ █ █ ███ █████ ███████ █
█     █       █         █ █       █             █
█████████████████████████████ ███████████████████"""


maze = maze.split('\n')

def solveMaze(maze):
	# Allows us to convert the direction from the current point into the next point.
	def getDirection(x, y, direction):
		if direction == 0:
			return [x, y - 1]
		elif direction == 1:
			return [x + 1, y]
		elif direction == 2:
			return [x, y + 1]
		else:
			return [x - 1, y]

	# Checks the moves possible from a given point and direction.
	def checkMoves(x, y, direction):
		# If we hit a wall, we can't do anything...
		if maze[y][x] == '█':
			return []
		else:
			# Directions: 0 up, 1 right, 2 down, 3 left
			checkStraight = direction
			checkLeft = (direction - 1) % 4
			checkRight = (direction + 1) % 4
			moves = []
			
			# Check moves just going straight (note that we need to check that the new point is possible first)
			checkX, checkY = getDirection(x, y, checkStraight)
			if checkY < len(maze) and checkY >= 0 and checkX < len(maze[0]) and checkX >= 0 and maze[checkY][checkX] != '█':
				moves.append([checkX, checkY, checkStraight])
			
			# Check for going left
			checkX, checkY = getDirection(x, y, checkLeft)
			if checkY < len(maze) and checkY >= 0 and checkX < len(maze[0]) and checkX >= 0 and  maze[checkY][checkX] != '█':
				moves.append([checkX, checkY, checkLeft])
				
			# Check for going right
			checkX, checkY = getDirection(x, y, checkRight)
			if checkY < len(maze) and checkY >= 0 and checkX < len(maze[0]) and checkX >= 0 and  maze[checkY][checkX] != '█':
				moves.append([checkX, checkY, checkRight])
			
			# Return all our possible moves from this point (can contain straight, left, or right)
			return moves

	# Now for actually solving this maze!
	
	# First, we need to find our starting point. We know it's on the first row, but need to find the x.
	startX = 0
	# We always need to check going down, so we'll go ahead and do that until we get an x that works!
	while len(checkMoves(startX, 0, 2)) == 0:
		startX += 1

	# We'll start at our starting point, going down. The last item of our first coordinate is the path followed which is empty at the start.
	coords = [[startX, 0, 2, []]]
	# Saves if we have a solution.
	solutionFound = False
	# Saves what the solution is
	soln = 0
	while not solutionFound:
		# This list stores our new coordinates that will then become the coordinates for the next iteration
		new_coords = []
		# Loop through the positions we're at right now
		for x, y, direction, path in coords:
			# If we're at the bottom of the maze, we have our solution!
			if y == len(maze) - 1:
				soln = path + [[x,y]]
				solutionFound = True
				break
			# But if we don't have it yet...
			
			# Adds our current point to the saved path
			new_path = path + [[x, y]]
			
			# Loop through possible moves and add them to new_coords
			for move in checkMoves(x, y, direction):
				new_coords.append(move + [new_path])
		# Set coords to new_coords for next iteration
		coords = new_coords
	
	# Format output and return
	output = ",".join(f"({x},{y})" for x,y in soln)
	return output

# Test maze:
output = solveMaze(maze)
print(output)
print("(40,0),(40,1),(41,1),(41,2),(41,3),(42,3),(43,3),(44,3),(45,3),(45,2),(45,1),(46,1),(47,1),(47,2),(47,3),(47,4),(47,5),(47,6),(47,7),(47,8),(47,9),(47,10),(47,11),(47,12),(47,13),(47,14),(47,15),(47,16),(47,17),(47,18),(47,19),(47,20),(47,21),(47,22),(47,23),(47,24),(47,25),(47,26),(47,27),(46,27),(45,27),(44,27),(43,27),(42,27),(41,27),(40,27),(39,27),(39,26),(39,25),(40,25),(41,25),(41,24),(41,23),(42,23),(43,23),(44,23),(45,23),(45,22),(45,21),(44,21),(43,21),(42,21),(41,21),(41,20),(41,19),(42,19),(43,19),(43,18),(43,17),(42,17),(41,17),(40,17),(39,17),(39,18),(39,19),(38,19),(37,19),(37,20),(37,21),(36,21),(35,21),(35,22),(35,23),(36,23),(37,23),(37,24),(37,25),(36,25),(35,25),(34,25),(33,25),(33,26),(33,27),(32,27),(31,27),(30,27),(29,27),(29,28)")
print(output == "(40,0),(40,1),(41,1),(41,2),(41,3),(42,3),(43,3),(44,3),(45,3),(45,2),(45,1),(46,1),(47,1),(47,2),(47,3),(47,4),(47,5),(47,6),(47,7),(47,8),(47,9),(47,10),(47,11),(47,12),(47,13),(47,14),(47,15),(47,16),(47,17),(47,18),(47,19),(47,20),(47,21),(47,22),(47,23),(47,24),(47,25),(47,26),(47,27),(46,27),(45,27),(44,27),(43,27),(42,27),(41,27),(40,27),(39,27),(39,26),(39,25),(40,25),(41,25),(41,24),(41,23),(42,23),(43,23),(44,23),(45,23),(45,22),(45,21),(44,21),(43,21),(42,21),(41,21),(41,20),(41,19),(42,19),(43,19),(43,18),(43,17),(42,17),(41,17),(40,17),(39,17),(39,18),(39,19),(38,19),(37,19),(37,20),(37,21),(36,21),(35,21),(35,22),(35,23),(36,23),(37,23),(37,24),(37,25),(36,25),(35,25),(34,25),(33,25),(33,26),(33,27),(32,27),(31,27),(30,27),(29,27),(29,28)")


# Our actual solver:
r = remote("0.cloud.chals.io", 12743)


print(r.recvuntil("Here we go...").decode())

for _ in range(100):
	maze = r.recvuntil(">").decode()
	print(maze)
	maze = maze.split('\n')
	maze = list(filter(lambda x: '█' in x, maze))
	maze = [x.strip() for x in maze]
	r.write(solveMaze(maze).encode() + b'\n')

r.interactive()