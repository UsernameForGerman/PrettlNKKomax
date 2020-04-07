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
KOMAX_NUMBER = 5

# db_connection = conn.Position(DB_PATH)
"""
komax_wb = load_workbook('New_excel.xlsx')
ws = komax_wb.active
komax_df = pd.DataFrame(ws.values)
komax_df.columns = komax_df.loc[0, :]
komax_df = komax_df.iloc[2:, 2:24]
komax_df.index = pd.Index(range(komax_df.shape[0]))
komax_df = komax_df[komax_df['komax'] == str(KOMAX_NUMBER)]
"""


#print(komax_df.columns)


def to_normal_int(number):
    type_number = type(number)
    if type_number is np.int64 or type_number is np.int32 or type_number is np.int16 or type_number is np.int8 or type_number is np.int_:
        return int(number)

def to_normal(value):
    type_value = type(value)
    if type_value is str or type_value is int or type_value is float or type_value is bool:
        return value
    elif type_value is np.bool_:
        return bool(value)
    else:
        return to_normal_int(value)

#print(sum(komax_df.loc[148:, :][komax_df['harness'] == '43118-3724544-45']['time']))

# d = {key: [to_normal_int(value)] for key, value in d.items()}

#print(komax_df[komax_df.isin(d).all(), :])

#komax_df[[komax_df[] == d[key]] and ]
# komax_df = None

komax_df = pd.read_excel('komax_df_{}.xlsx'.format(KOMAX_NUMBER))

def on_message(ws, message):
    global komax_df

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

    elif received_data['status'] == 2 and 'task' in received_data:
        komax_df = pd.DataFrame(received_data['task'])
        komax_df.index = pd.Index(komax_df['id'])
        # save komax_df to excel
        komax_df.to_excel('komax_df_{}.xlsx'.format(KOMAX_NUMBER))
        print(komax_df)


def on_error(ws, error):
    print(error)

def on_close(ws):
    print('closed')

def on_open(ws):
    def run(*args):
        global komax_df
        idx_to_send = 0
        while idx_to_send < komax_df.shape[0]:
            """
            if komax_df is None:
                try:
                    komax_df = pd.read_excel('komax_df_{}.xlsx'.format(KOMAX_NUMBER))
                except:
                    pass
            """
            status = 1
            if komax_df is not None:
                to_send = komax_df.iloc[idx_to_send, :].to_dict()
                for key, value in to_send.items():
                    to_send[key] = to_normal(value)
            else:
                to_send = 1

            data_to_send = {
                'status': status,
                'komax_number': KOMAX_NUMBER,
                'position': to_send,
            }
            print(data_to_send)
            json_data = json.dumps(data_to_send)
            ws.send(json_data)
            time.sleep(0.05)
            idx_to_send += 1
        else:
            while True:
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
