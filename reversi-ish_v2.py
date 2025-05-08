"""

Copyright © 2025 AglaoDev-jp

---

Code by AglaoDev-jp © 2025, licensed under the MIT License.
Image by AglaoDev-jp © 2025, licensed under CC BY 4.0.

---

External Library:

- pygame:
  Copyright © 2000-2023 Pygame developers
  Licensed under the LGPL v2.1 License. See LICENSE-pygame.txt or visit:
  [Pygame License](https://www.pygame.org/docs/license.html)

A heartfelt thanks to all developers and contributors who have made this library possible.

// This file was created and refined with support from OpenAI’s conversational AI, ChatGPT.
// We greatly benefited from its assistance in idea generation and code improvements.

"""

import pygame # Pygameライブラリをインポート(GUI)
import sys # sys.exit()でプログラムを終了するために必要
import random # 疑似ランダム生成ライブラリ。AIの石選択に使用。
from pathlib import Path # ファイルパスの操作に使用。osライブラリよりも記述がシンプル and 効率的

# --- 初期設定 ---
pygame.init() # Pygameの初期化（必ず最初に実行）

# --- サイズの設定 ---
BOARD_WIDTH = 640 # ボードの幅
BOARD_OFFSET_X = 160 # ボード横のウインドウ
WIDTH = BOARD_WIDTH + BOARD_OFFSET_X # 画面の幅
HEIGHT = 640 # 画面の高さ
ROWS, COLS = 8, 8 # 盤は8×8マス
CELL_SIZE = BOARD_WIDTH // COLS # 各マスのサイズ（1マス = 640 ÷ 8 = 80ピクセル）

# --- 画像の読み込み ---
# スクリプトがあるフォルダを基準に画像を読み込む
script_dir = Path(__file__).resolve().parent # pathlibはスクリプトの位置に基づいて”動的に”絶対パスを生成します💪
image_path = script_dir / "image.png"  # pathlib的なパス指定
# 画像ファイルをPygameのサーフェス（Surface）オブジェクトとして読み込みます。
# image_path は Path 型なので(pathlibで作ったから)Pygameで読み込むには文字列（str）に変換する必要があります。
start_screen_image = pygame.image.load(str(image_path)) # ←これだけだと読み込んだ画像のサイズは元の画像サイズのままです（例：400×300の画像ならそのまま）。
# 指定した大きさに画像（サーフェス）を変形する関数。
start_screen_image = pygame.transform.scale(start_screen_image, (WIDTH, HEIGHT)) # ←これで800×640ピクセルにリサイズ。

# --- 色の定義（RGB形式） --- Pygameは RGB 形式のみ(RGBA にすると、透明度（Alpha）も追加できるようです。)
GREEN = (0, 128, 0) # 盤面の緑色
BLACK = (0, 0, 0)   # 黒石・線・文字の色
WHITE = (255, 255, 255) # 白石・文字の色
GRAY = (128, 128, 128) # ガイド・文字の色
YELLOW = (255, 255, 0) # 文字のホバー色
"""
RGB = Red（赤）, Green（緑）, Blue（青） の頭文字です。
各値は 0〜255 の整数で表されます。
各色の強さを指定して、最終的な色を合成します。
つまり (R, G, B) の3つの値で1つの色を表現します
"""

# --- フォント ---
font = pygame.font.SysFont("Meiryo", 36)

# --- ウィンドウの作成 ---
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("リバーシ”風”ゲーム") # ウィンドウタイトルの設定

# --- ボタン領域 ---

# リスタートボタン
restart_button_rect = pygame.Rect(20, 360, 120, 40) 
# 難易度選択ボタン（ボタン配置を変更しています）
easy_button = pygame.Rect(20, 410, 180, 60)
normal_button = pygame.Rect(20, 480, 180, 60)
hard_button = pygame.Rect(20, 550, 180, 60)  # ← NEW! "てごわい"

# --- ガイド on off ボタン ---
guide_button = pygame.Rect(580, 550, 200, 60)

# --- 状態管理（ゲーム全体のフラグ管理、初期化を行う） ---

""" 8x8 の2次元リスト（例：board[y][x] で各マスにアクセス）初期化は reset_board() 関数で行われます。"""
board = []            # 現在の盤面の状態を保持するための変数。

