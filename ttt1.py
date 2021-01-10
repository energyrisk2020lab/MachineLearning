# Tic-tac-toe のソースコード，Q-Learning の学習用
# https://qiita.com/narisan25/items/e64a5741864d5a3b0db0

import random
import math

# 盤面
# 0-9の配列にXなら1、ブランクなら0、○なら-1を入れます。


#### 定数の宣言
# Python には，型としての定数はない ＝ 書き換えを禁止することはできない
# 慣例として，大文字とアンダースコアのみで構成される変数を定数とみなす
# https://qiita.com/D-hatamoto/items/140cb5956cad796c5024

# ゲーム盤を要素数 9 のリストで定義する（1行目左から1,2,3; 2行目左から4,5,6; 3行目左から7,8,9）
# 空白セルを0，Xを1，○を-1で表現する
# ゲームの結果は，Xの勝ち，○の勝ち，引き分けのいずれかである
# ゲームの結果を数字で現す，Xの勝ち:1，○の勝ち:-1，引き分け:2
EMPTY = 0
PLAYER_X = 1
PLAYER_O = -1
MARKS = {PLAYER_X:"X",PLAYER_O:"O", EMPTY:" "}
DRAW = 2



#### クラス TTTBoard の宣言
# ゲーム盤の状態と，ゲーム盤が有する機能を表現するクラス

class TTTBoard:

    def __init__(self, board=None):     # 現在の盤面を表現するリスト作成
        if board == None:
            self.board = []
            for i in range(9):self.board.append(EMPTY)
        else:
            self.board = board
        self.winner = None
    # 初期化のための関数（＝コンストラクタ）
    # オブジェクト生成（インスタンス生成）時に必ず呼び出され，初期化を行う
    # ゲーム盤は board というリスト（要素数9）で表現される
    # boardが存在しなければ，要素がすべてゼロの board を生成する（ゼロはブランクを意味する）
    # boardが存在すれば，それをそのまま使う

    def get_possible_pos(self):         # 現在の盤面において着手可能なセルのリスト作成
        pos = []
        for i in range(9):
            if self.board[i] == EMPTY:
                pos.append(i)
        return pos
    # pos というリストに，ブランクセルの番号を格納する
    # すなわち，着手可能なセルのリストを作成する
    # 作成したリストを出力する

    def print_board(self):              # 現在の盤面の画面への出力
        tempboard = []
        for i in self.board:            # 現在の盤面を表現するリスト board（int）に従い，tempboard(str)に対応する記号を追加
            tempboard.append(MARKS[i])
        row = ' {} | {} | {} '
        hr = '\n-----------\n'
        print((row + hr + row + hr + row).format(*tempboard))
    # self.board は，要素数9のリストであり，各要素は, 1, -1, 0 のいずれかの値をとる
    # self.tempboard は，要素数9のリストであり，各要素は, X, 0, " " のいずれかの値をとる
    # 両者のマッピングは辞書MARKSの通り行われる
    # format 関数を使って，リスト tempboard の要素を，9つの{}に分解して入れる
    # https: // qiita.com / Morio / items / b79ead5f881e6551d9e1
    # リストに * を付けて関数の引数に指定すると、それぞれの要素が展開され個別の引数として渡される。
    # https://note.nkmk.me/python-print-basic/

    def check_winner(self):             # 現在の盤面における勝敗の判定
        win_cond = ((1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9),(1,5,9),(3,5,7))
        for each in win_cond:   # win_cond の各要素について，
            if self.board[each[0]-1] == self.board[each[1]-1] == self.board[each[2]-1]:
                if self.board[each[0]-1]!=EMPTY:
                    self.winner = self.board[each[0]-1]
                    return self.winner
        return None
    # 勝利条件はゲームを通じて変わらないため，タプルとして定義
    # each = (1,2,3)のとき，配列 board の 0,1,2 番目の要素が等しいかどうかをチェック
    # board に並んでいるのが EMPTY でなければ（1か-1なら），その数字を勝者とみなす
    # プレイヤーX勝利，プレイヤー0勝利，いずれでもないのいずれかを出力（1, -1, None）
    # 引き分けの判定は，この関数ではなくcheck_drawで行う

    def check_draw(self):               # 現在の盤面が引き分けかどうかの判定
        if len(self.get_possible_pos())==0 and self.winner is None:
            self.winner = DRAW
            return DRAW
        return None
    # 着手可能なセルのリストが空で，かつ勝者が決まっていない場合，引き分けです
    # 引き分けまたは引き分けでないのいずれかを出力（DRAW, None）

    def move(self, pos, player):        # 盤面の更新（＝着手の記録）と勝敗の判定
        if self.board[pos] == EMPTY:
            self.board[pos] = player
        else:
            self.winner = -1*player
        self.check_winner()
        self.check_draw()
    # 着手不可能なセル（空白ではないセル）に打ったら反則負け（相手の勝ち）

    def clone(self):                    # 現在の盤面のコピーを作成
        return TTTBoard(self.board.copy())
    # .copy()は，対象のリストを値渡しコピーするメソッド
    # 値渡しコピー：元のリスト（この場合board）の要素が変化しても，コピーされたリストの要素は変化しない
    # https://qiita.com/BotamochiRice/items/c7fdaf87b7e72492c504

    # def switch_player(self):            # 現在の手番を更新
    #     if self.player_turn == self.player_x:
    #         self.player_turn = self.player_o
    #     else:
    #         self.player_turn = self.player_x
    # 現在の手番を現す変数 player_turn は，TTT_GameOrganizer クラス内で定義
    # この関数は削除しても動く→おそらく元のソースの消し忘れか


