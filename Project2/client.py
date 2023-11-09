#Alexander Scher
#Lab2 - Networking
#11/7/23

import socket
import struct
import sys
import time

def main():
    try:
        if len(sys.argv) == 3:
            ipAddr = sys.argv[1]
            portNum = int(sys.argv[2])
        else:
            # print(len(sys.argv))
            print("Give 2 arguments and try again")
            exit(1)
        userStr = input("Enter a string to send!\n")
        # print(x)
        #userStr = "0 1 2 3 4 5 6 7 8 9 a b c d e f g h i j k l m n o p q r s t u v w x y z !"
        chunks = [userStr[i:i+2] for i in range(0, len(userStr), 2)]
        #print(chunks)
        strEncode = userStr.encode()
        #print(strLength)
        #print(ipAddr, portNum)
        #init socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverAddress = (ipAddr, portNum)
        windowStart = 0
        windowEnd = 5
        # print(userStr[windowStart:windowEnd])
        # Send the size of the message (Message 1) to the server
        msgSize = len(strEncode)
        sock.sendto(struct.pack('!I', msgSize), serverAddress)
        acksReceived = 0
        seq_number =  0

        while len(chunks) > acksReceived:
            for i in chunks[windowStart:windowEnd]:
                header = f"{seq_number:<11}{len(i):<4}"
                full_message = header.encode() + i.encode()
                sock.sendto(full_message, serverAddress)
                seq_number += 2
            ack, _ = sock.recvfrom(1024)
            ack_num = int(ack.decode().strip())
            if ack_num != None:
                acksReceived += 1
                windowStart += 1
                if windowEnd < len(chunks):
                    windowEnd += 1
            seq_number = 2*acksReceived
            print(f"Received Ack {ack_num} for '{chunks[ack_num//2]}'")

    except SyntaxError:
        print("An error occured try again.")
    print("Done.")
    sock.close()

main()