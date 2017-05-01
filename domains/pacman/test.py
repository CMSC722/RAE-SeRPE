# simulate a RAE
import imp
pacman = imp.load_source('foobar', 'pacman.cmd')

class State:
    pass

def main():
    state = State()
    pacman.init(state)
    pacman.render(state)
    pause = raw_input()
    pacman.go_right(state)
    pacman.render(state)
    pause = raw_input()
    pacman.go_right(state)
    pacman.render(state)
    pause = raw_input()
    pacman.go_right(state)
    pacman.render(state)
    pause = raw_input()


if __name__ == '__main__':
    main()