#### クラス TTT_GameOrganizer の宣言
# 任意の2プレイヤーによる ゲームセッションを表現するクラス
# 盤面とプレイヤーは，それぞれ別のクラスで定義される
# ゲーム・ゲームプレイ：3目並べを1回プレイすること
# ゲームセッション：3目並べを nplay 回プレイすること

class TTT_GameOrganizer:

# act_turn = 0
# winner = None
# これらの変数はコメントアウトしても動く→元のソースの消し忘れか

    def __init__(self,px,po,nplay=1,showBoard=True,showResult=True,stat=100):   # ゲームセッションの初期設定
        self.player_x = px                                      # プレイヤーXを代入（インスタンス）
        self.player_o = po                                      # プレイヤーOを代入（インスタンス）
        self.nwon = {px.myturn:0,po.myturn:0,DRAW:0}            # 戦績を記録する辞書
        self.nplay = nplay                                      # ゲームセッションの規定ゲーム数
        self.players = (self.player_x,self.player_o)            # プレイヤーのタプル（インスタンスのタプル）
        self.board = None                                       # 初期状態にて，盤面は存在しない
        self.disp = showBoard                                   # 盤面表示の有無（True: 表示する）
        self.showResult = showResult                            # ゲーム結果表の有無（True: 表示する）
        self.player_turn = self.players[random.randrange(2)]    # 手番プレイヤーをランダムに初期化（インスタンス）
        self.nplayed = 0                                        # 終了ゲーム数
        self.stat = stat                                        # stat回以上ゲームがプレイされないためのブレーキ？
    # pycharm で，デバッグ中に変数にマウスオーバーすると，代入されている値が見える

    def progress(self):
        while self.nplayed <self.nplay: # ゲームが nplay 回プレイされるまで繰り返す while文
            self.board = TTTBoard()                             # 現在の盤面を取得（インスタンス）
            while self.board.winner == None:                    # 現在の盤面の winner が None であればループ突入
                if self.disp:print("Turn is " + self.player_turn.name)  # 手番プレイヤー名を表示
                act = self.player_turn.act(self.board)          # 手番プレイヤーのactメソッドに現在の盤面を引数として与える
                self.board.move(act,self.player_turn.myturn)
                    # progress インスタンス内の board インスタンス内の move メソッドに，手番プレイヤーのactメソッドの出力を与える
                    # move メソッドが，盤面の更新とself.board.winnerの更新を行う
                if self.disp:self.board.print_board()           # moveメソッドによって更新された盤面を表示する

                if self.board.winner != None:                   # 現在の盤面の winner が None でなければ
                    # notice every player that game ends
                    for i in self.players:                      # すべてのプレイヤーが getGameResultメソッドを実行
                        i.getGameResult(self.board)
                    if self.board.winner == DRAW:               # 引き分けの場合の処理
                        if self.showResult:print("Draw Game")
                    elif self.board.winner == self.player_turn.myturn:  # 手番プレイヤーが勝者の場合
                        out = "Winner : " + self.player_turn.name
                        if self.showResult: print(out)
                    else:                                       # 手番プレイヤー以外が勝者の場合（反則負け）
                        print("Invarid Move!")
                    self.nwon[self.board.winner] += 1
                else:                                           # 現在の盤面の winner が None であれば
                    self.switch_player()                        # switch_player メソッドにより手番を交替
                    #Notice other player that the game is going
                    self.player_turn.getGameResult(self.board)  # 手番プレイヤーが getGameResultメソッドを実行
                                                                # q値の更新はここで行われる

            self.nplayed += 1                                   # 終了ゲーム数を1増やす
            if self.nplayed % self.stat == 0 or self.nplayed == self.nplay:
                # 終了ゲーム数が100に達する，またはゲームセッションの規定ゲーム数に達した場合
                print(self.player_x.name + ":" + str(self.nwon[self.player_x.myturn]) + ","\
                    + self.player_o.name + ":" + str(self.nwon[self.player_o.myturn])\
                    + ",DRAW:"+str(self.nwon[DRAW]))
                # ゲームセッションの戦績を表示

    def switch_player(self):                                    # 手番を交替する関数
        if self.player_turn == self.player_x:
            self.player_turn = self.player_o
        else:
            self.player_turn = self.player_x


