import websocket
import _thread
import time

import highest_pos as conn

DB_PATH = 'DatabaseServer.mdb'
KOMAX_ID = 'AAAAA'

db_connection = conn.Position(DB_PATH)

def on_message(ws, message):
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


def on_error(ws, error):
    print(error)

def on_close(ws):
    print("Closed")

def on_open(ws):
    def run(*args):
        status = 1

        for i in range(10):
            current_position = db_connection.current_wire_pos()
            ws.send({'komax': KOMAX_ID, 'status': status, 'text': current_position})

            time.sleep(1)

            ws.close()

        print("thread_terminating")

    _thread.start_new_thread(run, ())

# websocket.enableTrace(True)

ws = websocket.WebSocketApp(
    "ws://localhost:8000/komax_app/komax_manager/",
    on_message=on_message,
    on_error=on_error,
    on_close=on_close,
    on_open=on_open,
)

ws.run_forever()

