import matlab.engine
import os
import datetime
import threading

thread_count = 10


def simulate(thread_id, P, I, D, simout):
    print(f"Thread[{thread_id}] START: ", datetime.datetime.now())
    simout[thread_id] = eng.eval(f"testFunction({P},{I},{D})", nargout=1)
    print(f"Thread[{thread_id}] FINISH: ", datetime.datetime.now())


if __name__ == '__main__':
    simout = [] * thread_count
    eng = matlab.engine.start_matlab()
    eng.addpath(os.getcwd())
    print(datetime.datetime.now())
    print("-"*20)
    th = [None] * thread_count
    for i in range(thread_count):
        th[i] = threading.Thread(target=simulate, args=(i, i, i, i, simout))
        th[i].setDaemon(True)
        th[i].start()

    for i in range(thread_count):
        th[i].join()

    print(datetime.datetime.now())
    print("-"*20)
    print("Array size =", len(simout))
    print("-" * 20)
    for i in range(len(simout)):
        print(simout[i])


