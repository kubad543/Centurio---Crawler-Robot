import socket
import keyboard

ip = '192.168.0.82'
port = 12345


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def polacz_z_serverem():
    print("start")

    s.connect((ip, port))

    print("Connected to server")
    

def send_data(data):
    s.send(data.encode('utf-8'))

def on_key_event(event):
    # print("wciśnięto: " + event.name)
    if event.name == 'w':
        send_data('przod')
    elif event.name == 's':
        send_data('tyl')
    elif event.name == 'a':
        send_data('lewo')
    elif event.name == 'd':
        send_data('prawo')
    elif event.name == 'space':
        send_data('hamulec')
    elif event.name == 'esc':
        send_data('koniec')
        s.close()
        exit()

if __name__ == '__main__':
    polacz_z_serverem()
    keyboard.on_press(on_key_event)
    keyboard.wait('esc')

    