current_player = 1    # 現在の手番変数。状態管理へ。
"""
1 → 黒（プレイヤー）
2 → 白（AI）
使用場所：
プレイヤーとAIの切り替え（current_player = 2 など）
パス判定（check_pass() 関数内）
描画時のターン表示（draw_board() 関数内）
"""
game_over = False     # ゲーム終了フラグ（Trueになると結果を表示する）
result_text = ""      # 勝敗メッセージを表示するための文字列（例："黒の勝ち！"）
pass_message = ""     # パス時のメッセージ（例："白パス！"）
difficulty = None     # 難易度設定（"easy" or "normal" or "hard" を格納、Noneを入れてある状態）
mode = "start"        # 現在のモード（"start"：開始画面, "playing"：対局中, "game_over"：終了画面）
ai_pending = False    # AIの処理待ち状態（TrueでAIの手番待ち）
ai_timer = 0          # AI処理のタイミングを調整するためのタイマー（ms）ウエイトを入れないとAIが速すぎて逆に操作感がよくなかった。0に戻すため。
show_guide = True     # 有効な手をガイドとして表示するか（Trueで表示ON）

AI_DELAY = 500    # AIの動く速度（ミリ秒）定数アピールで大文字+アンダーバー。

# --- 重みマップ ---
weights_easy = [[0]*COLS for _ in range(ROWS)] # すべて 0 点
weights_normal = [
    [100, -20, 10, 5, 5, 10, -20, 100],
    [-20, -50, -2,-2,-2,-2,-50,-20],
    [10,  -2,  0, 0, 0, 0,  -2, 10],
    [5,   -2,  0, 0, 0, 0,  -2, 5 ],
    [5,   -2,  0, 0, 0, 0,  -2, 5 ],
    [10,  -2,  0, 0, 0, 0,  -2, 10],
    [-20, -50, -2,-2,-2,-2,-50,-20],
    [100, -20, 10, 5, 5, 10, -20, 100]
]

# --- 盤面評価関数（ミニマックス用） ---
def evaluate_board(board, ai_color):
    opponent = 1 if ai_color == 2 else 2  # AIが2ならプレイヤーは1、AIが1ならプレイヤーは2（相手の色）
    score = 0 # 評価値（AIにとって有利かどうか）を初期化
    corners = [(0,0),(0,7),(7,0),(7,7)] # 角のマス（高評価ポイント）
    xs      = [(1,1),(1,6),(6,1),(6,6)] # 角の隣のXマス（危険ポイント）

    for y in range(ROWS):  # 盤面の行
        for x in range(COLS):  # 盤面の列
            cell = board[y][x]  # 現在のマスの内容（0:空, 1:黒, 2:白）

            if cell == ai_color: 
                # AIの石 → +1（石の数）＋ 位置による補正（角なら+100、Xなら-30、それ以外は0）
                score += 1 + (100 if (y,x) in corners else -30 if (y,x) in xs else 0)

            elif cell == opponent: 
                # 相手の石 → -1（石の数）＋ 位置による補正（角なら-100、Xなら+30、それ以外は0
                score -= 1 + (100 if (y,x) in corners else -30 if (y,x) in xs else 0)
                # 代入演算子（複合代入演算子）＋ 三項演算子
                # 三項演算子 (A if 条件1 else B if 条件2 else C)
                """ 
                | 場所     | 値の計算                | AI視点での増減 |
                | ------ | ------------------- | -------- |
                | AIの石/角 | `+(1 + 100) = +101` | +101     |
                | AIの石/X | `+(1 + -30) = -29`  | -29      |
                | 相手の石/角 | `-(1 + 100) = -101` | -101     |
                | 相手の石/X | `-(1 + -30) = +29`  | +29      |
                → score に `1 + (100 if (y,x) in corners else -30 if (y,x) in xs else 0)`
                を += / -= で加減算してる感じ？
                """
                
    return score # 最終的な評価値を返す（正数ならAIが有利、負数なら不利）

# --- ミニマックス法 + α–β法 ---

