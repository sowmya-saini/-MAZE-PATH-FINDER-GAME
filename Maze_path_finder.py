from collections import deque
import copy

min_path = [] 
maze = [] 

def isValidBoundaries(i, j, square_matrix):
    n = len(square_matrix)
    m = len(square_matrix[0])
    if 0 <= i < n and 0 <= j < m and (square_matrix[i][j] == "." or square_matrix[i][j] == "T"):
        return True
    return False
       
def MinPathInMaze(i, j, square_matrix, min_path):
    check = deque()
    check.append((i, j))
    levels = []
    levels.append((i, j))
    boundaries = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    while check:
        l = []
        for _ in range(len(check)):
            i, j = check.popleft()
            for b in boundaries:
                r = i + b[0]
                c = j + b[1]
                if isValidBoundaries(r, c, square_matrix):
                    if square_matrix[r][c] == ".":
                        square_matrix[r][c] = "#"
                        check.append((r, c))
                        l.append((r, c))
                    else:
                        min_path.append(len(levels))
                        return min_path
                        break         
        if l:
            levels.append(l)
    return min_path
            
def matrix_traverse(square_matrix, n, m, min_path):
    for i in range(n):
        for j in range(m):
            if square_matrix[i][j] == "S":
                MinPathInMaze(i, j, square_matrix, min_path)
                break

print("ENTER MAZE DETAILS")
n, m = map(int, input().split())
for _ in range(n):
    row = list(input())
    maze.append(row)

maze1 = copy.deepcopy(maze)

matrix_traverse(maze1, n, m, min_path)
    
print("Original Maze:", maze)
print("Modified Maze:", maze1)
print("min_path:", min_path)

# Importing
import pygame
import sys

# Initializig
pygame.init()

# SCREEN
w, h = 800, 600
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("3 GUESSES MINIMUM PATH IN MAZE")
screen.fill((255, 255, 255))

# EXIT BUTTON
button_w, button_h = 100, 50
button_color = (255, 255, 170)
button_text_color = (0, 0, 0)
button_font = pygame.font.Font(None, 36)
button_x, button_y = 350, 500
button_rect = pygame.Rect(button_x, button_y, button_w, button_h)
button_text = button_font.render("Exit", True, button_text_color)
button_text_rect = button_text.get_rect(center=button_rect.center)

# Colors

GREEN =(0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
Gray= (128, 128, 128)
LIGHT_LAVENDER = (230, 230, 255)  
LIGHT_MINT_GREEN = (204, 255, 204)  
LIGHT_LEMON = (255, 255, 204)  

start = (0, 0)
end = (0, 0)

for i,v1 in enumerate(maze):
    for j, v2 in enumerate(v1):
        if v2 == "S":
            start = (i, j)
        if v2 == "T":
            end = (i, j)

#CELL DETAILS
cell = 50
grid_width = len(maze[0]) * cell
grid_height = len(maze) * cell
grid_x_offset = (w - grid_width) // 2
grid_y_offset = (h - grid_height) // 2

#Font
font = pygame.font.Font(None, 25)  # Use default system font with size 36

#PLAYER POSITION
sp = start
ep = end
print(sp, ep)
# Player Icon
player_color = (0, 0, 255)  # Blue
player_size = 20

#Variables 
shortest_path = min_path[0]
chances = 3
moves_count = 0
won = False

# MAIN LOOP
run = True
while run:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False
        elif i.type == pygame.MOUSEBUTTONDOWN:
            if i.button == 1 and button_rect.collidepoint(i.pos):
                run = False
        elif chances == 0 and not won:
            text = font.render("YOU CAN'T PLAY NOW", True, BLACK)  # Render the text
            text_rect = text.get_rect(center=(400, 570))  # Get the rect of the text
            screen.blit(text, text_rect)  # Blit the text onto the screen surface
        elif i.type == pygame.KEYDOWN:
            if moves_count < shortest_path and not won:
                if i.key == pygame.K_DOWN:
                    sp_new = (sp[0] + 1, sp[1])
                    moves_count += 1
                    if isValidBoundaries(sp_new[0], sp_new[1], maze):
                        sp = sp_new
                elif i.key == pygame.K_UP:
                    sp_new = (sp[0] - 1, sp[1])
                    moves_count += 1
                    if isValidBoundaries(sp_new[0], sp_new[1], maze):
                        sp = sp_new
                elif i.key == pygame.K_LEFT:
                    moves_count += 1
                    sp_new = (sp[0], sp[1]-1)
                    if isValidBoundaries(sp_new[0], sp_new[1], maze):
                        sp = sp_new
                elif i.key == pygame.K_RIGHT:
                    moves_count += 1
                    sp_new = (sp[0], sp[1]+1)
                    if isValidBoundaries(sp_new[0], sp_new[1], maze):
                        sp = sp_new
            else:
                chances -= 1
                moves_count = 0
                sp = start
                if chances == 2 and not won:
                    text = font.render("You lost Try again! 1 chance completed", True, BLACK)  # Render the text
                    text_rect = text.get_rect(center=(400, 10))  # Get the rect of the text
                    screen.blit(text, text_rect)  # Blit the text onto the screen surface
                if chances == 1 and not won:
                    text = font.render("You lost Try again! 2 chances completed", True, BLACK)  # Render the text
                    text_rect = text.get_rect(center=(400, 30))  # Get the rect of the text
                    screen.blit(text, text_rect)  # Blit the text onto the screen surface
                if chances == 0 and not won:
                    text = font.render("SORRY YOU LOST !!! YOUR CHANCES ARE COMPLETED!", True, BLACK)  # Render the text
                    text_rect = text.get_rect(center=(400, 50))  # Get the rect of the text
                    screen.blit(text, text_rect)  # Blit the text onto the screen surface
            if maze[sp[0]][sp[1]] == "T" and chances >0:
                text = font.render("You Won!", True, BLACK)  # Render the text
                text_rect = text.get_rect(center=(400, 570))  # Get the rect of the text
                screen.blit(text, text_rect)  # Blit the text onto the screen surface
                won = True
   
    #DRAW BUTTON
    pygame.draw.rect(screen, button_color, button_rect)
    screen.blit(button_text, button_text_rect)

    # DRAW GRID
    for index1, min_path1 in enumerate(maze):
        for index2, min_path2 in enumerate(min_path1):
            cell_x = index2 * cell + grid_x_offset  # Adjusted x-coordinate with offset
            cell_y = index1 * cell + grid_y_offset  # Adjusted y-coordinate with offset
            if min_path2 == "#":
                pygame.draw.rect(screen, BLACK, (cell_x, cell_y, cell, cell))
            elif min_path2 == "S":
                text = font.render("START", True, RED)
                text_rect = text.get_rect(center=(cell_x + cell // 2, cell_y + cell // 2))
                screen.blit(text, text_rect)
            elif min_path2 == "T":
                text = font.render("END", True, RED)
                text_rect = text.get_rect(center=(cell_x + cell // 2, cell_y + cell // 2))
                screen.blit(text, text_rect)
            else:
                pygame.draw.rect(screen, LIGHT_MINT_GREEN, (cell_x, cell_y, cell, cell))
            pygame.draw.rect(screen, Gray, (cell_x, cell_y, cell, cell), 1)

    # Draw Player
    player_rect = pygame.Rect(sp[1] * cell + grid_x_offset + (cell - player_size) // 2,
    sp[0] * cell + grid_y_offset + (cell - player_size) // 2,player_size, player_size)
    pygame.draw.rect(screen, player_color, player_rect)
    pygame.display.flip()

# EXIT
pygame.quit()
sys.exit()