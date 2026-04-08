#library imports.
import pygame
import time
import random

# define speed.
snake_speed=20

#window-size.
window_x=750
window_y=450

#defining_colors ( RGB )

black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)

#initialize pygame

pygame.init()
pygame.mixer.init()

# Load sound effects with error handling
# If sound files don't exist, the game will still run without sounds
eat_sound = None
game_over_sound = None

try:
    if os.path.exists('eat_sound.wav'):
        eat_sound = pygame.mixer.Sound('eat_sound.wav')
    if os.path.exists('game_over.wav'):
        game_over_sound = pygame.mixer.Sound('game_over.wav')
except:
    print("Warning: Could not load sound files. Game will run without sound effects.")

#initialise game window
pygame.display.set_caption('Snake game')
game_window=pygame.display.set_mode((window_x,window_y))

fps=pygame.time.Clock()

# default snake position

snake_pos=[100,50]

# defining first 4 blocks of snake
# body
snake_body = [  [100, 50],
                [90, 50],
                [80, 50],
                [70, 50]
            ]
# fruit position 
fruit_position = [random.randrange(1, (window_x//10)) * 10,
                  random.randrange(1, (window_y//10)) * 10]
fruit_spawn = True

# setting default snake direction 
# towards right
direction = 'RIGHT'
change_to = direction

#initial score -  0

score=0

def show_score(choice,color,fruit,size):
    score_font = pygame.font.SysFont(fruit, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)

# game over function
def game_over():
    # Play game over sound if available
    if game_over_sound:
        game_over_sound.play()
  
    # creating font object my_font
    my_font = pygame.font.SysFont('times new roman', 50)
    
    # creating a text surface on which text 
    # will be drawn
    game_over_surface = my_font.render('Your Score is : ' + str(score), True, red)
    
    # create a rectangular object for the text
    # surface object
    game_over_rect = game_over_surface.get_rect()
    
    # setting position of the text
    game_over_rect.midtop = (window_x/2, window_y/4)
    
    # blit will draw the text on screen
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    
    # after 2 seconds we will quit the 
    # program
    time.sleep(2)
    
    # deactivating pygame library
    pygame.quit()
    
    # quit the program
    quit()   

# Main Function
while True:
  
    # handling key events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # If two keys pressed simultaneously 
    # we don't want snake to move into two directions
    # simultaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Snake body growing mechanism 
    # if fruits and snakes collide then scores will be 
    # incremented by 10
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == fruit_position[0] and snake_pos[1] == fruit_position[1]:
        score += 10
        fruit_spawn = False
        # Play eat sound if available
        if eat_sound:
            eat_sound.play()
    else:
        snake_body.pop()
        
    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x//10)) * 10, 
                          random.randrange(1, (window_y//10)) * 10]
        
    fruit_spawn = True
    game_window.fill(black)
    
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(
          pos[0], pos[1], 10, 10))
        
    pygame.draw.rect(game_window, white, pygame.Rect(
      fruit_position[0], fruit_position[1], 10, 10))

    # Game Over conditions
    if snake_pos[0] < 0 or snake_pos[0] > window_x-10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > window_y-10:
        game_over()
    
    # Touching the snake body
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()
    
    # displaying score continuously
    show_score(1, white, 'times new roman', 20)
    
    # Refresh game screen
    pygame.display.update()

    # Frame Per Second /Refresh Rate
    fps.tick(snake_speed)     