######## 以下，プレイヤーを表現するクラスの宣言
# すべてのクラスは，act メソッドと getGameResult メソッドを持たなければならない
# act メソッド: 着手を決める関数
# getGameResult メソッド: 現在の盤面（インスタンス）に応じた処理
# getGameResult で何もしない場合も，pass を有するメソッドを定義する必要あり

#### クラス PlayerRandom の宣言
# まったくの乱数で着手を決めるエージェント
# getGameResult は pass

class PlayerRandom:
    def __init__(self,turn):
        self.name = "Random"
        self.myturn = turn

    def act(self,board):
        acts = board.get_possible_pos()
        i = random.randrange(len(acts))
        return acts[i]

    def getGameResult(self,board):
        pass



#### クラス PlayerHuman の宣言
# 人間プレイヤー
# getGameResult は pass

class PlayerHuman:
    def __init__(self,turn):
        self.name = "Human"
        self.myturn = turn

    def act(self,board):
        valid = False
        while not valid:
            try:                        # try節：例外が発生する可能性のある処理
                act = input("Where would you like to place " + str(self.myturn) + "(1-9)? ")
                act = int(act)
                # if act >= 1 and act <= 9 and board.board [act-1] == EMPTY:
                if act >= 1 and act <= 9:
                    valid = True
                    return act-1
                else:                   # 入力が数字だった場合の処理
                    print("That is not a valid move! Please try again.")
            except Exception as e:      # 入力が数字以外だった場合の処理
                print (act + "is not a valid move! Please try again.")
        return act

    def getGameResult(self,board):      # winner が None でなく自分でもなく DRAW でもない場合，反則負け
        if board.winner is not None and board.winner != self.myturn and board.winner != DRAW:
            print("I lost")



#### クラス PlayerAlphaRandom の宣言
# 現在の盤面で勝てる着手がある場合はそれを選択
# ない場合はランダムに着手
# getGameResult は pass

class PlayerAlphaRandom:
    def __init__(self,turn):
        self.name = "AlphaRandom"
        self.myturn = turn

    def act(self,board):
        acts = board.get_possible_pos()
        # see only next winnable act
        for act in acts:
            tempboard = board.clone()
            tempboard.move(act,self.myturn)
            # check if win
            if tempboard.winner == self.myturn:
                # print ("Check mate")
                return act
        # 勝てる手がない場合はただのランダム君
        i = random.randrange(len(acts))
        return acts[i]

    def getGameResult(self,board):
        pass


#### クラス PlayerMC の宣言
# 現時点で選択可能なすべての着手について，trial メソッドを使って評価点を作成する
# 評価点とは，ある着手を選択した後でAlphaRandom同士の模擬戦を行った場合の勝率である
# 評価点が一番高い着手を選択する
# 模擬戦の回数（n）を増やすほど，正確な評価を行うことができる