def minimax_ab(board, depth, alpha, beta, maximizing_player, ai_color):
    """
    ミニマックス法 + α–β法 を使って盤面を評価する関数
    - ミニマックス法: AI側は評価値を最大化、プレイヤー側は評価値を最小化すると仮定して探索
    - α–β法: 不要な探索を枝刈りすることで高速化
    引数:
      board: 現在の盤面
      depth: 残り探索深さ
      alpha: 最大化側(AI側)の下限値
      beta: 最小化側(プレイヤー側)の上限値
      maximizing_player: TrueならAI側の手番、Falseならプレイヤー側の手番
      ai_color: AI側の石の値(白=2 または 黒=1)
    """
    # AI側とプレイヤー側の色を決定
    opponent = 1 if ai_color == 2 else 2 # プレイヤー側の石の値
    current = ai_color if maximizing_player else opponent # 今回打つのはAI側(最大化)またはプレイヤー側(最小化)

    indent = "  " * (3 - depth)  # 深さに応じたインデントで階層を表現（デバッグ用）

    # 終端条件: 深さ0または現在の色に有効手がない場合
    if depth == 0 or not has_valid_move(board, current):
        # 盤面を評価してスコアを返す
        score = evaluate_board(board, ai_color)
        # α‑β探索の深さと枝刈り状況をインデント付きで `print` 出力。
        print(f"{indent}depth={depth}, {'MAX' if maximizing_player else 'MIN'}: 終端→ score={score}")
        return score

    moves = get_valid_moves(board, current) # 打てる手のリストを取得

    if not moves: # 置ける場所が無いってことでパス処理です。
        # パス処理もログ出力
        print(f"{indent}depth={depth}, {'MAX' if maximizing_player else 'MIN'}: パス")
        # パス: 有効手がなければ相手の番として探索を続行 (深さを1減らす)
        return minimax_ab(board, depth-1, alpha, beta, not maximizing_player, ai_color)

    if maximizing_player:
        max_eval = -float('inf') # 最大化初期評価値
        for x, y in moves:
            # 盤面をコピーしてシミュレーション（仮想着手）
            new_board = [row[:] for row in board]
            new_board[y][x] = current
            flip_stones(new_board, x, y, current)

            # 再帰的に次の深さを探索 (プレイヤー側) 
            print(f"{indent}MAX: ({x},{y}) を仮想で置く → 深さ {depth-1}")
            eval = minimax_ab(new_board, depth-1, alpha, beta, False, ai_color)
            print(f"{indent}MAX: ({x},{y}) の評価値 = {eval}") 

            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval) # αの更新 (AI側の下限値を上げる)

            # α–β法 (β <= α ならこれ以上探索しても結果に影響しない => 枝刈り！)
            if beta <= alpha:
                print(f"{indent}MAX: βカット発生！（β={beta} <= α={alpha}）")
                break # βカット: プレイヤー側(最小化)の探索を省略

        print(f"{indent}MAX: 最終スコア = {max_eval}")
        return max_eval # 最大評価値を返す

    else:
        # 最小化の探索
        min_eval = float('inf') # 最小化の初期評価値
        for x, y in moves:
            new_board = [row[:] for row in board]
            new_board[y][x] = current
            flip_stones(new_board, x, y, current)

            # 再帰的に次の深さを探索 (AI)
            print(f"{indent}MIN: ({x},{y}) を仮想で置く → 深さ {depth-1}")
            eval = minimax_ab(new_board, depth-1, alpha, beta, True, ai_color)
            print(f"{indent}MIN: ({x},{y}) の評価値 = {eval}")

            min_eval = min(min_eval, eval)
            beta = min(beta, eval)  # βの更新 (プレイヤー側の上限値を下げる)

            # α–β法 (β <= α => 枝刈り)
            if beta <= alpha:
                print(f"{indent}MIN: αカット発生！（β={beta} <= α={alpha}）")
                break # αカット: AI側(最大化)の探索を省略

        print(f"{indent}MIN: 最終スコア = {min_eval}")
        return min_eval # 最小評価値を返す


