"""
Manually control the agent to provide expert trajectories.
"""

from flat_game import carmunk
import numpy as np
from nn import neural_net
import curses # for keypress


NUM_SENSORS = 8
GAMMA = 0.9


def play(screen):

    car_distance = 0
    weights = [1, 1, 1, 1, 1, 1, 1, 1]# just used for the reward calculation in this run
    game_state = carmunk.GameState(weights)

    # Do nothing to get initial.
    _, state, __ = game_state.frame_step((2))

    featureExpectations = np.zeros(len(weights))

    # Move.
    while True:
        car_distance += 1
        event = screen.getch()

        if event == curses.KEY_LEFT:
            action = 3
        elif event == curses.KEY_RIGHT:
            action = 4
        elif event == curses.KEY_DOWN:
            break
        else:
            action = 2


        # Take action.
        immediateReward , state, readings = game_state.frame_step(action)
        featureExpectations += (GAMMA**(car_distance-1))*np.array(readings)
        # Tell us something.
        if car_distance % 2000 == 0:
            break

    return featureExpectations

if __name__ == "__main__":
    screen = curses.initscr()
    curses.noecho()
    curses.curs_set(0)
    screen.keypad(1)
    screen.addstr("Play the game")
    result = play(screen)
    curses.endwin()
    print (result)
