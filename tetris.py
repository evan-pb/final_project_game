import pygame as pg
import numpy as np

pg.init()
pg.display.set_caption("TETRIS")
WIDTH, HEIGHT = 1010, 610
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
BLACK = "#000000"
WHITE = "#ffffff"
LIGHTGRAY = "#646464"
BLUE = "#39e7ed"
GREEN = "#32e132"
RED = "#ff0000"
YELLOW = "#fff41f"
PURPLE = "#4539ed"
ORANGE = "#ed710c"
MAGENTA = "#cf1fcc"
TOGGLE_SHADOW = True

reds = [RED, "#85150d", "#c7271c", "#520803", "#9e0f05", "#a31f15", "#f02416", "#d41002"]

font = pg.font.Font("assets/ARCADECLASSIC.ttf", 25)
smallfont = pg.font.Font("assets/ARCADECLASSIC.ttf", 15)
types = ["square", "stair_l", "stair_r", "L_l", "L_r", "line", "t"]
c_types = ["square", "stair_l", "stair_r", "L_l", "L_r", "line", "t", "star", "corner", "crescent", "step", "dot", "long_line"]

theme = pg.mixer.music.load("assets/theme.mp3")
blip = pg.mixer.Sound("assets/hitHurt.wav")
clear_sound = pg.mixer.Sound("assets/clear.mp3")
game_over_sound = pg.mixer.Sound("assets/game_over.mp3")
clear_sound.set_volume(30)

# Initialize constant objects

