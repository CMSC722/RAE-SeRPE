import pacman
import textDisplay
import graphicsDisplay
import game
import layout


class State:
    pass


def init():
    rules = pacman.ClassicGameRules()
    rules.quiet = False
    gameDisplay = graphicsDisplay.PacmanGraphics()
    beQuiet = True
    catchExceptions = False
    noKeyboard = True
    ghostType = pacman.loadAgent('RandomGhost', noKeyboard)
    ghosts = [ghostType(i + 1) for i in range(1)]
    game = rules.newGame(
        layout.getLayout('mediumClassic'), 'ReflexAgent', ghosts,
        gameDisplay, beQuiet, catchExceptions)
    gameDisplay.initialize(game.state.data)
    state = State()
    state.game = game
    return state


def render(state):
    newState = state.game.state.data
    newState._agentMoved = 0
    state.game.display.update(newState)
    newState = state.game.state.data
    newState._agentMoved = 1
    state.game.display.update(newState)


def is_accessible(state, x, y):
    walls = state.game.state.getWalls()
    if walls[x][y] == True:
        return False
    else:
        ghosts = state.game.state.getGhostPositions()
        for ghost in ghosts:
            if ghost[0] == x and ghost[1] == y:
                return False
        return True


def go_up(state):
    state.game.state = state.game.state.generateSuccessor(0, game.Directions().NORTH)
    return state


def go_down(state):
    state.game.state = state.game.state.generateSuccessor(0, game.Directions().SOUTH)
    return state


def go_left(state):
    state.game.state = state.game.state.generateSuccessor(0, game.Directions().WEST)
    return state


def go_right(state):
    state.game.state = state.game.state.generateSuccessor(0, game.Directions().EAST)
    return state


def is_done(state):
    return state.game.gameOver
