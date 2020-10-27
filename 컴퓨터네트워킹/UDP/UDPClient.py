from time import perf_counter, strftime
from socket import *

print("Running")
print("======================================")
serverName = '127.0.0.1'
serverPort = 12000
server = (serverName, serverPort)
clientSocket = socket(AF_INET, SOCK_DGRAM)  # create socket for connect with server
clientSocket.settimeout(1)

for i in range(10):
    message = input("Input Client Message: ")
    start = perf_counter()
    clientSocket.sendto(message.encode(), server)  # client request
    try:    # timeout exception handling
        modifiedMessage, serverAddress = clientSocket.recvfrom(1024)  # receive request from server
        end = perf_counter()
        print("Ping {:2}    RTT: {} sec".format((i+1), str(end-start)))  # calculate RTT and print
        print("Reply: " + modifiedMessage.decode())
    except timeout:  # packet loss
        print('Ping {:2}    Request timed out'.format((i+1)))
    print()
clientSocket.close()  # close socket
print("======================================")
print("Connection closed..")
