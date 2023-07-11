from threading import Thread
from app import create_app
import subprocess


def run_app():
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)


def open_camera():
    subprocess.call('mjpg_streamer -i "input_uvc.so" -o "output_http.so -w /usr/local/www"',shell=True)


try:
    # t1 = Thread(target=run_app, args=())
    t2 = Thread(target=open_camera, args=())
    # t1.start()
    t2.start()
except Exception as e:
    print('memory is not enough')

run_app()