class PlayerMC:
    def __init__(self,turn,name="MC"):
        self.name = name
        self.myturn =turn

    def getGameResult(self,winter):
        pass

    def win_or_rand(self,board,turn):
        acts = board.get_possible_pos()
        # see only next winnable act
        for act in acts:
            tempboard=board.clone()
            tempboard.move(act,turn)
            # check if win
            if tempboard.winner==turn:
                return act
        i = random.randrange(len(acts))
        return acts[i]

    def trial(self,score,board,act):
        tempboard = board.clone()
        tempboard.move(act,self.myturn)
        tempturn = self.myturn
        while tempboard.winner is None:
            tempturn = tempturn*-1
            tempboard.move(self.win_or_rand(tempboard,tempturn),tempturn)

        if tempboard.winner==self.myturn:
            score[act]+=1
        elif tempboard.winner==DRAW:
            pass
        else:
            score[act]-=1

    def getGameResult(self,board):
        pass

    def act(self,board):
        acts = board.get_possible_pos()         # 選択可能な着手のリスト
        scores={}                               # 選択可能な各着手に対する評価点を示す辞書
        n=100                                   # 着手毎にモンテカルロ試行を何回繰り返すかを指定
        for act in acts:
            scores[act]=0
            for i in range(n):
                #print("Try"+str(i))
                self.trial(scores,board,act)

            #print(scores)
            scores[act]/=n
        # このfor文によって，評価点の辞書が完成する（初手であれば 4: すなわち中心が一番高くなるはず）


        max_score = max(scores.values())        # 評価点の最大値
        for act, v in scores.items():           # key とvalue の組に対してfor文を回す
            if v == max_score:                  # value(＝評価点)が max_score と等しくなるitemにつき，key(=act)を返す
                #print(str(act)+"="+str(v))
                return act


#### クラス PlayerQL の宣言
# ε-グリーディ方策に基づくQ学習を行う
# ε-グリーディ方策はpolicyメソッドで表現される
# Q学習（Q値の更新）はlearnメソッドで表現される
# Organizer からの呼び出しは以下の通り
# (1) Organizer の progress メソッド が act メソッドを呼び出す
#   → actメソッドがpolicy メソッドを呼び出す
#   → policyメソッドがε-グリーディ方策に基づいて着手を返す
# (2)Organizer の progress メソッド が getGameResult メソッドを呼び出す
#   → getGameResult メソッドがlearnメソッドを呼び出す