# --- α–β法を使った最善手探索 ---
def get_best_move_ab(board, depth, ai_color):
    """
    α–β法でAI側の最善手を探索する関数
    - AI側の全有効手を評価し、最も高い評価値の手を候補として保持
    - 同じ評価値の手が複数ある場合はランダムで1つ選択
    """
    moves = get_valid_moves(board, ai_color)  # AIの有効手を取得
    alpha = -float('inf')  # αの初期値 (最大化プレイヤーの下限)
    beta = float('inf')    # βの初期値 (最小化プレイヤーの上限)
    best_score = -float('inf') # スコア更新：初期化
    best_moves = [] # ベスト候補手のリスト

    for x, y in moves:
        # 各手をシミュレートして評価
        new_board = [row[:] for row in board]
        new_board[y][x] = ai_color
        flip_stones(new_board, x, y, ai_color)

        score = minimax_ab(new_board, depth-1, alpha, beta, False, ai_color)
        
        if score > best_score:
            best_score = score
            best_moves = [(x, y)]  # 新しい最高評価値のリストに置き換え
        elif score == best_score:
            best_moves.append((x, y))  # 同じ評価値ならリストに追加

        alpha = max(alpha, score)  # αの更新 (AI側の下限値を上げる)

    # 候補手からランダムに1つ選択して返す
    return random.choice(best_moves) if best_moves else None

# --- AI戦略の定義 ---
def ai_move_easy():
    """簡単モード: すべてランダムに有効手を選択"""
    global current_player, pass_message
    pass_message = "" # パスメッセージを消去

    # AI（白=2）の有効な手（置けるマス）を取得
    moves = get_valid_moves(board, 2)

    if not moves: # 打てる場所がなければパス処理へ
        check_pass()
        return
    
    # 有効な手の中からランダムに1つ選んで着手
    x,y = random.choice(moves)
    board[y][x] = 2 # 石を置く
    flip_stones(board, x, y, 2) # 挟んだ石を裏返す

    current_player = 1 # 手番をプレイヤー（黒=1）に戻す
    check_pass() # 次のプレイヤーがパスかどうか判定

def ai_move_normal():
    """ふつうモード: 重み付き評価関数で候補手を選択"""
    global current_player, pass_message
    pass_message = "" # パスメッセージを消去

    best_score = -float('inf') # スコアの初期化（最小値からスタート）
    candidates = []  # ベスト候補手のリスト

    # 全マスを調べて「置けるマス」を探す
    for y in range(ROWS): # 行を探す
        for x in range(COLS): # 列を探す
            if is_valid_move(board, x, y, 2):  # そのマスに置けるか？
                score = weights_normal[y][x] # 重みマップのスコアを取得
                if score > best_score:
                    best_score, candidates = score, [(x,y)]  # スコア更新：リストを初期化
                elif score == best_score:
                    candidates.append((x,y))  # 同じスコアなら候補に追加

    if candidates:
        x,y = random.choice(candidates)  # 候補からランダムに1つ選択
        board[y][x] = 2 # 石を置く
        flip_stones(board, x, y, 2) # 挟んだ石を裏返す
    
    else: # 打てる手がない → パス！
        check_pass()

    current_player = 1 # 手番をプレイヤー（黒=1）に戻す
    check_pass() # 次のプレイヤーがパスかどうか判定

def ai_move_hard():
    """てごわいモード: ミニマックス法 + α–β法 で最善手を探索"""
    global current_player, pass_message
    pass_message = "" # パスメッセージを消去

    # 探索の「深さ」を設定 (今回は3手先まで読む安牌設定、6で結構苦しい)
    move = get_best_move_ab(board, depth=3, ai_color=2)
    if move:
        x, y = move
        board[y][x] = 2 # 石を置く
        flip_stones(board, x, y, 2) # 挟んだ石を裏返す

    else: # 打てる手がない？じゃあパス処理だね
        check_pass() 

    current_player = 1 # プレイヤー(黒=1)に手番を戻す
    check_pass() # 次のプレイヤーがパスかどうか判定

# --- 難易度ごとのAI戦略マップ ---
# 難易度設定に応じて、それぞれの関数を呼び出すための辞書マッピング
# 例: difficulty = "easy" のとき → ai_move_easy() を呼び出す
ai_strategies = {
    "easy": ai_move_easy,
    "normal": ai_move_normal,
    "hard": ai_move_hard,
}

# --- 盤面初期化関数 ---
def reset_board():
    global board, current_player, game_over, result_text, pass_message
    board = [[0 for _ in range(COLS)] for _ in range(ROWS)] # 初期は全部空　8×8の2次元リスト（リバーシ盤）を全て0で初期化
    # 初期配置（中央4マス）
    board[3][3], board[4][4] = 2, 2 # 白石
    board[3][4], board[4][3] = 1, 1 # 黒石
    current_player = 1 # 黒から開始
    game_over = False # ゲーム終わってないよ処理
    result_text = "" # 勝敗表示初期化
    pass_message = "" # パスメッセージも初期化

