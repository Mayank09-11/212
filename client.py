import socket
import threading
import tkinter as tk
from tkinter import filedialog

class MusicClient:
    def __init__(self, host='127.0.0.1', port=12345):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.root = tk.Tk()
        self.root.title("Music Sharing App")

        self.chat_box = tk.Text(self.root, state='disabled')
        self.chat_box.pack()

        self.msg_entry = tk.Entry(self.root)
        self.msg_entry.pack()

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack()

        self.file_button = tk.Button(self.root, text="Send File", command=self.send_file)
        self.file_button.pack()

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        self.root.mainloop()

    def send_message(self):
        msg = self.msg_entry.get()
        self.client.send(msg.encode('utf-8'))
        self.msg_entry.delete(0, tk.END)

    def send_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.upload_file(file_path)

    def upload_file(self, file_path):
        ftp = ftplib.FTP()
        ftp.connect('127.0.0.1', 21)
        ftp.login('user', '12345')
        with open(file_path, 'rb') as file:
            ftp.storbinary(f"STOR {os.path.basename(file_path)}", file)
        ftp.quit()

    def receive_messages(self):
        while True:
            try:
                msg = self.client.recv(1024).decode('utf-8')
                self.chat_box.config(state='normal')
                self.chat_box.insert(tk.END, msg + "\n")
                self.chat_box.config(state='disabled')
            except:
                print("An error occurred!")
                self.client.close()
                break

if __name__ == "__main__":
    MusicClient()
