from multiprocessing import Process, Pipe
import time

def t0(conn,):
    '''
    transmitter process t0
    :param conn: entrance of pipeline to process joiner
    :return: none
    '''
    # receive data from joiner
    rcv = conn.recv()   # rcv[0] = (1, -1) bit data to be sent by t0, rcv[1] = t0's chip sequence
    # calculate m-chip vectors for t0 (if rcv[0]==1 then positive, else negative)
    seq = encode(rcv[0], rcv[1])
    conn.send(seq)  # send m-chip vectors to joiner
    conn.close()    # close pipeline

def t1(conn, ):
    '''
    transmitter process t1
    :param conn: entrance of pipeline to process joiner
    :return: none
    '''
    rcv = conn.recv()   # receive data from joiner
    # rcv[0] = (1, -1) bit data to be sent by t1, rcv[1] = t1's chip sequence
    # calculate m-chip vectors for t1 (if rcv[0]==1 then positive, else negative)
    seq = encode(rcv[0], rcv[1])
    conn.send(seq)  # send m-chip vectors to joiner
    conn.close()    # close pipeline


def t2(conn, ):
    '''
    transmitter process t2
    :param conn: entrance of pipeline to process joiner
    :return: none
    '''
    rcv = conn.recv()   # receive data from joiner
    # rcv[0] = (1, -1) bit data to be sent by t2, rcv[1] = t2's chip sequence
    # calculate m-chip vectors for t2 (if rcv[0]==1 then positive, else negative)
    seq = encode(rcv[0], rcv[1])
    conn.send(seq)  # send m-chip vectors to joiner
    conn.close()    # close pipeline

def t3(conn, ):
    '''
    transmitter process t3
    :param conn: entrance of pipeline to process joiner
    :return: none
    '''
    rcv = conn.recv()   # receive data from joiner
    # rcv[0] = (1, -1) bit data to be sent by t3, rcv[1] = t3's chip sequence
    # calculate m-chip vectors for t3 (if rcv[0]==1 then positive, else negative)
    seq = encode(rcv[0], rcv[1])
    conn.send(seq)  # send m-chip vectors to joiner
    conn.close()    # close pipeline

def r0(conn,):
    '''
    receiver process r0
    :param conn: entrance of pipeline to process joiner
    :return: none
    '''
    seq = conn.recv()   # receive data from joiner
    # rcv[0] = m-bit chip vectors from t0, rcv[1] = t0's chip sequence
    print('r0: ', decode(seq[0], seq[1]))
    conn.close()

def r1(conn,):
    seq = conn.recv()   # receive data from joiner
    # rcv[0] = m-bit chip vectors from t1, rcv[1] = t1's chip sequence
    print('r1: ', decode(seq[0], seq[1]))
    conn.close()

def r2(conn,):
    seq = conn.recv()   # receive data from joiner
    # rcv[0] = m-bit chip vectors from t2, rcv[1] = t2's chip sequence
    print('r2: ', decode(seq[0], seq[1]))
    conn.close()


def r3(conn,):
    seq = conn.recv()   # receive data from joiner
    # rcv[0] = m-bit chip vectors from t3, rcv[1] = t3's chip sequence
    print('r3: ', decode(seq[0], seq[1]))
    conn.close()


def encode(x, cseq):
    # calculate m-chip vectors for t3 (if rcv[0]==1 then positive, else negative)
    seq = []
    for y in cseq:
        seq.append(x*y)
    return seq


def decode(mc, cseq):
    '''
    :param mc: m-bit chip vector
    :param cseq: chip sequence
    :return: recoverd bit(1, 0) else silent, error
    '''
    data = 0
    # Bit extraction through dot product
    for x, y in zip(mc, cseq):
        data += (x*y)
    data //= 8
    if data == 1:
        return 1
    elif data == -1:    # cause bioplar expression
        return 0
    elif data == 0:     # not sent
        return "silent"
    else:
        "Error"

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

# combine all signals from transmitter in joiner
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

    # # for test
    # t = [1, 1, -1, 1]
    # cseq_list = [[-1, -1, -1, 1, 1, -1, 1, 1],[-1, -1, 1, -1, 1, 1, 1, -1],
    #               [-1, 1, -1, 1, 1, 1, -1, -1], [-1, 1, -1, -1, -1, -1, 1, -1]]

    # pipeline joiner <-> transmitter
    joiner_con = []
    transmitter_con = []

    for idx in range(4):
        x, y = Pipe()
        joiner_con.append(x)
        transmitter_con.append(y)

    # pipeline joiner <-> receiver
    joiner_con2 = []
    receiver_con = []

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