reset_board()

"""  
  0 1 2 3 4 5 6 7   ← x（列番号 col）
0 □ □ □ □ □ □ □ □
1 □ □ □ □ □ □ □ □
2 □ □ □ □ □ □ □ □
3 □ □ □ ○ ● □ □ □  ← y = 3 行
4 □ □ □ ● ○ □ □ □  ← y = 4 行
5 □ □ □ □ □ □ □ □
6 □ □ □ □ □ □ □ □
7 □ □ □ □ □ □ □ □
↑
y（行番号 row）

□：空きマス（0）  
●：黒石（1）  
○：白石（2）

使い方：board[y][x]
"""

# --- 置けるか判定 ---
def is_valid_move(board, x, y, player):
    # すでに石が置かれているマスには置けない
    if board[y][x] != 0:
        return False

    # 8方向（縦・横・斜め）をすべて調べる
    directions = [(-1, -1), (-1, 0), (-1, 1),  # 左上、上、右上
                  (0, -1),          (0, 1),   # 左、       右
                  (1, -1), (1, 0), (1, 1)]     # 左下、下、右下

    # プレイヤーが 1（黒）なら相手は 2（白）、その逆も
    opponent = 2 if player == 1 else 1

    # 各方向についてチェック
    for dx, dy in directions:
        nx, ny = x + dx, y + dy  # 隣のマスの座標
        has_opponent = False     # 相手の石を挟めるかどうかのフラグ

        # 盤の範囲内で探索を続ける
        while 0 <= nx < COLS and 0 <= ny < ROWS:
            if board[ny][nx] == opponent:
                # 相手の石がある場合 → さらに奥へ進んで調べる
                has_opponent = True
                nx += dx
                ny += dy
            elif board[ny][nx] == player:
                # 自分の石にぶつかった時、相手の石を1個以上挟んでいればOK
                if has_opponent:
                    return True  # 挟めてるので「ここに置ける」
                break  # 相手の石を挟んでいなければNG
            else:
                # 空きマスや盤外に出たらこの方向はNG
                break

    return False  # どの方向にも置けない場合

# --- 裏返し処理 ---
def flip_stones(board, x, y, player):
    # 8方向すべてを調べる
    directions = [(-1, -1), (-1, 0), (-1, 1),  # 左上、上、右上
                  (0, -1),          (0, 1),   # 左、       右
                  (1, -1), (1, 0), (1, 1)]     # 左下、下、右下

    # 相手プレイヤーの番号（黒=1、白=2）
    opponent = 2 if player == 1 else 1

    # 各方向を調べてひっくり返せる石を探す
    for dx, dy in directions:
        nx, ny = x + dx, y + dy  # 隣のマスからスタート
        path = []  # ひっくり返す候補の石の座標を一時的に記録するリスト

        # 盤面内をチェックしながら、相手の石が続いてるか調べる
        while 0 <= nx < COLS and 0 <= ny < ROWS:
            if board[ny][nx] == opponent:
                # 相手の石ならpathに追加してさらに奥へ進む
                path.append((nx, ny))
                nx += dx
                ny += dy
            elif board[ny][nx] == player:
                # 自分の石にぶつかった → 挟まれてることが確定！
                for px, py in path:
                    board[py][px] = player  # 相手の石を自分の石に裏返す
                break  # この方向の裏返しは終わり
            else:
                # 空マスや範囲外だったらその方向は失敗（パスは無効）
                break
"""
dx = delta x（変化量）
dy = delta y（変化量）っていう意味。
nx = next x（次のx）
ny = next y（次のy） っていう意味。
よく使う表現らしい。
"""
# --- 有効な手があるか判定 ---# 打てるマスが1つでもあるか？ True/Falseで答える
def has_valid_move(board, player):
    for y in range(ROWS):        # すべての行を調べて
        for x in range(COLS):    # すべての列を調べて
            if is_valid_move(board, x, y, player):  # そのマスに置けるなら
                return True      # 1個でも見つかったら「置ける！」→ True
    return False  # 全部調べてもダメだったら → False

# --- 有効な手のリストを取得 --- 打てるマスを全部リストで返す(ガイドにも使っています)
def get_valid_moves(board, player):
    moves = []  # 空のリストを用意して
    for y in range(ROWS):
        for x in range(COLS):
            if is_valid_move(board, x, y, player):
                moves.append((x, y))  # 置けるマスの座標をリストに追加
    return moves  # 最終的に全部返す

