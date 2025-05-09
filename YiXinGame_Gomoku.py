import subprocess as sub
import os
file_dir = os.path.dirname(__file__)

from YiXinGame import Game

import requests as re
import time as t

user = 'zhanghao'  # 自己的账号
password = 'mima'  # 自己的密码
encodeLogin_modulus = 12344 # 公钥
join_url = 'http://xx.xx.xx.xx:800x/join_game'
check_url = 'http://xx.xx.xx.xx:800x/check_game/'
play_url = 'http://xx.xx.xx.xx:800x/play_game/'

def fastModular(x):
    """x[0] = base """
    """x[1] = power"""
    """x[2] = modulus"""
    result = 1
    while (x[1] > 0):
        if (x[1] & 1):
            result = result * x[0] % x[2]
        x[1] = int(x[1] / 2)
        x[0] = x[0] * x[0] % x[2]
    return result


def str_to_num(strings):
    sum = 0
    lens = len(strings)
    for i in range(0, lens):
        sum += ord(strings[i]) * 256 ** (lens - i - 1)
    return sum


def encodeLogin(password):
    # 公钥
    power = 65537
    modulus = encodeLogin_modulus

    return hex(fastModular([str_to_num(password), power, modulus]))


def join_game(user, myHexPass):
    """加入游戏并返回一个 get回复包对象"""

    url = join_url
    param = {
        'user': user,
        'password': myHexPass,
        'data_type': 'json'
    }

    getHtml = re.get(url, params=param)

    print(f"Open a new game{getHtml.text}")
    return getHtml


def check_game(game_id):
    url = check_url + str(game_id)
    getState = re.get(url)
    # print(getState.text)    # 测试显示数据用
    return getState


def play_game(user, myHexPass, game_id, coord):
    url = play_url + str(game_id)
    param = {
        'user': user,
        'password': myHexPass,
        'data_type': 'json',
        'coord': coord
    }
    re.get(url, params=param)


def getIndexNum(coords):
    """coords y x"""
    # 0行 [0]='.'--- [14]='.'[15]='\n'
    # 1行 [16]='.'--- [30]='.'[31]='\n'
    # 2行 [32]='.'--- [46]='.'[47]='\n'
    # 15行 [240]='.'--- [254]='.'[255]='\n'
    return (ord(coords[0]) - ord('a')) * 16 + ord(coords[1]) - ord('a')


def allIndexStr():
    spot = []
    for i in range(0, 15):
        for j in range(0, 16):
            spot.append(chr(i + 97) + chr(j + 97))
    return spot


def getLine(coord, board):
    """
    获得中心点的四周 15 点情况 返回一个字符串列表
    coord[0] y 纵坐标 coord[1] x 控制横坐标
    board  棋局
    """
    line = ['', '', '', '']
    i = 0
    """ 核心思想就是 将周围点两个坐标x，y的限制 转化为一个位置index的限制 """
    while (i != 15):
        if ord(coord[1]) - ord('a') - 7 + i in range(0, 15):  # line[0]是横线 只需保证 横坐标在棋盘里就好
            line[0] += board[(ord(coord[0]) - ord('a')) * 16 + ord(coord[1]) - ord('a') - 7 + i]
        else:
            line[0] += ' '
        if ord(coord[0]) - ord('a') - 7 + i in range(0, 15):  # line[2]是竖线 只需保证 纵坐标在棋盘里就好
            line[2] += board[(ord(coord[0]) - ord('a') - 7 + i) * 16 + ord(coord[1]) - ord('a')]
        else:
            line[2] += ' '
        # - 7 + i 是从最小值上升判断  + 7 - i 是从最大值下降判断 两者没有什么不同 根据index的求法而定
        if ord(coord[1]) - ord('a') - 7 + i in range(0, 15) and ord(coord[0]) - ord('a') - 7 + i in range(0,
                                                                                                          15):  # line[1]是\线 保证 横纵坐标都在棋盘里就好
            line[1] += board[(ord(coord[0]) - ord('a') - 7 + i) * 16 + ord(coord[1]) - ord('a') - 7 + i]
        else:
            line[1] += ' '
        if ord(coord[1]) - ord('a') + 7 - i in range(0, 15) and ord(coord[0]) - ord('a') - 7 + i in range(0,
                                                                                                          15):  # line[3]是/线 保证 横纵坐标都在棋盘里就好
            line[3] += board[(ord(coord[0]) - ord('a') - 7 + i) * 16 + ord(coord[1]) - ord('a') + 7 - i]
        else:
            line[3] += ' '

        i += 1
    return line


