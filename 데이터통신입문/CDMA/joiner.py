from multiprocessing import Process, Pipe
import time

def t0(conn,):
    rcv = conn.recv()
    seq = []
    for x in rcv[1]:
        seq.append(rcv[0]*x)
    conn.send(seq)
    conn.close()

def t1(conn, ):
    rcv = conn.recv()
    seq = []
    for x in rcv[1]:
        seq.append(rcv[0]*x)
    conn.send(seq)
    conn.close()

def t2(conn, ):
    rcv = conn.recv()
    seq = []
    for x in rcv[1]:
        seq.append(rcv[0]*x)
    conn.send(seq)
    conn.close()

def t3(conn, ):
    rcv = conn.recv()
    seq = []
    for x in rcv[1]:
        seq.append(rcv[0]*x)
    conn.send(seq)
    conn.close()

def r0(conn,):
    seq = conn.recv()
    data = 0
    for x, y in zip(seq[0], seq[1]):
        data += x * y
    data //= 8
    print('r0: ', end='')
    if data == 1:
        print(1)
    elif data == -1:
        print(0)
    elif data == 0:
        print('silent')
    else:
        print('error')

    conn.close()

def r1(conn,):
    seq = conn.recv()
    data = 0
    for x, y in zip(seq[0], seq[1]):
        data += x * y
    data //= 8
    print('r1: ', end='')
    if data == 1:
        print(1)
    elif data == -1:
        print(0)
    elif data == 0:
        print('silent')
    else:
        print('error')

    conn.close()

def r2(conn,):
    seq = conn.recv()
    data = 0
    for x, y in zip(seq[0], seq[1]):
        data += x * y
    data //= 8
    print('r2: ', end='')
    if data == 1:
        print(1)
    elif data == -1:
        print(0)
    elif data == 0:
        print('silent')
    else:
        print('error')

    conn.close()

def r3(conn,):
    seq = conn.recv()
    data = 0
    for x, y in zip(seq[0], seq[1]):
        data += x * y
    data //= 8
    print('r3: ', end='')
    if data == 1:
        print(1)
    elif data == -1:
        print(0)
    elif data == 0:
        print('silent')
    else:
        print('error')

    conn.close()

# get bit
def get_bit():
    bit = []
    for i in range(4):
        bit.append(int(input("t{}: ".format(i))))
    # 2진수 0에는 -1, 2진수 1은 +1로 나타내어 양극성 표현
    bit = list(map(lambda x: -1 if x == 0 else 1, bit))

    return bit

# chip sequence
def get_cseq():
    seq = list(input())
    # 2진수 0에는 -1, 2진수 1은 +1로 나타내어 양극성 표현
    seq = list(map(lambda x: -1 if int(x) == 0 else 1, seq))

    return seq

def combine(seq_list):
    signal = []
    for (x, y, z, w) in zip(seq_list[0], seq_list[1], seq_list[2], seq_list[3]):
        signal.append(x+y+z+w)
    return signal

def joiner():
    # get bit signal
    t = get_bit()
    # get chip sequence
    cseq_list = []
    for i in range(4):
        print("chip sequence {}: ".format(i), end="")
        cseq = get_cseq()
        cseq_list.append(cseq)
    # t = [1, 1, -1, 1]
    # cseq_list = [[-1, -1, -1, 1, 1, -1, 1, 1],[-1, -1, 1, -1, 1, 1, 1, -1],
    #               [-1, 1, -1, 1, 1, 1, -1, -1], [-1, 1, -1, -1, -1, -1, 1, -1]]

    joiner_con = []
    transmitter_con = []
    joiner_con2 = []
    receiver_con = []

    # joiner <-> transmitter
    for idx in range(4):
        x, y = Pipe()
        joiner_con.append(x)
        transmitter_con.append(y)

    # joiner <-> receiver
    for idx in range(4):
        x, y = Pipe()
        joiner_con2.append(x)
        receiver_con.append(y)

    tprocessor = []  # transmitter processor
    rprocessor = []  # receiver processor
    seq_list = []   # transmitter에서 받은 sequence

    trn_list = [t0, t1, t2, t3]
    rcv_list = [r0, r1, r2, r3]

    # send to transmitter
    for idx in range(4):
        joiner_con[idx].send([t[idx], cseq_list[idx]])
        tprocessor.append(Process(target=trn_list[idx], args=(transmitter_con[idx], )))

    # receive from transmitter
    for idx in range(4):
        tprocessor[idx].start()
        rcv = joiner_con[idx].recv()
        seq_list.append(rcv)

    # combine signal
    signal = combine(seq_list)
    print('sending signal: ', signal)

    # send to receiver
    for idx in range(4):
        joiner_con2[idx].send([signal, cseq_list[idx]])
        rprocessor.append(Process(target=rcv_list[idx], args=(receiver_con[idx],)))
        rprocessor[idx].start()
        time.sleep(0.5)

    # deallocate
    for idx in range(4):
        tprocessor[idx].join()
        rprocessor[idx].join()





if __name__ == '__main__':
    joiner()