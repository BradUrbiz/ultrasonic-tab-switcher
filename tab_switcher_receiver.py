import socket
import webbrowser
import pyautogui

port = 65432  

def switch_tab():
    pyautogui.hotkey('ctrl', 'w')  
    webbrowser.open("https://www.khanacademy.org/math/precalculus/x9e81a4f98389efdf:composite/x9e81a4f98389efdf:composing/a/finding-and-evaluating-composite-functions")
    print("Tab Switched")

def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(("", port))
    server_sock.listen(1)

    print("Active")

    while True:
        try:
            client_sock, addr = server_sock.accept()
            print(f"Connected: {addr}")

            data = client_sock.recv(64).decode("utf-8").strip()
            print(f"Received: {data}")

            if data == "SWITCH":
                switch_tab()

            client_sock.close()

        except KeyboardInterrupt:
            print("Terminated")
            break
        except Exception as e:
            print(f"Error: {e}")

    server_sock.close()

main()
