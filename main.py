import gymnasium as gym
import random
import time

PUSH_RIGHT = 1
PUSH_LEFT = 0
MAX_CART_POS = 4.8
MAX_POLE_ANGLE = 0.418


def simple_balancer(cart_pos, cart_vel, pole_angle, pole_vel, prev_vel):
    expected_position = cart_pos + cart_vel
    expected_angle = pole_angle + pole_vel
    # Normalized error for both variables
    error = (abs(expected_position) - MAX_CART_POS) / MAX_CART_POS - (abs(expected_angle) - MAX_POLE_ANGLE) / MAX_POLE_ANGLE


    if error < 0:

        if abs(expected_angle) > 0.2 * MAX_POLE_ANGLE:
            if expected_angle > 0:
                return PUSH_RIGHT
            return PUSH_LEFT

    if error > 0:

        if abs(expected_position) > 0.1 * MAX_CART_POS:
            if expected_position > 0:
                return PUSH_LEFT
            return PUSH_RIGHT

    #print('random')
    #print(cart_vel)
    print(error)
    return random.choice([PUSH_LEFT, PUSH_RIGHT])


def run_simulation(balancing_algorithm):
    env = gym.make('CartPole-v1', render_mode="human")
    observation, info = env.reset(seed=42)

    # Initialize defaults
    cart_pos, cart_vel, pole_angle, pole_vel = 0, 0, 0, 0
    prev_vel = 0

    for _ in range(1000):
       time.sleep(0.02)
       action = balancing_algorithm(cart_pos, cart_vel, pole_angle, prev_vel)
       prev_vel = cart_vel
       observation, reward, terminated, truncated, info = env.step(action)
       cart_pos, cart_vel, pole_angle, pole_vel = observation


    env.close()


if __name__ == '__main__':
    run_simulation(simple_balancer)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
