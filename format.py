import requests
import threading
import time
from flask import Flask
app = Flask(__name__)

@app.before_first_request
def activate_job():
    def run_job():
        while True:
            print("Run recurring task")
            for i in range(0,2):
               r = requests.get('http://127.0.0.1:13800/')
               print(r)
            time.sleep(1)

    thread = threading.Thread(target=run_job)
    thread.start()

@app.route("/")
def hello():
    return "started"



def start_runner():
    def start_loop():
        not_started = True
        while not_started:
            print('In start loop')
            try:
                r = requests.get('http://127.0.0.1:13800/')
                if r.status_code == 200:
                    print('Server started, quiting start_loop')
                    not_started = False
                print(r.status_code)
            except:
                print('Server not yet started')
            time.sleep(2)

    print('Started runner')
    thread = threading.Thread(target=start_loop)
    thread.start()

if __name__ == "__main__":
    start_runner()
    app.run(debug=True,port=13800)