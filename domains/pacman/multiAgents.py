# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from util import manhattanDistance
from game import Directions
import random
import util
import pdb

from game import Agent


class ReflexAgent(Agent):

    def getAction(self, gameState):
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [
            self.evaluationFunction(gameState, action) for action in legalMoves
        ]
        bestScore = max(scores)
        bestIndices = [
            index for index in range(len(scores)) if scores[index] == bestScore
        ]
        chosenIndex = random.choice(
            bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        # Useful information you can extract from a GameState (pacman.py)
        oldFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates
        ]

        totalScore = 0.0
        for ghost in newGhostStates:
            d = manhattanDistance(ghost.getPosition(), newPos)
            factor = 1
            if d <= 1:
                if ghost.scaredTimer != 0:
                    factor = -1
                    totalScore += 2000
                else:
                    totalScore -= 200

        for capsule in currentGameState.getCapsules():
            d = manhattanDistance(capsule, newPos)
            if (d == 0):
                totalScore += 100
            else:
                totalScore += 10.0 / d

        for x in xrange(oldFood.width):
            for y in xrange(oldFood.height):
                if (oldFood[x][y]):
                    d = manhattanDistance((x, y), newPos)
                    if (d == 0):
                        totalScore += 100
                    else:
                        totalScore += 1.0 / (d * d)
        return totalScore
