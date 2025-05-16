import json
import re
import socket
import subprocess

class Main:
    def __init__(self):
        self.BUFFER_SIZE = 1024*1024
        self.rcv_buff = bytearray(self.BUFFER_SIZE)
        self.send_buff = []
        self.monitor_socket = None
        self.play_mode_list = []
        self.play_mode=None
        self.time=None
        self.score_left=0
        self.score_right=0
        self.rcssserver3d=None
        self.left_team=None
        self.right_team=None

    def init_monitor_socket(self):
        config = self.get_config()
        server_ip = config['monitor']['ip']
        server_port = config['monitor']['port']
        self.monitor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.monitor_socket.connect((server_ip, server_port))
        except Exception as e:
            print("发生错误：", e)
            exit(-1)

    def run_rcssserver3d(self):
        server_proc = subprocess.Popen(["rcssserver"])

    def run_left_team(self):
        pass

    def run_right_team(self):
        pass

    def receive(self):
        try:
            if self.monitor_socket.recv_into(self.rcv_buff, nbytes=4) != 4:
                raise ConnectionResetError()
            msg_size = int.from_bytes(self.rcv_buff[:4], byteorder='big', signed=False)
            if self.monitor_socket.recv_into(self.rcv_buff, nbytes=msg_size, flags=socket.MSG_WAITALL) != msg_size:
                raise ConnectionResetError()
            return self.rcv_buff[:msg_size]
        except ConnectionResetError:
            print("\nError: socket was closed by rcssserver3d!")
            exit()

    def get_config(self):
        with open("config.json", "r") as f:
            config = json.load(f)
            return config

    def send(self, msg):
        try:
            self.monitor_socket.send((len(msg)).to_bytes(4, byteorder='big') + msg)
        except Exception as e:
            print("发生错误：", e)

    def parse(self, text):
        # print(text)
        play_modes_match = re.search(r'play_modes\s+(.*?)$', text)
        play_modes_list = play_modes_match.group(1).split() if play_modes_match else []
        if len(play_modes_list) > 0:
            self.play_mode_list = play_modes_list
        play_mode_match = re.search(r'play_mode\s+(\d+)', text)
        play_mode_index = int(play_mode_match.group(1)) if play_mode_match else None
        play_mode_name = self.play_mode_list[play_mode_index] if play_mode_index is not None and play_mode_index < len(
            self.play_mode_list) else None
        time_match = re.search(r'time\s+([\d.]+)', text)
        time_value = float(time_match.group(1)) if time_match else None
        score_left_match = re.search(r'score_left\s+(\d+)', text)
        score_left = int(score_left_match.group(1)) if score_left_match else None
        score_right_match = re.search(r'score_right\s+(\d+)', text)
        score_right = int(score_right_match.group(1)) if score_right_match else None
        self.play_mode=play_mode_name if play_mode_name else self.play_mode
        self.time=round(time_value,1) if time_value is not None else self.time
        self.score_left=score_left if score_left is not None else self.score_left
        self.score_right=score_right if score_right is not None else self.score_right


if __name__ == '__main__':
    m = Main()
    m.init_monitor_socket()
    m.send(b"(reqfullstate)")
    while True:
        text = m.receive()
        m.parse(text.decode('ascii'))
        print(f"\rplayMode:{m.play_mode},time:{m.time},score_left:{m.score_left},score_right:{m.score_right}",end='')
        if m.play_mode == "BeforeKickOff":
            if m.time - 0 < 0.1:
                m.send(b"(playMode KickOff_Left)")
            else:
                m.send(b"(playMode KickOff_Right)")
