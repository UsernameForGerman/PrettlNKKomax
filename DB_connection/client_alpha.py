import websocket
import _thread
import time
import json
import numpy as np

import highest_pos as conn

DB_PATH = 'DatabaseServer.mdb'
KOMAX_ID = 'AAAAA'

# db_connection = conn.Position(DB_PATH)

def on_message(ws, message):

    """
    if 'status' in message and message['status'] == 2:
        if message['type'] == 'new':
            db_connection.stop_komax('delete')
            db_connection.load_task(message['text'])
        elif message['type'] == 'mix':
            pass
        elif message['type'] == 'extra':
            pass
    else:
        pass
    """
    received_data = json.loads(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("Closed")

def on_open(ws):
    def run(*args):

        for i in range(5):
            status = int(np.random.random_integers(1, 5))
            data_to_send = {
                'status': status,
            }
            json_data = json.dumps(data_to_send)
            ws.send(json_data)
            time.sleep(1)


        ws.close()
        print("thread_terminating")

    _thread.start_new_thread(run, ())

# websocket.enableTrace(True)

ws = websocket.WebSocketApp(
    "wss://komaxsite.herokuapp.com/komax_app/komax_manager/",
    on_message=on_message,
    on_error=on_error,
    on_close=on_close,
    on_open=on_open,
)

ws.run_forever()

