# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
	"""
	This class outlines the structure of a search problem, but doesn't implement
	any of the methods (in object-oriented terminology: an abstract class).

	You do not need to change anything in this class, ever.
	"""

	def getStartState(self):
		"""
		Returns the start state for the search problem.
		"""
		util.raiseNotDefined()

	def isGoalState(self, state):
		"""
		  state: Search state

		Returns True if and only if the state is a valid goal state.
		"""
		util.raiseNotDefined()

	def getSuccessors(self, state):
		"""
		  state: Search state

		For a given state, this should return a list of triples, (successor,
		action, stepCost), where 'successor' is a successor to the current
		state, 'action' is the action required to get there, and 'stepCost' is
		the incremental cost of expanding to that successor.
		"""
		util.raiseNotDefined()

	def getCostOfActions(self, actions):
		"""
		 actions: A list of actions to take

		This method returns the total cost of a particular sequence of actions.
		The sequence must be composed of legal moves.
		"""
		util.raiseNotDefined()


def tinyMazeSearch(problem):
	"""
	Returns a sequence of moves that solves tinyMaze.  For any other maze, the
	sequence of moves will be incorrect, so only use this for tinyMaze.
	"""
	from game import Directions
	s = Directions.SOUTH
	w = Directions.WEST
	return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
	"""
	Search the deepest nodes in the search tree first.

	Your search algorithm needs to return a list of actions that reaches the
	goal. Make sure to implement a graph search algorithm.

	To get started, you might want to try some of these simple commands to
	understand the search problem that is being passed in:

	print "Start:", problem.getStartState()
	print "Is the start a goal?", problem.isGoalState(problem.getStartState())
	print "Start's successors:", problem.getSuccessors(problem.getStartState())
	"""
	ban = []
	sol = []
	stack = util.Stack()
	state = problem.getStartState()
	ban.append(state)
	if problem.getSuccessors(state) == None:
		return 0
	else:
		while(1):
			y = len(problem.getSuccessors(state))
			for x in problem.getSuccessors(state):
				if x[0] in ban:
					y -= 1
					if y == 0:
						stack.pop()
						help = stack.pop()
						sol.pop()
						state = help[0]
						stack.push(help)
				else:
					stack.push(x)
					sol.append(x[1])
					if problem.isGoalState(x[0]) == True:
						return sol
					else:
						state = x[0]
						ban.append(state)
					break

	util.raiseNotDefined()

def breadthFirstSearch(problem):
	"""Search the shallowest nodes in the search tree first."""
	queue = util.Queue()
	ban = set()
	meta = {}
	queue.push(problem.getStartState())
	meta[problem.getStartState()] = ()
	while queue:
		state = queue.pop()
		if problem.isGoalState(state):
			sol = []
			while (1):
				row = meta[state]
				if len(row) == 2:
					state = row[0]
					sol.append(row[1])
				else:
					break
			return list(reversed(sol))
		for child in problem.getSuccessors(state):
			if child[0] in ban:
				continue
			if child[0] not in queue.list:
				meta[child[0]] = (state, child[1])
				queue.push(child[0])
		ban.add(state)

	util.raiseNotDefined()

def uniformCostSearch(problem):
	"""Search the node of least total cost first."""
	queue = util.PriorityQueue()
	ban = set()
	meta = {}
	queue.push(problem.getStartState(), 1)
	meta[problem.getStartState()] = ()
	while queue:
		state = queue.pop()
		if problem.isGoalState(state):
			sol = []
			while (1):
				row = meta[state]
				if len(row) == 3:
					state = row[0]
					sol.append(row[1])
				else:
					break
			return list(reversed(sol))
		for child in problem.getSuccessors(state):
			if child[0] in ban:
				continue
			row = meta[state]
			if child[0] in meta:
				if meta[child[0]][2] < (row[2] + child[2]):
					break
				else:
					meta[child[0]] = (state, child[1], (child[2] + row[2]))
					queue.update(child[0], child[2] + row[2])
			else:
				if len(row) == 3:
					meta[child[0]] = (state, child[1], child[2] + row[2])
					queue.update(child[0], child[2] + row[2])
				else:
					meta[child[0]] = (state, child[1], child[2])
					queue.update(child[0], child[2])	
		ban.add(state)

	util.raiseNotDefined()

def nullHeuristic(state, problem=None):
	"""
	A heuristic function estimates the cost from the current state to the nearest
	goal in the provided SearchProblem.  This heuristic is trivial.
	"""
	return 0

def aStarSearch(problem, heuristic=nullHeuristic):
	"""Search the node that has the lowest combined cost and heuristic first."""
	queue = util.PriorityQueueWithFunction(nullHeuristic)
	ban = set()
	meta = {}
	queue.push(problem.getStartState())
	meta[problem.getStartState()] = ()
	while queue:
		state = queue.pop()
		if problem.isGoalState(state):
			sol = []
			while (1):
				row = meta[state]
				if len(row) == 3:
					state = row[0]
					sol.append(row[1])
				else:
					break
			return list(reversed(sol))
		for child in problem.getSuccessors(state):
			if child[0] in ban:
				continue
			row = meta[state]
			if child[0] in meta:
				if meta[child[0]][2] < (row[2] + child[2]):
					break
				else:
					meta[child[0]] = (state, child[1], child[2] + row[2] + nullHeuristic(state))
					queue.update(child[0], child[2] + row[2] + nullHeuristic(state))
			else:
				if len(row) == 3:
					meta[child[0]] = (state, child[1], child[2] + row[2] + nullHeuristic(state))
					queue.update(child[0], child[2] + row[2] + nullHeuristic(state))
				else:
					meta[child[0]] = (state, child[1], child[2])
					queue.update(child[0], child[2])	
		ban.add(state)

	util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