class PlayerQL:
    def __init__(self,turn,name="QL",e=0.2,alpha=0.3):
        self.name = name
        self.myturn = turn
        self.q = {}                             # set of s, a; キーが(state,act)となっている
        self.e = e                              # eの確率でランダム方策，1-eの確率でグリーディ方策
        self.alpha = alpha                      # 学習率
        #self.gamma = 1.0                        # 割引率
        self.gamma = 0.9  # 割引率
        self.last_move = None
        self.last_board = None
        self.totalgamecount = 0

    def policy(self,board):
        self.last_board = board.clone()         # 現在の盤面をコピー
        acts = board.get_possible_pos()         # 選択可能な着手のリスト

        # Explore sometimes
        if random.random() < (self.e/(self.totalgamecount//10000+1)):   # ランダム方策をとる条件
            # // は切り下げ除算なので，totalgamecount が10000未満であれば，self.eを1で割ることになる
            # totalgamecount が10000を超えると，ランダム方策をとる確率が徐々に下がるよう工夫されている
            i = random.randrange(len(acts))
            return acts[i]

        qs = [self.getQ(tuple(self.last_board.board),act) for act in acts]
            # qは，盤面と着手の組をkey, Q値をvalue とする辞書
            # qsは，qのvalue であるQ値だけを並べたリスト
        maxQ = max(qs)

        if qs.count(maxQ) > 1:  # list qs の要素のうち，maxQ と等しいものが1つより多い場合
            # more than 1 best option; choose among them randomly
            best_options = [i for i in range(len(acts)) if qs[i] == maxQ]
            i = random.choice(best_options)
        else:
            i = qs.index(maxQ)

        self.last_move = acts[i]
        return acts[i]

    def getQ(self,state,act):               # 現在の盤面と着手の組に対し，もしq値が存在しなければ，初期値1を与える
        # encourage exploration; "optimistc" 1.0 initial values
        # 未知の盤面のQ値を自動的に1に設定する：するとエージェントは未知の盤面を積極的に探索する
        if self.q.get((state,act)) is None:
            self.q[(state,act)] = 1
        return self.q.get((state,act))      # 辞書qのvalueをリターン


    def getGameResult(self,board):
        r = 0
        if self.last_move is not None:          # すなわち初手ではないとき
            if board.winner is None:            # 前の手番における盤面と着手の組が勝利にも敗北にもならなかったとき
                self.learn(self.last_board,self.last_move,0,board)
                pass
            else:
                if board.winner == self.myturn:
                    self.learn(self.last_board,self.last_move,1,board)
                elif board.winner != DRAW:
                    self.learn(self.last_board,self.last_move,-1,board)
                else:
                    self.learn(self.last_board,self.last_move,0,board)
            self.totalgamecount += 1
            self.last_move = None
            self.last_board = None

    def learn(self,s,a,r,fs):   # s:前手番の盤面，a:前手番の着手，r:報酬，fs:現在の盤面
        pQ = self.getQ(tuple(s.board),a)    # 前手番の盤面・着手のQ値
        if fs.winner is not None:           # 勝敗が決まっている：maxQnew はゼロ（∵もう状態遷移しないため）
            maxQnew = 0
        else:                               # 勝敗決まっていない：maxQnew は現在選べる手の中でQを最大にするもの
            maxQnew = max([self.getQ(tuple(fs.board),act) for act in fs.get_possible_pos()])
        self.q[(tuple(s.board),a)] = pQ + self.alpha*((r + self.gamma*maxQnew)-pQ)  # Qの更新
        #print(str(s.board)+"with "+str(a)+" is updated from "+str(pQ)+" refs MAXQ="+str(maxQnew)+":"+str(r))
        #print(self.q)

    def act(self,board):
        return self.policy(board)

#### クラス PlayerQLB の宣言
# ボルツマン方策に基づくQ学習を行う
# クラス PlayerQL から，以下の点を変更
# (1) policy メソッドの内容を，ε-グリーディ方策からボルツマン方策に変更
# (2) それに関係して，__init__ メソッドのパラメータを変更

class PlayerQLB:
    def __init__(self,turn,name="QLB",alpha=0.3):
        self.name = name
        self.myturn = turn
        self.q = {}                             # set of s, a; キーが(state,act)となっている
#       self.e = e                              # eの確率でランダム方策，1-eの確率でグリーディ方策
        self.T = 0.01                              # 温度パラメータ，これが小さいほど Q が高い着手が選ばれやすくなる
        self.alpha = alpha                      # 学習率
        self.gamma = 0.9                        # 割引率
        self.last_move = None
        self.last_board = None
        self.totalgamecount = 0

    def policy(self,board):
        self.last_board = board.clone()         # 現在の盤面をコピー
        acts = board.get_possible_pos()         # 選択可能な着手のリスト

        qs = [self.getQ(tuple(self.last_board.board),act) for act in acts]
            # qは，盤面と着手の組をkey, Q値をvalue とする辞書
            # qsは，qのvalue であるQ値だけを並べたリスト
        qs_exp = [math.exp(que/self.T) for que in qs]
        qs_exp_sum = sum(qs_exp)
        boltzmann = [qep/qs_exp_sum for qep in qs_exp]
        i = random.choices(acts,weights = boltzmann)
        act = i[0]          # choices がリストを返すため，スカラに変換（choiceだとweightsを受け付けない）

        self.last_move = act
        return act

    def getQ(self,state,act):               # 現在の盤面と着手の組に対し，もしq値が存在しなければ，初期値1を与える
        # encourage exploration; "optimistc" 1.0 initial values
        # 未知の盤面のQ値を自動的に1に設定する：するとエージェントは未知の盤面を積極的に探索する
        if self.q.get((state,act)) is None:
            self.q[(state,act)] = 1
        return self.q.get((state,act))      # 辞書qのvalueをリターン


    def getGameResult(self,board):
        r = 0
        if self.last_move is not None:          # すなわち初手ではないとき
            if board.winner is None:            # 前の手番における盤面と着手の組が勝利にも敗北にもならなかったとき
                self.learn(self.last_board,self.last_move,0,board)
                pass
            else:
                if board.winner == self.myturn:
                    self.learn(self.last_board,self.last_move,1,board)
                elif board.winner != DRAW:
                    self.learn(self.last_board,self.last_move,-1,board)
                else:
                    self.learn(self.last_board,self.last_move,0,board)
            self.totalgamecount += 1
            self.last_move = None
            self.last_board = None

    def learn(self,s,a,r,fs):   # s:前手番の盤面，a:前手番の着手，r:報酬，fs:現在の盤面
        pQ = self.getQ(tuple(s.board),a)    # 前手番の盤面・着手のQ値
        if fs.winner is not None:           # 勝敗が決まっている：maxQnew はゼロ（∵もう状態遷移しないため）
            maxQnew = 0
        else:                               # 勝敗決まっていない：maxQnew は現在選べる手の中でQを最大にするもの
            maxQnew = max([self.getQ(tuple(fs.board),act) for act in fs.get_possible_pos()])
        self.q[(tuple(s.board),a)] = pQ + self.alpha*((r + self.gamma*maxQnew)-pQ)  # Qの更新

    def act(self,board):
        return self.policy(board)


def Human_vs_Random():
    p1 = PlayerHuman(PLAYER_X)
    p2 = PlayerRandom(PLAYER_O)
    game = TTT_GameOrganizer(p1,p2)
    game.progress()

def Random_vs_Random():
    p1 = PlayerRandom(PLAYER_X)
    p2 = PlayerRandom(PLAYER_O)
    game = TTT_GameOrganizer(p1,p2)
    game.progress()

def Human_vs_AlphaRandom():
    p1 = PlayerHuman(PLAYER_X)
    p2 = PlayerAlphaRandom(PLAYER_O)
    game = TTT_GameOrganizer(p1,p2)
    game.progress()

def MC_vs_MC():
    p1 = PlayerMC(PLAYER_X)
    p2 = PlayerMC(PLAYER_O)
    game = TTT_GameOrganizer(p1,p2,10)
    game.progress()

def Human_vs_MC():
    p1 = PlayerMC(PLAYER_X)
    p2 = PlayerMC(PLAYER_O)
    game = TTT_GameOrganizer(p1, p2, 10)
    game.progress()
    p1 = PlayerHuman(PLAYER_X)
    game = TTT_GameOrganizer(p1,p2,3)
    game.progress()

def QL_vs_QL():
    p1 = PlayerQL(PLAYER_X)
    p2 = PlayerQL(PLAYER_O)
    game = TTT_GameOrganizer(p1,p2,100000,False,False,10000)
    game.progress()
#    print(game.player_x.q)

def QLB_vs_QLB():
    p1 = PlayerQLB(PLAYER_X)
    p2 = PlayerQLB(PLAYER_O)
    game = TTT_GameOrganizer(p1,p2,100000,False,False,10000)
    game.progress()
#    print(game.player_x.q)

def QL_vs_QLB():
    p1 = PlayerQL(PLAYER_X)
    p2 = PlayerQLB(PLAYER_O)
    game = TTT_GameOrganizer(p1,p2,100000,False,False,10000)
    game.progress()
#    print(game.player_x.q)



def Human_vs_QL():
    p1 = PlayerQL(PLAYER_X)
    p2 = PlayerQL(PLAYER_O)
    game = TTT_GameOrganizer(p1,p2,100000,False,False,10000)
    game.progress()
    p1 = PlayerHuman(PLAYER_X)
    game = TTT_GameOrganizer(p1,p2,3)
    game.progress()

def Human_vs_QLB():
    p1 = PlayerQLB(PLAYER_X)
    p2 = PlayerQLB(PLAYER_O)
    game = TTT_GameOrganizer(p1,p2,100000,False,False,10000)
    game.progress()
    p1 = PlayerHuman(PLAYER_X)
    game = TTT_GameOrganizer(p1,p2,3)
    game.progress()

def MC_vs_QL():
    p1 = PlayerQL(PLAYER_X)
    p2 = PlayerQL(PLAYER_O)
    game = TTT_GameOrganizer(p1, p2, 100000, False, False, 10000)
    game.progress()
    p1 = PlayerMC(PLAYER_X)
    game = TTT_GameOrganizer(p1, p2, 100)
    game.progress()

def MC_vs_QLB():
    p1 = PlayerQLB(PLAYER_X)
    p2 = PlayerQLB(PLAYER_O)
    game = TTT_GameOrganizer(p1, p2, 100000, False, False, 10000)
    game.progress()
    p1 = PlayerMC(PLAYER_X)
    game = TTT_GameOrganizer(p1, p2, 100)
    game.progress()

#Human_vs_Random()
#Random_vs_Random()
#Human_vs_AlphaRandom()
#MC_vs_MC()
#Human_vs_MC()
#QL_vs_QL()
#QLB_vs_QLB()
#Human_vs_QL()
#Human_vs_QLB()
#QL_vs_QLB()
#MC_vs_QL()
MC_vs_QLB()
