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
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def manhattanDistance(state, problem):
    """Heuristica como distancida de Manhattan"""
    goal = problem.goal
    return abs(state[0] - goal[0]) + abs(state[1] - goal[1])

def euclidianDistance(state, problem):
    """Heuristica como distancia Euclidiana"""
    goal = problem.goal
    return ((state[0] - goal[0])**2 + (state[1] - goal[1])**2)**0.5

def paredes(state, problem):
    """Distancia de Manhattan com penalidade para paredes vizinhas"""
    if state == problem.goal:
        return 0
    # Numero de paredes vizinhas ao estado atual
    neighborWalls = 0
    for i in range(state[0]-1, state[0]+2):
        for j in range(state[1]-1, state[1]+2):
            neighborWalls += 1 if problem.walls[i][j] == 'T' else 0
    # Subtrai 7 que e o numero maximo de paredes vizinhas possiveis
    return neighborWalls  #dist + neighborWalls - 7

def paredes2(state, problem):
    # dist = manhattanDistance(state, problem)
    # if dist == 0:
    #     return 0
    if state == problem.goal:
        return 0
    neighborWalls = 0
    for i, j in [(1,0), (-1,0), (0,1), (0,-1)]:
        x = state[0] + i
        y = state[1] + j
        neighborWalls += 1 if problem.walls[x][y] == 'T' else 0
    return neighborWalls  #dist + neighborWalls - 3

def manhattanParedes(state, problem):
    dist = manhattanDistance(state, problem)
    if dist == 0:
        return 0
    p1 = (state[0], problem.goal[1])
    p2 = (problem.goal[0], state[1])
    walls1 = 0
    for i in range(problem.goal[0], p1[0]+1):
        walls1 += 1 if problem.walls[i][p1[1]] == 'T' else 0
    for j in range(p1[1], state[1]+1):
        walls1 += 1 if problem.walls[p1[0]][j] == 'T' else 0
    walls2 = 0
    for i in range(p2[0], state[0]+1):
        walls2 += 1 if problem.walls[i][p2[1]] == 'T' else 0
    for j in range(problem.goal[1], p2[1]+1):
        walls2 += 1 if problem.walls[p2[0]][j] == 'T' else 0
    walls = max(walls1, walls2)
    return dist + 3 * walls

def maxh(state, problem):
    heuristics = [manhattanDistance, euclidianDistance, paredes, paredes2, manhattanParedes]
    return max([h(state, problem) for h in heuristics])

class Node:
    """
    Um no da arvore de busca do algoritmo A*
    Atributos:
        state (tuple)     : Posicao do tabulaeiro no formato (x,y)
        path  (list<str>) : Lista com o caminho ate a posicao atual
        path_cost  (int)  : Custo do caminho ate o estado
        obj_cost   (int)  : Custo estimado ate estado meta (heuristica)
    """
    def __init__(self, state, path, path_cost, obj_cost):
        self.state = state
        self.path = path
        self.path_cost = path_cost
        self.obj_cost = obj_cost

    def __str__(self):
        """Transformacao em str para impressao"""
        return 'state: {}, path: {}, cost: {}'.format(self.state, self.path, self.cost)

    def __eq__(self, other):
        """Comparacao se dois nos tem estados iguais"""
        return self.state == other.state

    def getCost(self):
        """Custo total do no, somando custo de caminho e custo objetivo"""
        return self.path_cost + self.obj_cost


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    from util import PriorityQueue

    # Cria noh do estado inicial
    initial_state = problem.getStartState()
    node = Node(state=initial_state, path=[], path_cost=0, obj_cost=heuristic(initial_state, problem))

    # Fronteira
    openSet = PriorityQueue()
    openSet.push(node, node.getCost())
    # Nos explorados
    closedSet = []

    while not openSet.isEmpty():
        # Escolhe noh com menor custo
        node = openSet.pop()
        closedSet.append(node)
        # Checa se estado atual eh estado meta
        if problem.isGoalState(node.state):
            return node.path
        # Gera os filhos do estado atual
        for state, direction, cost in problem.getSuccessors(node.state):
            newNodePath = node.path + [direction]
            newNodePathCost = node.path_cost + cost
            newNode = Node(
                state=state, 
                path=newNodePath, 
                path_cost=newNodePathCost, 
                obj_cost=heuristic(state, problem)
            )
            if newNode not in closedSet:
                # Adiciona novo noh caso ainda nao exista
                # se jah existir noh atualiza o custo se o novo custo for menor
                openSet.update(newNode, newNode.getCost())

    # Caso nao encontre nenhum caminho, nao faz nada    
    return []

    # Inicializando o estado inicial de busca
    # currentState = problem.getStartState()
    # currentNode = Node(currentState, [], 0)

    # # Conjunto do estados expandidos e nao vizitados
    # openSet = PriorityQueue()
    # # Conjunto de estados ja vizitados
    # closedSet = set()

    # while not problem.isGoalState(currentNode.state):
    #     # Itera sobre os vizinhos do estado atual
    #     for state, direction, cost in problem.getSuccessors(currentNode.state):
    #         # Cria um novo no para o vizinho
    #         newNodePath = currentNode.path + [direction]
    #         newNodeCost = currentNode.cost + cost + heuristic(state, problem)
    #         newNode = Node(state, newNodePath, newNodeCost)

    #         # Adiciona ao openSet caso ainda nao tenha sido vizitado
    #         if newNode.state not in closedSet:
    #             sameNodeInOpenSet = None
    #             for _,_,node in openSet.heap:
    #                 if node.state == newNode.state:
    #                     sameNodeInOpenSet = node
    #             if sameNodeInOpenSet:
    #                 if sameNodeInOpenSet.cost > newNodeCost:
    #                     openSet.push(newNode)
    #                     openSet.update(sameNodeInOpenSet, newNodeCost)
    #             else:
    #                 openSet.push(newNode, newNodeCost)

    #     # Caminha para o novo estado com menor custo            
    #     currentNode = openSet.pop()
    #     closedSet.add(currentNode.state)

    # return currentNode.path


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
