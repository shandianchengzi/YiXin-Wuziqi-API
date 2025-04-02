import subprocess as sub
import os
file_dir = os.path.dirname(__file__)

def check_five_in_a_row(board, player, x, y):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dx, dy in directions:
        count = 1
        # Check in the positive direction
        nx, ny = x + dx, y + dy
        while 0 <= nx < 15 and 0 <= ny < 15 and board[nx][ny] == player:
            count += 1
            nx += dx
            ny += dy
        # Check in the negative direction
        nx, ny = x - dx, y - dy
        while 0 <= nx < 15 and 0 <= ny < 15 and board[nx][ny] == player:
            count += 1
            nx -= dx
            ny -= dy
        if count >= 5:
            return True
    return False

# reference: https://plastovicka.github.io/protocl2en.htm from the Gomocup Website https://gomocup.org/detail-information/
class YiXin:
    # from https://www.aiexp.info/pages/yixin-cn.html
    mYixin = sub.Popen(os.path.join(file_dir, "Yixin2018.exe"),
                       stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE)
    # 设定参数

    def __init__(self):
        self.input('START 15')
        self.input('INFO timeout_match 200000')
        self.input('INFO timeout_turn 3500')  # 控制思考快慢

        self.output()
        print("YiXin ready!!")

    # 向Yixin 输入对手落子指令
    def input(self, str):
        print('Human: '+str)
        self.mYixin.stdin.write((str+'\n').encode())
        self.mYixin.stdin.flush()

    # 获取Yixin 的输出
    def output(self):
        # 一直获取Yixin 输出，直到落子的指令或其它
        while True:
            str = bytes.decode(self.mYixin.stdout.readline())
            print('YiXin: ' + str, end='')
            if ((',' in str) or ('OK' in str)) or ('ERROR' in str):
                break
        self.mYixin.stdout.flush()
        if ('ERROR' in str):
            print('Please check the input!')
            exit(0)
        if (',' in str):
            return str

    def update_board(self, pos, first=0):
        '''
        pos: [[x, y], [x, y], ...]
        first: 0 or 1
        '''
        self.input('BOARD')
        for i in range(len(pos)):
            self.input(f"{pos[i][0]},{pos[i][1]},{first+1}")
            first = 1 - first
        self.input('DONE')

        return self.output() # wait the next pos

    # 新的一局
    def restart(self):
        self.input('RESTART 15')
        self.output() # wait OK

class Game:
    order = ''
    def __init__(self):
        self.yixin = YiXin()
        self.order = ''
        self.winner = 0

    # trans the order to the position
    def order_to_pos(self, order:str):
        # e.g. 'a1b2' -> [[0, 0], [1, 1]]
        pos = []
        for i in range(0, len(order), 2):
            pos.append([ord(order[i])-97, ord(order[i+1])-97])
        return pos
    
    # trans one pos to one order
    def pos_to_order(self, pos):
        # e.g. [7,7] -> 'h8'
        if type(pos) == list:
            return chr(pos[0]+97) + chr(pos[1]+97)
        # e.g. '7,7' -> 'h8'
        if type(pos) == str:
            pos = pos.strip().split(',')
            return chr(int(pos[0])+97) + chr(int(pos[1])+97)

    # input order, and output the corresponding order
    def play(self, order:str):
        '''
        order: the order of the game, e.g. 'a1b1a2b2'
        return: the next order, e.g. 'a3'
        '''
        # 如果self.order不是order的前缀，那么就重新开始一局
        if not order.startswith(self.order):
            self.yixin.restart()
            self.order = '' # clear the old order
        # just update the new order
        new_order = order[len(self.order):]
        next_pos = self.yixin.update_board(self.order_to_pos(new_order))
        next_order = self.pos_to_order(next_pos)
        # update the order
        self.order = order + next_order
        # recheck the game winner
        self.winner = self.check_game(self.order)
        return next_order

    def print_board(self):
        board = ''  # 棋板
        for i in range(0, 15):
            board += '...............' + '\n'
        BW = judge(self.order)
        for i in range(0, len(self.order), 2):  # i = 0 2 4 6 8
            index = getIndexNum(self.order[i:i + 2])
            board = board[0: index] + BW[~int(i/2)%2] + board[index + 1:]
        print(board)  # 测试显示数据用
    
    # check the game winner
    def check_game(self, order):
        # e.g. 'a1b1a2b2a3b3a4b4a5' -> 1
        moves = self.order_to_pos(order)
        # check the winner
        board = [[0] * 15 for _ in range(15)]
        for i, (x, y) in enumerate(moves):
            player = 1 if i % 2 == 0 else 2
            board[x][y] = player
            if check_five_in_a_row(board, player, x, y):
                return player
        return 0

def getIndexNum(coords):
    """coords y x"""
    # 0行 [0]='.'--- [14]='.'[15]='\n'
    # 1行 [16]='.'--- [30]='.'[31]='\n'
    # 2行 [32]='.'--- [46]='.'[47]='\n'
    # 15行 [240]='.'--- [254]='.'[255]='\n'
    return (ord(coords[0]) - ord('a')) * 16 + ord(coords[1]) - ord('a')

def judge(testOrder):
    if (len(testOrder) // 2) % 2 == 0:  # 我是黑方
        return 'MO'
    else:  # 我是白方
        return 'OM'

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
        if mod.winner:
            mod.print_board()
            result = 'MO'
            print(f"Game Over! The winner is {result[mod.winner-1]}.")
            break

if __name__ == '__main__':
    def play(mod):
        start_game_test(mod)
    mod = Game()
    play(mod)