import json
import re
import socket
import subprocess
import os
import time
import threading
import csv
import time

class Runner:
    def __init__(self):
        self.reset()

    def reset(self):
        self.BUFFER_SIZE = 1024*1024
        self.rcv_buff = bytearray(self.BUFFER_SIZE)
        self.send_buff = []
        self.monitor_socket = None
        self.play_mode_list = []
        self.play_mode=None
        self.time=0
        self.score_left=0
        self.score_right=0
        self.rcssserver3d_proc=None

    def init_monitor_socket(self):
        config = self.get_config()
        server_ip = config['monitor']['ip']
        server_port = config['monitor']['port']
        self.monitor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.monitor_socket.connect((server_ip, server_port))
        except Exception as e:
            print("发生错误：", e)

    def kill_rcssserver3d(self):
        os.system("pkill rcssserver3d -9")
        time.sleep(1)

    def run_rcssserver3d(self):
        self.rcssserver3d_proc = subprocess.Popen(['rcssserver3d'], 
                                    stdout=subprocess.DEVNULL, 
                                    stderr=subprocess.DEVNULL)
        time.sleep(1)

    def run_team(self,binary_path):
        original_dir = os.getcwd()
        script_dir = os.path.dirname(os.path.abspath(binary_path))
        os.chdir(script_dir)
        os.system('bash start.sh localhost > nul 2>&1')
        os.chdir(original_dir)
        time.sleep(2)

    def receive(self):
        try:
            if self.monitor_socket.recv_into(self.rcv_buff, nbytes=4) != 4:
                raise ConnectionResetError()
            msg_size = int.from_bytes(self.rcv_buff[:4], byteorder='big', signed=False)
            if self.monitor_socket.recv_into(self.rcv_buff, nbytes=msg_size, flags=socket.MSG_WAITALL) != msg_size:
                raise ConnectionResetError()
            return self.rcv_buff[:msg_size]
        except ConnectionResetError:
            print("\nsocket closed")
            return None

    def get_config(self):
        with open("config.json", "r") as f:
            config = json.load(f)
            return config

    def send(self, msg, delay=0):
        def send_msg(msg):
            try:
                self.monitor_socket.send((len(msg)).to_bytes(4, byteorder='big') + msg)
            except Exception as e:
                print("发生错误：", e)
        timer = threading.Timer(delay, send_msg,args=(msg,))
        timer.start()
        
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

    def run_game(self,team1_path,team2_path,exchange=False):
        self.kill_rcssserver3d()
        self.reset()
        if exchange:
            # 上半场
            score_team1=0
            score_team2=0
            self.run_rcssserver3d()
            self.run_team(team1_path)
            self.run_team(team2_path)
            self.init_monitor_socket()
            self.send(b"(reqfullstate)")
            while True:
                text = self.receive()
                if text is None:
                    return None
                self.parse(text.decode('ascii'))
                print(f"\rplayMode:{self.play_mode},time:{self.time},score_left:{self.score_left},score_right:{self.score_right}",end='')
                if self.play_mode == "BeforeKickOff":
                    if self.time==0:
                        self.send(b"(playMode KickOff_Left)",1)
                    else:
                        break
            self.kill_rcssserver3d() 
            score_team1+=self.score_left
            score_team2+=self.score_right
            # 下半场
            self.run_rcssserver3d()
            self.run_team(team2_path)
            self.run_team(team1_path)
            self.init_monitor_socket()
            self.send(b"(reqfullstate)")
            while True:
                text = self.receive()
                if text is None:
                    return None
                self.parse(text.decode('ascii'))
                print(f"\rplayMode:{self.play_mode},time:{self.time},score_left:{self.score_left},score_right:{self.score_right}",end='', flush=True)
                if self.play_mode == "BeforeKickOff":
                    if self.time==0:
                        self.send(b"(playMode KickOff_Left)",1)
                    else:
                        break
            self.kill_rcssserver3d() 
            score_team2+=self.score_left
            score_team1+=self.score_right
        else:
            score_team1=0
            score_team2=0
            self.run_rcssserver3d()
            self.run_team(team1_path)
            self.run_team(team2_path)
            self.init_monitor_socket()
            self.send(b"(reqfullstate)")
            while True:
                text = self.receive()
                if text is None:
                    return None
                self.parse(text.decode('ascii'))
                print(f"\rplayMode:{self.play_mode},time:{self.time},score_left:{self.score_left},score_right:{self.score_right}",end='')
                if self.play_mode == "BeforeKickOff":
                    if self.time==0:
                        self.send(b"(playMode KickOff_Left)",1)
                    else:
                        self.send(b"(playMode KickOff_Right)",1)
                elif self.play_mode == "GameOver":
                    break
            self.kill_rcssserver3d()
            score_team1+=self.score_left
            score_team2+=self.score_right
        return [score_team1,score_team2]


