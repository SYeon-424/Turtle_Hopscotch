# Turtle_Hopscotch
# 거북이 두 마리로 땅따먹기를 하는 게임이다. 화면이 가득 찰 때 까지 진행되며, 검은 거북이는 wasd, 파란 거북이는 방향키로 조작할 수 있다. 
# 중간중간 스폰되는 아이템을 활용해 게임의 재미를 높였다. 화면이 가득 찼을 때 더 많은 부분을 차지하는 사람이 이긴다. 
import turtle
import time
import random

WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20 
ROWS = HEIGHT // GRID_SIZE
COLS = WIDTH // GRID_SIZE

#기본 설정
screen = turtle.Screen()
screen.title("Turtle_Hopscotch_ver.1")
screen.setup(WIDTH, HEIGHT)
screen.tracer(0) 

game_over_text = turtle.Turtle()
game_over_text.hideturtle()
game_over_text.penup()

tiles = [[0 for _ in range(COLS)] for _ in range(ROWS)]

painter = turtle.Turtle()
painter.hideturtle()
painter.speed(0)

item_green = turtle.Turtle()
item_green.shape("circle")
item_green.color("green")
item_green.penup()
item_green.hideturtle()

item_yellow = turtle.Turtle()
item_yellow.shape("square")
item_yellow.color("yellow")
item_yellow.penup()
item_yellow.hideturtle()

#위치보정
def _get_tile_center(col, row):
    return col * GRID_SIZE - WIDTH // 2 + GRID_SIZE // 2, row * GRID_SIZE - HEIGHT // 2 + GRID_SIZE // 2