logo_image = pg.transform.scale_by(pg.image.load("assets/logo.png"), 1.5)
logo_rect = logo_image.get_rect()
logo_rect.center = (WIDTH // 2, 200)

start_text = font.render("PRESS ENTER TO START!", True, LIGHTGRAY)
start_rect = start_text.get_rect()
start_rect.center = (WIDTH // 2, 400)

pause_frame_rect = pg.rect.Rect(WIDTH//2 - 250, HEIGHT//2 - 100, 500, 200)
pause_fill_rect = pg.rect.Rect(WIDTH//2 - 245, HEIGHT//2 - 95, 490, 190)

pause_text = font.render("PAUSED", True, WHITE)
pause_text_rect = pause_text.get_rect()
pause_text_rect.center = (WIDTH//2, HEIGHT//2 - 30)

game_over_text = font.render("GAME OVER!", True, WHITE)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WIDTH//2, HEIGHT//2 - 30)

high_score_message = font.render("NEW HIGH SCORE!", True, WHITE)
high_score_message_rect = high_score_message.get_rect()
high_score_message_rect.center = (WIDTH // 2, game_over_rect.y)

restart_text = font.render("RESTART", True, WHITE)
restart_text_rect = restart_text.get_rect()
restart_text_rect.center = (WIDTH//2 - 120, HEIGHT//2 + 30)
restart_button_rect = pg.rect.Rect(restart_text_rect.x - 10, restart_text_rect.y - 8, restart_text_rect.width + 20, restart_text_rect.height + 16)

continue_text = font.render("QUIT", True, WHITE)
continue_text_rect = continue_text.get_rect()
continue_text_rect.center = (WIDTH//2 + 120, HEIGHT//2 + 30)
continue_button_rect = pg.rect.Rect(continue_text_rect.x - 10, continue_text_rect.y - 8, continue_text_rect.width + 20, continue_text_rect.height + 16)

time_text = font.render("00:00", True, LIGHTGRAY)
time_rect = time_text.get_rect()
time_rect.center = (WIDTH - 80, 40)

next_frame = pg.rect.Rect(WIDTH//2 + 170, 60, 150, 150)
next_fill = pg.rect.Rect(WIDTH//2 + 175, 65, 140, 140)

next_text = font.render("NEXT", True, WHITE)
next_rect = next_text.get_rect()
next_rect.center = (WIDTH//2 + 170 + 75, 30)

level_frame = pg.rect.Rect(WIDTH//2 + 170, 270, 150, 60)
level_fill = pg.rect.Rect(level_frame.x + 5, level_frame.y + 5, level_frame.width - 10, level_frame.height - 10)

level_text = font.render("LEVEL", True, WHITE)
level_rect = level_text.get_rect()
level_rect.center = (level_frame.centerx, 250)

level_count_text = font.render("0", True, LIGHTGRAY)
level_count_rect = level_count_text.get_rect()
level_count_rect.center = (level_frame.centerx, level_frame.centery)

lines_frame = pg.rect.Rect(WIDTH // 2 - 320, 220, 150, 70)
lines_fill = pg.rect.Rect(WIDTH // 2 - 315, 225, 140, 60)

lines_text = font.render("LINES", True, WHITE)
lines_rect = lines_text.get_rect()
lines_rect.center = (WIDTH // 2 - 320 + 60, 190)

lines_count_text = font.render("0000", True, LIGHTGRAY)
lines_count_rect = lines_count_text.get_rect()
lines_count_rect.center = lines_fill.centerx, lines_fill.centery

score_frame = pg.rect.Rect(WIDTH // 2 - 320, 80, 150, 70)
score_fill = pg.rect.Rect(WIDTH // 2 - 315, 85, 140, 60)

score_text = font.render("SCORE", True, WHITE)
score_rect = score_text.get_rect()
score_rect.center = (WIDTH // 2 - 320 + 60, 50)

score_count_text = font.render("00000", True, LIGHTGRAY)
score_count_rect = score_count_text.get_rect()
score_count_rect.center = score_fill.centerx, score_fill.centery

high_score_text = font.render("HIGH SCORE", True, WHITE)
high_score_rect = high_score_text.get_rect()
high_score_rect.center = (150, 40)

high_score_num = font.render("error", True, LIGHTGRAY)
high_score_num_rect = high_score_num.get_rect()
high_score_num_rect.x, high_score_num_rect.y = high_score_rect.x, 80

high_score_num_c = font.render("error", True, RED)
high_score_num_c_rect = high_score_num_c.get_rect()
high_score_num_c_rect.x, high_score_num_c_rect.y = high_score_rect.x, 120

# Settings components

settings_text = font.render("SETTINGS", True, WHITE)
settings_rect = settings_text.get_rect()
settings_rect.center = (WIDTH - 150, 40)
settings_button = pg.rect.Rect(settings_rect.x - 10, settings_rect.y - 10, settings_rect.width + 20, settings_rect.height + 20)

settings_box = pg.rect.Rect(settings_button.x, 100, settings_button.width, 500)
settings_box_fill = pg.rect.Rect(settings_box.x + 5, settings_box.y + 5, settings_box.width - 10, settings_box.height - 10)

frame_rect = pg.rect.Rect(WIDTH // 2 - 155, 0, 310, 610)
fill_rect = pg.rect.Rect(WIDTH // 2 - 150, 5, 300, 600)

toggle_shadow_text = smallfont.render("Drop shadow", True, WHITE)
toggle_shadow_rect = toggle_shadow_text.get_rect()
toggle_shadow_rect.center = (WIDTH - 140, 180)
shadow_rect_toggle = pg.rect.Rect(WIDTH - 245, 173, 15, 15)

toggle_next_text = smallfont.render("Show next", True, WHITE)
toggle_next_rect = toggle_next_text.get_rect()
toggle_next_rect.left, toggle_next_rect.y = (toggle_shadow_rect.left, toggle_shadow_rect.y + 50)
next_rect_toggle = pg.rect.Rect(shadow_rect_toggle.x, shadow_rect_toggle.y + 50, 15, 15)

toggle_challenge_text = smallfont.render("Challenge", True, RED)
toggle_challenge_rect = toggle_challenge_text.get_rect()
toggle_challenge_rect.left, toggle_challenge_rect.y = (toggle_next_rect.left, toggle_next_rect.y + 50)
challenge_toggle_rect = pg.rect.Rect(next_rect_toggle.x, next_rect_toggle.y + 50, 15, 15)


def display_settings():
    screen.blit(toggle_shadow_text, toggle_shadow_rect)
    screen.blit(toggle_next_text, toggle_next_rect)
    screen.blit(toggle_challenge_text, toggle_challenge_rect)
    if TOGGLE_SHADOW:
        pg.draw.rect(screen, WHITE, shadow_rect_toggle)
    else:
        pg.draw.rect(screen, LIGHTGRAY, shadow_rect_toggle)
    if SHOW_NEXT_BLOCK:
        pg.draw.rect(screen, WHITE, next_rect_toggle)
    else:
        pg.draw.rect(screen, LIGHTGRAY, next_rect_toggle)
    if CHALLENGE:
        pg.draw.rect(screen, RED, challenge_toggle_rect)
    else:
        pg.draw.rect(screen, LIGHTGRAY, challenge_toggle_rect)

def draw_overlay():
    screen.fill(BLACK)
    pg.draw.rect(screen, WHITE, frame_rect)
    pg.draw.rect(screen, BLACK, fill_rect)
    
    game.mat_to_image(block.color)

    if SHOW_NEXT_BLOCK:
        pg.draw.rect(screen, WHITE, next_frame)
        pg.draw.rect(screen, BLACK, next_fill)
        screen.blit(next_text, next_rect)
        step = next_fill.width // 4
        # Draw grid lines for next block display

        NEXT_MATRIX = np.zeros((4,4))
        if len(np.shape(next_block.shape)) == 1:
            height, length = 1, 4
        else:
            height, length = np.shape(next_block.shape)

        NEXT_MATRIX[1:height+1, 0:length] = next_block.shape 
        NEXT_MATRIX = np.rot90(NEXT_MATRIX[::-1], 3)
        
        draw = np.where(NEXT_MATRIX == 1)
        for i in range(len(draw[0])):
            rect = pg.rect.Rect(next_fill.x + draw[0][i] * step, next_fill.y + draw[1][i] * step, step, step)
            pg.draw.rect(screen, next_block.color, rect)
            
        for i in range(1,4):
            pg.draw.rect(screen, LIGHTGRAY, pg.rect.Rect(next_fill.x + i * step, next_fill.y, 2, next_fill.height))
            pg.draw.rect(screen, LIGHTGRAY, pg.rect.Rect(next_fill.x , next_fill.y + i * step, next_fill.height, 2))
        
    time_text = font.render(f"{minutes:02d}:{seconds%60:02d}", True, LIGHTGRAY)
    screen.blit(time_text, time_rect)

    screen.blit(lines_text, lines_rect)
    pg.draw.rect(screen, WHITE, lines_frame)
    pg.draw.rect(screen, BLACK, lines_fill)

    if CHALLENGE:
        lines_count_text = font.render(f"{game.lines:04d}", True, RED)
    else:
        lines_count_text = font.render(f"{game.lines:04d}", True, LIGHTGRAY)
    screen.blit(lines_count_text, lines_count_rect)

    screen.blit(score_text, score_rect)
    pg.draw.rect(screen, WHITE, score_frame)
    pg.draw.rect(screen, BLACK, score_fill)

    if CHALLENGE:
        score_count_text = font.render(f"{game.score:05d}", True, RED)
    else:
        score_count_text = font.render(f"{game.score:05d}", True, LIGHTGRAY)
    screen.blit(score_count_text, score_count_rect)

    screen.blit(level_text, level_rect)
    pg.draw.rect(screen, WHITE, level_frame)
    pg.draw.rect(screen, BLACK, level_fill)

    if CHALLENGE:
        level_count_text = font.render("???", True, RED)
    else:
        level_count_text = font.render(str(game.level), True, LIGHTGRAY) 
    screen.blit(level_count_text, level_count_rect)

    for i in range(1, 10):
            pg.draw.rect(screen, LIGHTGRAY, pg.rect.Rect(WIDTH // 2 - 150 + (30 * i), 5, 2, 600))
    for i in range(1, 20):
        pg.draw.rect(screen, LIGHTGRAY, pg.rect.Rect(WIDTH // 2 - 150, 5 + 30 * i, 300, 2))
        
def get_high_score():
    with open("high_score.txt") as f:
        scores = f.readlines()
    return [int(i.strip()) for i in scores]

def update_high_score(idx, score):
    with open("high_score.txt", "r") as f:
        lines = [int(i.strip()) for i in f.readlines()]
    lines[idx] = score
    with open("high_score.txt", "w") as f:
        f.writelines([f"{i}\n" for i in lines])
    
    

class Game:
    def __init__(self):
        self.matrix = np.zeros((20, 10))
        self.color_map = np.full((20,10), "       ")
        self.lines = 0
        self.score = 0
        self.level = 1


    def clear_shadow(self):
        locations = np.where(self.matrix == 3)
        for i in range(len(locations[0])):
            self.matrix[locations[0][i], locations[1][i]] = 0


    def spawn(self, block):

        height, length = np.shape(block.shape)
        spawn_location = (0, 4)
        # Replace empty part of main number matrix with 1's where there is a block
        self.matrix[spawn_location[0]:height, spawn_location[1]:spawn_location[1]+length] = block.shape 

        
    def rotate(self, n:int, block):
        locations = np.where(self.matrix == 1)
        if block.type != "dot":
            if 1 in self.matrix:
                board = self.matrix.copy()
                block_array = board[min(locations[0]):max(locations[0])+1, min(locations[1]):max(locations[1])+1]
                length, width = np.shape(block_array)
                if locations:
                    try:
                        if 2 not in self.matrix[min(locations[0]):min(locations[0])+width, min(locations[1]):min(locations[1])+length+1]:
                            self.matrix[min(locations[0]):min(locations[0])+length, min(locations[1]):min(locations[1])+width] = np.zeros((length, width))
                            self.matrix[min(locations[0]):min(locations[0])+width, min(locations[1]):min(locations[1])+length] = np.rot90(block_array, n)
                            for i in range(len(locations)):
                                self.color_map[locations[0][i], locations[1][i]] = "       "
                            for i in range(len(locations)):
                                self.color_map[locations[0][i], locations[1][i]] = block.color

                    except ValueError:
                        self.matrix[min(locations[0]):min(locations[0])+length, min(locations[1]):min(locations[1])+width] = block_array

            if TOGGLE_SHADOW:
                self.clear_shadow()
                self.highlight_drop()

    
    def mat_to_image(self, color = WHITE):
        fill_values, fill_values_2, fill_values_3 = np.where(self.matrix == 1), np.where(self.matrix == 2), np.where(self.matrix == 3)
        for i in range(len(fill_values[0])):
            rect = pg.rect.Rect((WIDTH//2-150) + 30 * fill_values[1][i], 5 + (30 * fill_values[0][i]), 30, 30)
            pg.draw.rect(screen, color, rect)
        if 2 in self.matrix:
            for i in range(len(fill_values_2[0])):
                rect2 = pg.rect.Rect((WIDTH//2-150) + 30 * fill_values_2[1][i], 5 + (30 * fill_values_2[0][i]), 30, 30)
                pg.draw.rect(screen, self.color_map[fill_values_2[0][i], fill_values_2[1][i]], rect2)
        if 3 in self.matrix:
            for i in range(len(fill_values_3[0])):
                rect3 = pg.rect.Rect((WIDTH//2-150) + 30 * fill_values_3[1][i], 5 + (30 * fill_values_3[0][i]), 30, 30)
                pg.draw.rect(screen, LIGHTGRAY, rect3)


    def lower_block(self, block):
        locations = np.where(self.matrix == 1)  # Find where the floating block is
        color = block.color
    
        if 19 in locations[0]: # Check if block is at the bottom of the screen
            for i in range(len(locations[0])):
                self.matrix[locations[0][i], locations[1][i]] = 2
                self.color_map[locations[0][i], locations[1][i]] = color 
            self.score += 10   
            blip.play()      

        elif 2 in self.matrix[[locations[0][i] + 1 for i in range(len(locations[0]))], locations[1]]: # Check if there is a block under any of the four squares
            for i in range(len(locations[0])):
                self.matrix[locations[0][i], locations[1][i]] = 2  
                self.color_map[locations[0][i], locations[1][i]] = color      
            self.score += 10   
            blip.play() 
        else:
            new_locations = [[i + 1 for i in locations[0]], locations[1]]  # define locations for the block after it has lowered by 1 square
            # Clear old values from matrix
            for i in range(len(locations[0])):
                self.matrix[locations[0][i], locations[1][i]] = 0
            # Add new values to matrix
            for i in range(len(locations[0])):
                self.matrix[new_locations[0][i], new_locations[1][i]] = 1


    def left_right(self, dir: bool):
        # dir = True -> left, False -> right
        self.clear_shadow() if TOGGLE_SHADOW else None
        locations = np.where(self.matrix == 1)  # Find where the floating block is
        if 1 in self.matrix:
            if dir and min(locations[1]) > 0: # If block is told to move left and it's not at the edge
                # Check if adjacent spaces are occupied
                if 2 not in self.matrix[locations[0], [locations[1][i] - 1 for i in range(len(locations[0]))]]:
                    new_locations = [locations[0], [i - 1 for i in locations[1]]]
                    for i in range(len(locations[0])):
                        self.matrix[locations[0][i], locations[1][i]] = 0
                    for i in range(len(locations[0])):
                        self.matrix[new_locations[0][i], new_locations[1][i]] = 1

            if not dir and max(locations[1]) < 9:
                if 2 not in self.matrix[locations[0], [locations[1][i] + 1 for i in range(len(locations[0]))]]:
                    new_locations = [locations[0], [i + 1 for i in locations[1]]]
                    for i in range(len(locations[0])):
                        self.matrix[locations[0][i], locations[1][i]] = 0
                    for i in range(len(locations[0])):
                        self.matrix[new_locations[0][i], new_locations[1][i]] = 1


    def drop_block(self, block):
        while 1 in self.matrix:
            self.lower_block(block)
            self.mat_to_image(block.color)
            draw_overlay()
            pg.display.flip()
            pg.time.delay(12)
        self.clear_shadow() if TOGGLE_SHADOW else None


    def check_clear(self):
        clear_rows = []
        for i in range(np.shape(self.matrix)[0]):
            if (1 not in self.matrix[i,:]) and (3 not in self.matrix[i,:]) and (0 not in self.matrix[i,:]):
                clear_rows.append(i) # Add the numerical row index of the row(s) that need(s) to be cleared
        if clear_rows:
            # Add cleared rows to top of matrix
            self.matrix = np.delete(self.matrix, clear_rows, axis=0)
            self.matrix = np.vstack([np.zeros((len(clear_rows), 10)),self.matrix])
            self.color_map = np.delete(self.color_map, clear_rows, axis = 0)
            self.color_map = np.vstack([np.full((len(clear_rows), 10), "       "), self.color_map])
            self.lines += len(clear_rows)
            if len(clear_rows) == 4:
                self.score += 500
            else:
                self.score += 50 * len(clear_rows) 
            clear_sound.play()
            if TOGGLE_SHADOW:
                self.clear_shadow()
                self.highlight_drop()


    def highlight_drop(self):
        locations = np.where(self.matrix == 1)
        distances = []
        if np.any(locations):
            slice_array = self.matrix[min(locations[0]):, min(locations[1]):max(locations[1])+1]
            for i in range(max(locations[1])+1-min(locations[1])): # For every vertical row under the block
                count = 0
                j = 0
                block_start = False
                while True: # Iterate through vertical 1-d columns to count the space needed to move down to draw the shadow
                    if j == len(slice_array[:,i]): # Prevent index error
                        break
                    if slice_array[j,i] == 1:
                        block_start = True
                        j+=1
                    elif not slice_array[j,i] and block_start: # Only start counting the empty space once a 1 has been detected
                        count += 1
                        j += 1
                    elif not slice_array[j,i]:
                        j += 1
                    else:
                        break
                distances.append(count)
            shadow_location = [[i + min(distances) for i in locations[0]], locations[1]]
            for i in range(len(locations[0])):
                if not self.matrix[shadow_location[0][i], shadow_location[1][i]]:
                    self.matrix[shadow_location[0][i], shadow_location[1][i]] = 3        



class Block:
    def __init__(self, type: str) -> None:
        global CHALLENGE
        self.type = type
        self.color = WHITE
        if self.type == "square":
            self.shape = np.array([[1, 1],
                                  [1, 1]])
            self.color = YELLOW
        elif self.type == "stair_l":
            self.shape = np.array([[1, 1, 0],
                                   [0, 1, 1]])
            self.color = RED
        elif self.type == "stair_r":
            self.shape = np.array([[0, 1, 1],
                                   [1, 1, 0]])     
            self.color = GREEN       
        elif self.type == "L_l":
            self.shape = np.array([[1, 1, 1],
                                   [1, 0, 0]])
            self.color = ORANGE
        elif self.type == "L_r":
            self.shape = np.array([[1, 0, 0],
                                   [1, 1, 1]])
            self.color = PURPLE
        elif self.type == "line":
            self.shape = np.array([[1, 1, 1, 1]])
            self.color = BLUE

        elif self.type == "t":
            self.shape = np.array([[1, 1, 1],
                                   [0, 1, 0]])
            self.color = MAGENTA

        elif self.type == "star":
            self.shape = np.array([[0, 1, 0],
                                   [1, 1, 1],
                                   [0, 1, 0]])
            # self.color = GOLD
        elif self.type == "corner":
            self.shape = np.array([[1, 0, 0],
                                   [1, 0, 0],
                                   [1, 1, 1]])
            # self.color = PINK
        elif self.type == "crescent":
            self.shape = np.array([[1, 1, 1],
                                   [1, 0, 1]])
            # self.color = 
        elif self.type == "step":
            self.shape = np.array([[1, 0],
                                   [1, 1]])
        elif self.type == "dot":
            self.shape = np.array([[1]])
        elif self.type == "long_line":
            self.shape = np.array([[1, 1, 1, 1, 1]])
            # self.color = WHITE
        if CHALLENGE:
            self.color = np.random.choice(reds)


if __name__ == "__main__":
    RUNNING = True
    PLAYING = False
    PAUSED = False
    GAME_OVER = False
    SHOW_SETTINGS = False 
    SHOW_NEXT_BLOCK = True
    CHALLENGE = False
    NEXT_MATRIX = np.zeros((4,4))
    high_scores = get_high_score()
    new_high_score = False
    frame_count = 0
    dummy = 0
    pg.mixer.music.play(-1)
    while RUNNING:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                RUNNING = False
            if e.type == pg.KEYDOWN and not PLAYING:
                if e.key == pg.K_RETURN:
                    new_high_score = False
                    game = Game()
                    PLAYING = True
                    SHOW_SETTINGS = False
                    next_block = Block(np.random.choice(types))
                    block = Block(np.random.choice(types))
                if e.key == pg.K_ESCAPE:
                    pg.mixer.music.stop()
                    exec(open("main.py").read())
            if e.type == pg.KEYDOWN and PLAYING and not GAME_OVER:
                if e.key == pg.K_ESCAPE:
                    PAUSED = not PAUSED
                if not PAUSED:
                    if e.key == pg.K_a:
                        game.left_right(True)
                    if e.key == pg.K_d:
                        game.left_right(False)
                    if e.key == pg.K_s:
                        game.lower_block(block)
                    if e.key == pg.K_q or e.key == pg.K_LEFT or e.key == pg.K_w:
                        game.rotate(1, block)
                    if e.key == pg.K_e or e.key == pg.K_RIGHT:
                        game.rotate(-1, block)
                    if e.key == pg.K_SPACE:
                        game.drop_block(block)
            if e.type == pg.MOUSEBUTTONDOWN and PAUSED or e.type == pg.MOUSEBUTTONDOWN and GAME_OVER:
                if (
                    restart_button_rect.left < mouse[0] < restart_button_rect.right
                    and restart_button_rect.top < mouse[1] < restart_button_rect.bottom
                ):
                    PAUSED = False
                    GAME_OVER = False
                    new_high_score = False
                    game = Game()
                    frame_count = 0
                if (
                    continue_button_rect.left < mouse[0] < continue_button_rect.right
                    and continue_button_rect.top < mouse[1] < continue_button_rect.bottom
                ):
                    PLAYING = False
                    PAUSED = False
                    GAME_OVER = False
                    frame_count = 0
                pg.mixer.music.unpause()
            if e.type == pg.MOUSEBUTTONDOWN and not PLAYING:
                if (
                    settings_button.left < mouse[0] < settings_button.right
                    and settings_button.top < mouse[1] < settings_button.bottom
                ):
                    SHOW_SETTINGS = not SHOW_SETTINGS

            if e.type == pg.MOUSEBUTTONDOWN and not PLAYING and SHOW_SETTINGS:
                if (
                    shadow_rect_toggle.left < mouse[0] < shadow_rect_toggle.right
                    and shadow_rect_toggle.top < mouse[1] < shadow_rect_toggle.bottom
                ):
                    TOGGLE_SHADOW = not TOGGLE_SHADOW
                if (
                    next_rect_toggle.left < mouse[0] < next_rect_toggle.right
                    and next_rect_toggle.top < mouse[1] < next_rect_toggle.bottom
                ):
                    SHOW_NEXT_BLOCK = not SHOW_NEXT_BLOCK
                if (
                    challenge_toggle_rect.left < mouse[0] < challenge_toggle_rect.right
                    and challenge_toggle_rect.top < mouse[1] < challenge_toggle_rect.bottom
                ):
                    CHALLENGE = not CHALLENGE
                if CHALLENGE:
                    TOGGLE_SHADOW, SHOW_NEXT_BLOCK = False, False
                if TOGGLE_SHADOW or SHOW_NEXT_BLOCK:
                    CHALLENGE = False
            

        mouse = pg.mouse.get_pos()
        
        if not PLAYING: # Title screen objects
            dummy = 0
            screen.fill(BLACK)
            screen.blit(logo_image, logo_rect)
            screen.blit(start_text, start_rect)
            if (
                settings_button.left < mouse[0] < settings_button.right
                and settings_button.top < mouse[1] < settings_button.bottom
            ):
                pg.draw.rect(screen, LIGHTGRAY, settings_button)
            screen.blit(settings_text, settings_rect)
            if SHOW_SETTINGS:
                pg.draw.rect(screen, WHITE, settings_box)
                pg.draw.rect(screen, BLACK, settings_box_fill)
                display_settings()
            
            screen.blit(high_score_text, high_score_rect)

            high_score_num = font.render(str(high_scores[0]).strip(), True, WHITE)
            high_score_c_num = font.render(str(high_scores[1]).strip(), True, RED)
            screen.blit(high_score_num, high_score_num_rect)
            screen.blit(high_score_c_num, high_score_num_c_rect)

        elif PAUSED or GAME_OVER: # Pause / game over menu
            pg.draw.rect(screen, WHITE, pause_frame_rect)
            pg.draw.rect(screen, BLACK, pause_fill_rect)
            screen.blit(pause_text, pause_text_rect) if PAUSED else None
            if (
                restart_button_rect.left < mouse[0] < restart_button_rect.right
                and restart_button_rect.top < mouse[1] < restart_button_rect.bottom
            ):
                pg.draw.rect(screen, LIGHTGRAY, restart_button_rect)
            if (
                continue_button_rect.left < mouse[0] < continue_button_rect.right
                and continue_button_rect.top < mouse[1] < continue_button_rect.bottom
            ):
                pg.draw.rect(screen, LIGHTGRAY, continue_button_rect)
            screen.blit(restart_text, restart_text_rect)
            screen.blit(continue_text, continue_text_rect)
            p = 1 if CHALLENGE else 0
            if game.score > int(high_scores[p]):
                high_scores[p] = game.score
                update_high_score(p, game.score)
                new_high_score = True
            if GAME_OVER:
                # Show score, high score if previous one was beat, and amount of lines cleared here
                if new_high_score:                    
                    screen.blit(high_score_message, high_score_message_rect)
                else:
                    screen.blit(game_over_text, game_over_rect)
                pg.mixer.music.pause()
                game_over_sound.play() if dummy == 0 else None
                dummy += 1


        else:
            frame_count += 1
            dummy = 0

            if 1 not in game.matrix:  # If there are no moving blocks
                block = next_block
                if CHALLENGE:
                    next_block = Block(np.random.choice(c_types))
                    gravity = np.random.randint(10, 60)
                else:
                    next_block = Block(np.random.choice(types))
                    gravity = 65 ** (1 - (game.level - 1) / 35) # asymptote equation to ensure no zero division error
                game.spawn(block)
            else: 
                if not frame_count % np.ceil(gravity): # When speed curve reaches numbers less than one, round up to one
                    game.lower_block(block)
            if 3 not in game.matrix and 1 in game.matrix and TOGGLE_SHADOW:
                game.highlight_drop()
            game.check_clear()
            seconds = frame_count // 60
            minutes = seconds // 60

            game.level = game.lines // 10 + 1
            

            if 2 in game.matrix[0,:]:
                GAME_OVER = True

            # Final method to read the matrix and draw the tetris grid from that
            game.mat_to_image(color=block.color)

            draw_overlay()
            
        pg.display.flip()
        clock.tick(60)


    pg.quit()

