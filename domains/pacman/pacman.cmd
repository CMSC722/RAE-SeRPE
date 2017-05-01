import pacman
import textDisplay
import graphicsDisplay
import game
import layout


def init(state):
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
    state.game = game
    state.score = 0
    return True


def render(state):
    newState = state.game.state.data
    newState._agentMoved = 0
    state.game.display.update(newState)
    newState = state.game.state.data
    newState._agentMoved = 1
    state.game.display.update(newState)
    return True


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
    state.score = state.game.state.getScore()
    return True


def go_down(state):
    state.game.state = state.game.state.generateSuccessor(0, game.Directions().SOUTH)
    state.score = state.game.state.getScore()
    return True


def go_left(state):
    state.game.state = state.game.state.generateSuccessor(0, game.Directions().WEST)
    state.score = state.game.state.getScore()
    return True


def go_right(state):
    state.game.state = state.game.state.generateSuccessor(0, game.Directions().EAST)
    state.score = state.game.state.getScore()
    return True


def is_done(state):
    return state.game.gameOver