def judge(testOrder):
    if (len(testOrder) // 2) % 2 == 0:  # 我是黑方
        return 'MO'
    else:  # 我是白方
        return 'OM'


def RuleWithPoints():
    RWP = {
        ("CMMMM", "MCMMM", "MMCMM", "MMMCM", "MMMMC"): 10000,
        ("COOOO", "OCOOO", "OOCOO", "OOOCO", "OOOOC"): 6000,
        (".CMMM.", ".MCMM.", ".MMCM.", ".MMMC."): 5000,
        ("COOO.", ".OOOC", ".OOCO.", ".OCOO."): 2500,
        ("OCMMM.", "OMCMM.", "OMMCM.", "OMMMC.", ".CMMMO", ".MCMMO", ".MMCMO", ".MMMCO"): 2000,
        (".MMC.", ".MCM.", ".CMM."): 400,
        (".OOC", "COO.", "MOOOC", "COOOM"): 400,
        (".MMCO", ".MCMO", ".CMMO", "OMMC.", "OMCM.", "OCMM.", "MOOC", "COOM"): 200,
        (".MC.", ".CM."): 50,
        ('.'): 1
    }
    return RWP

# The most important function
def getMaxCoords(Order, RWP, indexSrc, mod):
    """对于每一个当下的棋局 返回一个最成功的下点"""
    '''output: maxCoord
    output format: str, contains two characters, e.g. 'aa'
    '''
    
    # for debug
    mod.print_board()

    maxCoord = mod.play(Order)

    return maxCoord


win_num = 0
def start_game(mod):
    myHexPass = encodeLogin(password)
    RWP = RuleWithPoints()
    indexSrc = allIndexStr()
    game_id = join_game(user, myHexPass).json()["game_id"] # 仅仅是拿到一个game_id
    state = check_game(game_id).json() # 拿到一个状态字典，包含ready creator opponent_name current_turn board winner
    
    print("Looking forgame partners ...")
    while state['ready'] == "False":
        state = check_game(game_id).json()
        print(state['ready'], end=" ")
        t.sleep(5)
    
    if state['creator'] != user:
        opponent = state['creator']
    else:
        opponent = state['opponent_name']

    while state['ready'] == "True":
        if state['current_turn'] == user:
            order = state['board']
            coord = getMaxCoords(order, RWP, indexSrc, mod)
            play = play_game(user, myHexPass, game_id, coord)
            print(f"Playing {coord}")
        else:
            print(f"Waiting for {opponent} to play")

        t.sleep(5)
        state = check_game(game_id).json()

        if state['winner'] != "None":
            print(f"The winner is {state['winner']}")
            break

def start_game_test(mod):
    orders = ''
    orders += mod.play('')
    # print_board and wait human input the order
    while True:
        mod.print_board()
        pos = input('Please input your order (e.g. 7,7): ') # row, column
        if pos == 'q':
            break
        orders += mod.pos_to_order(pos) # add human order
        orders += mod.play(orders)      # add machine order

if __name__ == '__main__':
    def play(mod):
        global win_num
        confirm = True
        if confirm:
            start_game(mod)
            # start_game_test(mod)
        else:
            return
    mod = Game()
    play(mod)