import time

from flask import render_template
from flask import redirect
from . import main
from operation import CarOperation

car = CarOperation()
#steer = Steer(16, 13)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/control/<string:action_name>')
def action(action_name):
    if action_name == 'forward':
        print('forward')
        car.run(5,5)
        time.sleep(1)
        car.brake()
    elif action_name == 'backward':
        print('backward')
        car.back(5,5)
        time.sleep(1)
        car.brake()
    elif action_name == 'right':
        print('right')
        car.spin_right(40, 40)
        time.sleep(0.8)
        car.brake()
    elif action_name == 'left':
        print('left')
        car.spin_left(40, 40)
        time.sleep(0.8)
        car.brake()
    else:
        print('stop')
        car.brake()
    return action_name


@main.route('/action')
def action_stream():
    return redirect('http://192.168.50.1:8080/?action=stream')

"""
@main.route('/camera/<string:action_name>')
def camera(action_name):
    if action_name == 'camera_up':
        print('camera_up')
        steer.increase_angle2()
    elif action_name == 'camera_down':
        print('camera_down')
        steer.reduce_angle2()
    elif action_name == 'camera_right':
        print('camera_right')
        steer.increase_angle1()
    elif action_name == 'camera_left':
        print('camera_left')
        steer.reduce_angle1()
    else:
        print('nothing to do')
    return action_name
"""
