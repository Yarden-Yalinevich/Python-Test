
import socket

#'192.168.21.42'
def ip_send(token,command_name,param=None,ip=None):
    TCP_IP = "172.16.26.47" ### change the IP to the right one for the start
    TCP_PORT = 7
    BUFFER_SIZE = 1024
    if param == None:
        param_str = ''
    else:
        param_str = ''
        for k in range(len(param)):
            param_str = param_str+','+str(param[k])
    MESSAGE = str(token)+','+str(command_name)+param_str+';'
    MESSAGE_as_bytes = str.encode(MESSAGE)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE_as_bytes)
    data = s.recv(BUFFER_SIZE)
    s.close()
    return data.decode('utf-8')