# --- パス処理 ---
def check_pass():
    global current_player, pass_message, ai_pending, ai_timer
    # 有効手がなければパス
    if not has_valid_move(board, current_player):
        # パスメッセージ設定（黒→白、白→黒）
        pass_message = "黒パス！" if current_player == 1 else "白パス！"
        # 手番を渡す
        current_player = 2 if current_player == 1 else 1

        # AIの手番なら予約
        if current_player == 2 and has_valid_move(board, 2):
            ai_pending = True
            ai_timer = pygame.time.get_ticks()

# --- 石数を数える ---
def count_stones(board):
    # board は 2次元リストなので、1行ずつ（row）調べて、row.count(1)でその行の黒石数を取得
    # (ジェネレータ式（generator expression）)
    # (処理 for 要素 in シーケンス)
    # sum() で全行分を合計 → 合計数がわかる
    black = sum(row.count(1) for row in board) # 黒石（1）がいくつあるか数える
    white = sum(row.count(2) for row in board) # 白石（2）がいくつあるか数える
    # Pythonではカンマ区切りで2つ以上の値を返すと、タプル（tuple）でまとめて返されます。
    return black, white  # タプルで返す（(黒, 白)）
# print(count_stones(board)) #タプルになってるか確認(出まくるので止めています)
"""
・盤面描画の draw_board() で、石の数を表示
・ゲーム終了時の勝敗判定
のために使われています。
"""

# --- AI（ランダム or 重み付き） ---
def ai_move():
    global current_player
    best_score = -float('inf')  # 最初は最小スコア（どんな値よりも小さい）を入れておく
    candidates = []             # 最終的に選ばれうる候補手を入れるリスト

    # 難易度に応じて使用する重みマップを切り替える
    weights = weights_easy if difficulty == "easy" else weights_normal

    # 盤上すべてのマスをチェック
    for y in range(ROWS): # 盤面の中から「置ける場所」を全部探す
        for x in range(COLS):
            if is_valid_move(board, x, y, 2):  # AI（白=2）が置けるなら
                score = weights[y][x]         # そのマスの重みを取得

                # 最高スコアの手が更新されたらリストを入れ替える
                if score > best_score:
                    best_score = score
                    candidates = [(x, y)]
                elif score == best_score:
                    candidates.append((x, y))  # 同点なら追加（ランダムに選ぶため）

    # 候補がある場合 → どれかひとつをランダムに選んで手を打つ
    if candidates:
        x, y = random.choice(candidates)
        board[y][x] = 2                  # 石を置く
        flip_stones(board, x, y, 2)     # 裏返す処理
        current_player = 1              # 手番を黒に渡す
        check_pass()                    # パス処理のチェック