player1 = turtle.Turtle()
player1.shape("turtle")
player1.color("black")
player1.penup()
player1.goto(_get_tile_center(COLS // 4, ROWS // 4)) 

player2 = turtle.Turtle()
player2.shape("turtle")
player2.color("blue")
player2.penup()
player2.goto(_get_tile_center(COLS * 3 // 4, ROWS * 3 // 4)) 

direction1 = None
direction2 = None

#게임오버 시스템
def _game_over(winner, color):
    global direction1, direction2
    direction1 = None
    direction2 = None
    game_over_text.goto(0, 0)
    game_over_text.color(color)
    game_over_text.write(f"GAME OVER!\nWinner: {winner}", align="center", font=("Arial", 24, "bold"))
    screen.update()
    time.sleep(5)
    screen.bye()

#승자 판별 시스템
def _is_winner():
    if not any(0 in row for row in tiles): 
        player1_count = sum(row.count(1) for row in tiles)
        player2_count = sum(row.count(2) for row in tiles)

        winner = "Player 1" if player1_count > player2_count else "Player 2"
        color = "black" if winner == "Player 1" else "blue"
        _game_over(winner, color) 

#플레이어 이동 구현
def _move():
    global direction1, direction2

    def _move_player(player, direction, player_id):
        if direction:
            col = int((player.xcor() + WIDTH // 2) // GRID_SIZE)
            row = int((player.ycor() + HEIGHT // 2) // GRID_SIZE)

            if direction == "up" and row < ROWS - 1:
                row += 1
                player.setheading(90)
            elif direction == "down" and row > 0:
                row -= 1
                player.setheading(270)
            elif direction == "left" and col > 0:
                col -= 1
                player.setheading(180)
            elif direction == "right" and col < COLS - 1:
                col += 1
                player.setheading(0)

            x, y = _get_tile_center(col, row)
            player.goto(x, y)
            _color(col, row, player_id)

            if tiles[row][col] == 3:
                item_green.hideturtle()
                tiles[row][col] = 0
                _spread(col, row, player_id)

            if tiles[row][col] == 4:
                item_yellow.hideturtle()
                tiles[row][col] = 0
                _clear_area(col, row, player_id) 

    _move_player(player1, direction1, 1)
    _move_player(player2, direction2, 2)

    screen.update()
    _is_winner() 
    screen.ontimer(_move, 100)

#타일 색 채우기
def _color(col, row, player):
    if 0 <= row < ROWS and 0 <= col < COLS and tiles[row][col] == 0:
        tiles[row][col] = player
        painter.penup()
        x, y = _get_tile_center(col, row)
        painter.goto(x - GRID_SIZE // 2, y - GRID_SIZE // 2)
        painter.pendown()
        painter.color("gray" if player == 1 else "lightblue")
        painter.begin_fill()
        for _ in range(4):
            painter.forward(GRID_SIZE)
            painter.left(90)
        painter.end_fill()

#초록 아이템 -> 주변부 채우기
def _spread(col, row, player_id):
    offsets = [(dx, dy) for dx in range(-2, 3) for dy in range(-2, 3)]
    
    for dx, dy in offsets:
        new_col, new_row = col + dx, row + dy
        if 0 <= new_row < ROWS and 0 <= new_col < COLS:
            _color(new_col, new_row, player_id)

#노랑 아이템 -> 상대 색 없애기
def _clear_area(col, row, player_id):
    offsets = [(dx, dy) for dx in range(-3, 4) for dy in range(-3, 4)]  

    for dx, dy in offsets:
        new_col, new_row = col + dx, row + dy

        if 0 <= new_row < ROWS and 0 <= new_col < COLS:
            if tiles[new_row][new_col] not in (0, player_id): 
                tiles[new_row][new_col] = 0  
                painter.penup()
                x, y = _get_tile_center(new_col, new_row)
                painter.goto(x - GRID_SIZE // 2, y - GRID_SIZE // 2)
                painter.pendown()
                painter.color("white") 
                painter.begin_fill()
                for _ in range(4):
                    painter.forward(GRID_SIZE)
                    painter.left(90)
                painter.end_fill()

#아이템 랜덤 스폰
def _spawn_items():
    empty_tiles = [(r, c) for r in range(ROWS) for c in range(COLS) if tiles[r][c] == 0]

    if empty_tiles:
        row, col = random.choice(empty_tiles)
        item_type = random.choice([3, 4])  

        if item_type == 3 and not item_green.isvisible():
            x, y = _get_tile_center(col, row)
            item_green.goto(x, y)
            item_green.showturtle()
            tiles[row][col] = 3

        if item_type == 4 and not item_yellow.isvisible():
            x, y = _get_tile_center(col, row)
            item_yellow.goto(x, y)
            item_yellow.showturtle()
            tiles[row][col] = 4  

    screen.ontimer(_spawn_items, 5000)

screen.listen()

#키보드 조작 관리
def _stop1(): global direction1; direction1 = None
def _stop2(): global direction2; direction2 = None

def _go_up1(): global direction1; direction1 = "up"
def _go_down1(): global direction1; direction1 = "down"
def _go_left1(): global direction1; direction1 = "left"
def _go_right1(): global direction1; direction1 = "right"

def _go_up2(): global direction2; direction2 = "up"
def _go_down2(): global direction2; direction2 = "down"
def _go_left2(): global direction2; direction2 = "left"
def _go_right2(): global direction2; direction2 = "right"

screen.onkeypress(_go_up1, "w")
screen.onkeypress(_go_down1, "s")
screen.onkeypress(_go_left1, "a")
screen.onkeypress(_go_right1, "d")
screen.onkeyrelease(_stop1, "w")
screen.onkeyrelease(_stop1, "s")
screen.onkeyrelease(_stop1, "a")
screen.onkeyrelease(_stop1, "d")

screen.onkeypress(_go_up2, "Up")
screen.onkeypress(_go_down2, "Down")
screen.onkeypress(_go_left2, "Left")
screen.onkeypress(_go_right2, "Right")
screen.onkeyrelease(_stop2, "Up")
screen.onkeyrelease(_stop2, "Down")
screen.onkeyrelease(_stop2, "Left")
screen.onkeyrelease(_stop2, "Right")

#시작
_spawn_items()
screen.ontimer(_move, 100)  
screen.mainloop()