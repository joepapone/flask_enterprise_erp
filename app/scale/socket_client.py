import socket

# web socket cliente
def conn_socket()-> bytes:
    '''
    Connect to socket server from sending and receiving data.
    '''
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_data = None

    try:
        client.connect(('0.0.0.0', 8080))
        client.send(bytes('get','UTF-8'))
        server_data = client.recv(4096)
        client.close()
    
    except socket.error as e:
        print('Failure {}\n'.format(e))

    return server_data