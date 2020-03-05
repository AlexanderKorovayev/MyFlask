import multiprocessing
import time
from datetime import datetime


def sender(conn, msgs):
    for msg in msgs:
        conn.send(msg)
        #print("Sent the message: {}".format(msg))
        #time.sleep(0.1)
        print(f'send {msg} {datetime.now().time()}')
    conn.close()


def receiver(conn):
    while True:
        msg = conn.recv()
        print(f'rec {msg} {datetime.now().time()}')
        if msg == "END":
            break
        #print("Received the message: {}".format(msg))


if __name__ == "__main__":
    # messages to be sent
    msgs = ["hello", "hey", "hru?", "END"]

    # creating a pipe
    parent_conn, child_conn = multiprocessing.Pipe()
    # creating new processes
    p1 = multiprocessing.Process(target=sender, args=(parent_conn, msgs))
    p2 = multiprocessing.Process(target=receiver, args=(child_conn,))

    # running processes
    p1.start()
    p2.start()

    # wait until processes finish
    p1.join()
    p2.join()
