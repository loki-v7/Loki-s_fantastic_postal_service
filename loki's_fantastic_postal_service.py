# FROM loki:
# to make your job easier i will explan how my code works (for once)


import socket # this is the socket libray im importing here is the link for the functions and stuff --> https://docs.python.org/3/library/socket.html

class Connection:
    def __init__(self, name, ip_addr, port, file): # I accept a name to keep track of who sent what
        self.name = name
        self.ip_addr = ip_addr
        self.port = port
        self.file = file

    # the Server and client is almost two diffrent files in one file because in a lot of youtube tutorials they make them seprate
    def Server(self, instance):

        # making socket for connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET is for internet connection and SOCK_STREAM is for TCP connecting

        s.bind((instance.ip_addr, instance.port)) #pretty self-explanatory

        # connecting
        s.listen()
        client, addr = s.accept()

        # this recives name of file and sender as well as the data in the file

        file_name = client.recv(1024).decode() # recv is recive 1024 bytes and decode them
        client.send('True'.encode()) # this is to check and interupt if the conection was completed

        sender_name = client.recv(1024).decode()
        client.send('True'.encode())

        file_data = client.recv(1024).decode()

        print(f'{str(sender_name)} has sent {file_name}')

        #opening file to write the data in
        file = open(file_name, 'w')
        while file_data:
            if not file_data: #checks if file_data exist
                break
            else:
                file.write(file_data)
                file_data = client.recv(1024).decode()

        # gotta close conections!!!
        file.close()
        client.close()
        s.close()

    def Client(self, instance):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect to the server
        client.connect((instance.ip_addr, instance.port))

        #send the stuff and encode it
        client.send(f'{instance.file}'.encode())
        check_1 = client.recv(1024).decode()

        client.send(instance.name.encode())
        check_2 = client.recv(1024).decode()

        # open named file and send data
        file = open(instance.file, 'r')
        data = file.read()
        while data:
            client.send(str(data).encode())
            data = file.read()

        #close the connections
        file.close()
        client.close()



def make_connection():
    print('''##       ######## ########   ######  
##       ##       ##     ## ##    ## 
##       ##       ##     ## ##       
##       ######   ########   ######  
##       ##       ##              ## 
##       ##       ##        ##    ## 
######## ##       ##         ######  \nmade by: loki\n''')
    name = input('enter name: ')
    ip_addr = input('enter ip: ').strip()
    port = int(input('enter port: '))
    recvorsend = input('recv or send?: ').lower().strip()


    if recvorsend == 'recv':
        con1 = Connection(name, ip_addr, port, '') #if listening no need for file name!
        con1.Server(con1) # this calls the function and uses the instance as the variable insted of typing the parameters
    else:
        file = input('filename: ')
        con1 = Connection(name, ip_addr, port, file)
        con1.Client(con1)
def main():
    ansr = 'y'
    while ansr == 'y':
        make_connection()
        ansr = input('would you like to send another file?\n[y,n]: ').strip().lower()
        if ansr == 'y':
            make_connection()
        else:
            ansr = 'n'

if __name__ == '__main__':
    main()