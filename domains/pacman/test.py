# simulate a RAE
from commands import *


def main():
    state = init()
    render(state)
    pause = raw_input()
    state = go_right(state)
    render(state)
    pause = raw_input()
    state = go_right(state)
    render(state)
    pause = raw_input()
    state = go_right(state)
    render(state)
    pause = raw_input()


if __name__ == '__main__':
    main()