# --- 描画 ---
def draw_board():
    # 背景（盤面全体）を緑に塗りつぶし
    screen.fill(GREEN)
    """screen は「描画先（ウィンドウ）」のサーフェス（Surface）
    fill() はそのサーフェス全体を、指定した色（RGB）で塗りつぶします。"""

    # ★ スタート画面の描画処理（モードが "start" のとき）★
    if mode == "start":
        # 背景にスタート画面用の画像を表示
        screen.blit(start_screen_image, (0, 0))
        """
        screen.blit(image, (x, y))
        画像やテキストを画面に貼る処理。
        blit は「貼り付ける（blit = bit block transfer）」の略なんだそうな。
        画面の左上 (0, 0) に画像を表示するという意味。
        """

        # 現在のマウスの位置を取得
        mouse_pos = pygame.mouse.get_pos()

        # ホバー判定　マウスがそれぞれのボタンの上にあるか判定して、ホバー色を設定
        easy_text_color = YELLOW if easy_button.collidepoint(mouse_pos) else WHITE
        normal_text_color = YELLOW if normal_button.collidepoint(mouse_pos) else WHITE
        hard_text_color = YELLOW if hard_button.collidepoint(mouse_pos) else WHITE  # ← NEW!

        # 背景ボタン描画　難易度選択ボタンとガイド切替ボタンを描画
        pygame.draw.rect(screen, BLACK, easy_button)
        pygame.draw.rect(screen, BLACK, normal_button)
        pygame.draw.rect(screen, BLACK, hard_button)  # ← NEW!
        pygame.draw.rect(screen, WHITE, guide_button)
        """
        pygame.draw.rect(描画先, 色, 四角の情報, 線の太さ)
        
        描画先 → だいたい screen。
        四角の情報 → pygame.Rect(x, y, w, h) で定義。
        線の太さ → 省略すると「塗りつぶし」、数字を入れると「枠線だけ」。
        """

        # テキスト描画 各ボタン上に文字を描画（Meiryoフォント使用）
        easy_text = font.render("かんたん", True, easy_text_color)
        normal_text = font.render("ふつう", True, normal_text_color)
        hard_text = font.render("てごわい", True, hard_text_color)  # ← NEW!
        guide_text = font.render(f"ガイド:{'ON' if show_guide else 'OFF'}", True, BLACK)

        # テキストをボタンの上に配置
        screen.blit(easy_text, (easy_button.x + 20, easy_button.y + 10))
        screen.blit(normal_text, (normal_button.x + 20, normal_button.y + 10))
        screen.blit(hard_text, (hard_button.x + 20, hard_button.y + 10))  # ← NEW!
        screen.blit(guide_text, (guide_button.x + 6, guide_button.y + 6))
        """
        pygame.font.Font.render()
        font.render("文字", True, 文字色, 背景色)
        Pygameは文字列をそのまま画面に出せないので、
        いったん画像（Surface）に変換してから blit() で貼り付けます。
        True はアンチエイリアス（文字をなめらかにする）を有効にするかどうか。
        第3引数は文字の色を入れるところ。
        """

        # スタート画面では他の描画は行わないので return で終了
        return

    # ★ 対局中（"playing"）またはゲーム終了時（"game_over"）の描画処理 ★

    # --- 有効な手のガイド表示 ---
    if not game_over and current_player == 1 and show_guide:
        # 現在のプレイヤー（黒）に有効な手をすべて取得
        valid_moves = get_valid_moves(board, current_player)
        for x, y in valid_moves:
            # セルの中心座標を計算して、小さな灰色の円でガイドを描画
            center_x = x * CELL_SIZE + BOARD_OFFSET_X + CELL_SIZE // 2
            center_y = y * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(screen, GRAY, (center_x, center_y), 5)

    # --- セルと石の描画 ---
    for y in range(ROWS):
        for x in range(COLS):
            # 各セル（マス）の位置とサイズを計算して、枠を描画
            rect = pygame.Rect(x * CELL_SIZE + BOARD_OFFSET_X, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)

            # 石の描画（1:黒、2:白）
            if board[y][x] == 1:
                pygame.draw.circle(screen, BLACK, rect.center, CELL_SIZE // 2 - 5)
            elif board[y][x] == 2:
                pygame.draw.circle(screen, WHITE, rect.center, CELL_SIZE // 2 - 5)

    # --- 石の数を表示（左側に） ---
    black, white = count_stones(board)
    black_text = font.render(f"黒: {black}", True, BLACK)
    white_text = font.render(f"白: {white}", True, WHITE)
    screen.blit(black_text, (10, 100))
    screen.blit(white_text, (10, 140))

    # --- 現在の手番（どちらのターンか）を表示 ---
    if not game_over:
        # 今の手番の色の石を表示（黒 or 白）
        if current_player == 1:
            pygame.draw.circle(screen, BLACK, (20, 225), 15)
        else:
            pygame.draw.circle(screen, WHITE, (20, 225), 15)
        turn_text = font.render("の番", True, BLACK)
        screen.blit(turn_text, (40, 200))

    # --- パスメッセージを表示（例："白パス！"） ---
    if pass_message and not game_over:
        color = BLACK if "黒" in pass_message else WHITE
        pass_text = font.render(pass_message, True, color)
        screen.blit(pass_text, (10, 260))

    # --- ゲーム終了時の結果表示とリスタートボタン ---
    if game_over:
        # 結果（勝ち・負け・引き分け）メッセージを色付きで表示
        color = BLACK if "黒" in result_text else WHITE if "白" in result_text else GRAY
        result = font.render(result_text, True, color)
        screen.blit(result, (20, 300))

        # 「もう一度」ボタンを描画
        pygame.draw.rect(screen, BLACK, restart_button_rect)
        btn_text = font.render("もう一度", True, WHITE)
        screen.blit(btn_text, (restart_button_rect.x + 5, restart_button_rect.y + 5))

# --- スタート画面でのクリック処理 ---
def handle_click_start(pos):
    global difficulty, mode, show_guide
    if easy_button.collidepoint(pos):
        difficulty = "easy"
        mode = "playing"
        reset_board()
    elif normal_button.collidepoint(pos):
        difficulty = "normal"
        mode = "playing"
        reset_board()
    elif hard_button.collidepoint(pos):  # ← NEW!
        difficulty = "hard"
        mode = "playing"
        reset_board()
    elif guide_button.collidepoint(pos):
        show_guide = not show_guide

# --- ゲームオーバー画面でのクリック処理 ---
def handle_click_result(pos):
    global mode
    if restart_button_rect.collidepoint(pos):
        reset_board()
        mode = "start"

# --- ゲーム中のクリック処理（プレイヤーが石を置く） ---
def handle_click_game(pos):
    global current_player, ai_pending, ai_timer, pass_message
    pass_message = "" # パスメッセージを消去
    if current_player != 1 or ai_pending:
        return  # プレイヤーの手番でなければ何もしない

    mouse_x, mouse_y = pos
    grid_x = (mouse_x - BOARD_OFFSET_X) // CELL_SIZE
    grid_y = mouse_y // CELL_SIZE

    if 0 <= grid_x < COLS and 0 <= grid_y < ROWS:
        if is_valid_move(board, grid_x, grid_y, current_player):
            board[grid_y][grid_x] = current_player
            flip_stones(board, grid_x, grid_y, current_player)
            current_player = 2
            check_pass()
            if current_player == 2 and has_valid_move(board, 2):
                ai_pending = True
                ai_timer = pygame.time.get_ticks()  # 現在時刻を記録してウエイト処理に使う

# --- メインループ ---
# ゲームが動いている限りは、ずっと繰り返すため while 文
while True:
    # --- イベント処理：操作（マウス・キーボード・ウィンドウ閉じ）をチェック ---
    # 「×」ボタンを押した時に、きれいに終了させるコードです。Pygameでは必須。
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # Pygameを終了
            sys.exit()     # プログラム終了

        # --- マウスクリックイベント（MOUSEBUTTONDOWN） ---
        if event.type == pygame.MOUSEBUTTONDOWN:
            # モードごとにクリック処理を分岐
            if mode == "start":
                handle_click_start(event.pos) # ゲーム開始前の「スタート画面」モード
            elif game_over:
                handle_click_result(event.pos) # game_over
            else:
                handle_click_game(event.pos) # playing中

    # --- 手番プレイヤーに有効な手がなければパス処理を行う ---
    if mode == "playing" and not game_over:
        check_pass()

    # --- AIの手番処理（0.5秒待機してから実行） ---
    if mode == "playing" and not game_over:
        # 現在の手番に有効手がない → パス処理
        if not has_valid_move(board, current_player):
            # パスメッセージをセット
            pass_message = "黒パス！" if current_player == 1 else "白パス！"
            # 手番を渡す
            current_player = 2 if current_player == 1 else 1

            # AI の手番になったら予約
            if current_player == 2 and has_valid_move(board, 2):
                ai_pending = True
                ai_timer   = pygame.time.get_ticks()

        # AI の予約がある → 一定待ってから実行
        elif ai_pending:
            # 0.5秒以上経ったら
            if pygame.time.get_ticks() - ai_timer > AI_DELAY: # ← 定数にしました。
                ai_pending     = False        # 予約クリア
                pass_message   = ""           # AI が動くのでパスメッセージを消す
                ai_strategies.get(difficulty, ai_move_normal)()

        # それ以外（ユーザー操作のターン）は何もしない（handle_click_game で処理）
    
    # --- 両者とも打てないとゲーム終了 ---
    if not game_over and not has_valid_move(board, 1) and not has_valid_move(board, 2):
        black, white = count_stones(board)
        if   black > white: result_text = "黒の勝ち！"
        elif white > black: result_text = "白の勝ち！"
        else:                result_text = "引き分け！"
        game_over    = True
        pass_message = ""  # パスメッセージを消去

    # --- 描画処理 ---
    draw_board()           # 盤面を描画
    pygame.display.flip()  # 描画を更新（画面に反映）