import websocket
import _thread
import time
import json
import numpy as np
import pandas as pd
import openpyxl as xl
from openpyxl import load_workbook


import highest_pos as conn

DB_PATH = 'DatabaseServer.mdb'
KOMAX_ID = 'AAAAA'
KOMAX_NUMBER = 3

# db_connection = conn.Position(DB_PATH)
komax_wb = load_workbook('1821.xlsx')
ws = komax_wb.active
komax_df = pd.DataFrame(ws.values)
komax_df.columns = komax_df.loc[0, :]
komax_df = komax_df.iloc[2:, 2:24]
komax_df.index = pd.Index(range(komax_df.shape[0]))
komax_df = komax_df[komax_df['komax'] == str(KOMAX_NUMBER)]

print(komax_df[:5])
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
    print(received_data)
    if received_data['status'] == 2 and 'text' in received_data and received_data['text'] == 'Requested':

        data_to_send = {
            'status': received_data['status'],
            'text': received_data['text'],
            'task': komax_df.to_dict(),
            'komax_number': KOMAX_NUMBER,
        }
        print('sending')

        ws.send(json.dumps(data_to_send))
        # ws.send('hello')


def on_error(ws, error):
    print(error)

def on_close(ws):
    print("Closed")

def on_open(ws):
    def run(*args):
        while True:
            status = 1
            data_to_send = {
                'status': status,
                'komax_number': KOMAX_NUMBER,
            }
            json_data = json.dumps(data_to_send)
            ws.send(json_data)
            time.sleep(5)


        ws.close()
        print("thread_terminating")

    _thread.start_new_thread(run, ())

# websocket.enableTrace(True)

ws = websocket.WebSocketApp(
    # "wss://komaxsite.herokuapp.com/komax_app/komax_manager/",
    "ws://localhost:8000/komax_app/komax_manager/",
    on_message=on_message,
    on_error=on_error,
    on_close=on_close,
    on_open=on_open,
)

ws.run_forever()
