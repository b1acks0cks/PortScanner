import socket
import sys
import time

flags = sys.argv[1:]

flag_num = 0
valid_command = False
PORTS = [port for port in range(10000)]
verbose = "verbose" in flags or "-v" in flags or "-V" in flags

tcp_scan = not "no-tcp" in flags
udp_scan = "udp" in flags
if "-port" in flags or "--port" in flags:
    PORTS = []
    i = 0
    while i < len(flags):
        if flags[i] == "-port" or flags[i] == "--port":
            ports = flags[i+1]
            for port_num in ports.split(","):
                PORTS.append(int(port_num))
        i+=1

while flag_num < len(flags):
    flag = flags[flag_num]
    if flag == "ip":
        valid_command = True
        ADDR = flags[flag_num + 1]

        ### peform scan using raw sockets
        print(f"Peforming scan on host \033[036m{ADDR}\033[0m")
        time.sleep(2)
        if(tcp_scan):
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            for PORT in PORTS:
                try:
                    client.connect((ADDR, PORT))
                    print(f"\033[32m+ PORT {PORT} opened + \033[0m")
                except ConnectionRefusedError:
                    if(verbose):
                        print(f"\033[31m- PORT {PORT} closed -\033[0m")
                client.close()
        if(udp_scan):
            for PORT in PORTS:
                client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                client.settimeout(0.5)

                client.sendto(b"test", (ADDR, PORT))

                try:
                    data, addr= client.recvfrom(1024)
                    print(f"\033[32m+ PORT {PORT} opened (UDP) +\033[0m")
                except socket.timeout:
                    if verbose:
                        print(f"\033[31m- PORT {PORT} closed (UDP) -\033[0m")

        break
    if(not valid_command):
        print("Usage: python3 scan.py ip {TARGET}")
        break  