if __name__ == '__main__':
    our_binary_dir="binary/our"
    opp_binary_dir="binary/opp"
    our_binary_list=[os.path.join(our_binary_dir, name) for name in os.listdir(our_binary_dir) if os.path.isdir(os.path.join(our_binary_dir, name))]
    opp_binary_list=[os.path.join(opp_binary_dir, name) for name in os.listdir(opp_binary_dir) if os.path.isdir(os.path.join(opp_binary_dir, name))]
    print(our_binary_list)
    print(opp_binary_list)
    r=Runner()
    max_retry_times=2   # 比赛出现问题时的最大重试次数
    every_play_times=1  # 每个对抗打几次
    exchange=True       # 是否换边
    our_left=True       # 我方在左还是右(只在不换边对打才有意义)

    detail_record_title=["our_bin","opp_bin"]
    epochs=[]
    for i in range(every_play_times):
        epochs.append(f"epoch_{i+1}")
    detail_record_title.extend(epochs)
    detail_record_title.extend(["胜","平","负","异常","胜率"])
    single_bin_record_title=["our_bin","胜","平","负","异常","胜率"]
    all_useful_count=0
    all_win_count=0
    all_tie_count=0
    all_loss_count=0
    all_error_count=0

    time_str=time.strftime('%Y%m%d%H%M%S', time.localtime())
    with open(f"{time_str}-detail.csv","w",newline="", encoding="utf-8") as f:
        w=csv.writer(f)
        w.writerow(detail_record_title)
    with open(f"{time_str}-single.csv","w",newline="", encoding="utf-8") as f:
        w=csv.writer(f)
        w.writerow(single_bin_record_title)

    for our_bin in our_binary_list:
        single_bin_useful_count=0
        single_bin_win_count=0
        single_bin_tie_count=0
        single_bin_loss_count=0
        single_bin_error_count=0
        for opp_bin in opp_binary_list:
            row=[our_bin,opp_bin]
            useful_count=0
            win_count=0
            tie_count=0
            loss_count=0
            error_count=0
            for _ in range(every_play_times):
                retry_times=0
                result=None
                if our_left:
                    team_left=our_bin
                    team_right=opp_bin
                else:
                    team_left=opp_bin
                    team_right=our_bin
                result=r.run_game(os.path.join(team_left,"start.sh"),os.path.join(team_right,"start.sh"),exchange)
                while result is None and retry_times<max_retry_times:
                    retry_times+=1
                    result=r.run_game(os.path.join(team_left,"start.sh"),os.path.join(team_right,"start.sh"),exchange)
                if result is None:
                    row.append("Error")
                    error_count+=1
                else:
                    score_left=result[0]
                    score_right=result[1]
                    row.append(f"{score_left}:{score_right}")
                    useful_count+=1
                    if our_left:
                        score_our=score_left
                        score_opp=score_right
                    else:
                        score_our=score_right
                        score_opp=score_left
                    if score_our>score_opp:
                        win_count+=1
                    elif score_our==score_opp:
                        tie_count+=1
                    else:
                        loss_count+=1
            row.extend([win_count,tie_count,loss_count,error_count,f"{round(100*win_count/useful_count,2)}%"])
            with open(f"{time_str}-detail.csv","a",newline="", encoding="utf-8") as f:
                w=csv.writer(f)
                w.writerow(row)
            single_bin_useful_count+=useful_count
            single_bin_win_count+=win_count
            single_bin_tie_count+=tie_count
            single_bin_loss_count+=loss_count
            single_bin_error_count+=error_count
        with open(f"{time_str}-single.csv","a",newline="", encoding="utf-8") as f:
            w=csv.writer(f)
            w.writerow([our_bin,single_bin_win_count,single_bin_tie_count,single_bin_loss_count,single_bin_error_count,f"{round(100*single_bin_win_count/single_bin_useful_count,2)}%"])
        all_useful_count+=single_bin_useful_count
        all_win_count+=single_bin_win_count
        all_tie_count+=single_bin_tie_count
        all_loss_count+=single_bin_loss_count
        all_error_count+=single_bin_error_count
    print(f"总胜：{all_win_count}\n"+
        f"总平：{all_tie_count}\n"+
        f"总负：{all_loss_count}\n"+
        f"总异常：{all_error_count}\n"+
        f"总胜率：{round(100*all_win_count/all_useful_count,2)}%\n")

    with open(f"{time_str}-all.txt","w") as f:
        f.write(f"总胜：{all_win_count}\n"+
        f"总平：{all_tie_count}\n"+
        f"总负：{all_loss_count}\n"+
        f"总异常：{all_error_count}\n"+
        f"总胜率：{round(100*all_win_count/all_useful_count,2)}%\n")
