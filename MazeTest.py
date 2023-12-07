import pygame
import sys
import time
from random import choice, randrange
from collections import deque
from queue import PriorityQueue

# Kích thước cửa sổ và ô lưới
WIDTH, HEIGHT = 1200, 700
TILE_SIZE = 30
COLS, ROWS = (WIDTH-200) // TILE_SIZE, HEIGHT // TILE_SIZE

# Màu sắc
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
GREEN= (0, 255, 0)
NAVY=(0,0,128)
LINEN=(250,240,230)
STEEL_BLUE=(176,196,222)
CHIFFON=(255,250,205)
yellow = (255, 255, 0)
queued_vertices = set()
Node_count=0
search_time=0
# Khởi tạo Pygame
pygame.init()

# Tạo màn hình
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Runner")

# Font
font = pygame.font.SysFont(None, 55)
player_image = pygame.image.load("player_image.png")
player_image = pygame.transform.scale(player_image, (TILE_SIZE, TILE_SIZE))
player2_image = pygame.image.load("player2_image.png")
player2_image = pygame.transform.scale(player2_image, (TILE_SIZE, TILE_SIZE))
food_image = pygame.image.load("food_image.png")
food_image = pygame.transform.scale(food_image, (TILE_SIZE, TILE_SIZE))
wall_image = pygame.image.load("wall_image.png")
wall_image = pygame.transform.scale(wall_image, (TILE_SIZE, TILE_SIZE))
# Quy ước kí hiệu ô lưới
WALL = "W"
PATH = "P"
PLAYER = "S"
FOOD = "F"

# Hàm tạo mê cung bằng DFS
def generate_maze():
    grid = [[WALL] * COLS for _ in range(ROWS)]
    stack = deque([(1, 1)])
    while stack:
        x, y = stack[-1]
        grid[y][x] = PATH
        neighbors = [
            (x + dx, y + dy)
            for dx, dy in [(0, -2), (2, 0), (0, 2), (-2, 0)]
            if 0 < x + dx < COLS - 1 and 0 < y + dy < ROWS - 1 and grid[y + dy][x + dx] == WALL
        ]
        if neighbors:
            nx, ny = choice(neighbors)
            grid[(y + ny) // 2][(x + nx) // 2] = PATH
            stack.append((nx, ny))
        else:
            stack.pop()
    return grid

# Hàm vẽ mê cung
def draw_maze(grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if (x, y) in queued_vertices: 
                if food_found:
                    pygame.draw.rect(screen, WHITE, rect)
                    #pygame.time.delay(100)
                else:# Kiểm tra xem ô có phải là đỉnh đã thêm vào queue hay không
                    pygame.draw.rect(screen, yellow, rect)
            else:
                if cell == WALL:
                    #pygame.draw.rect(screen, BLACK, rect)
                    wall_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    screen.blit(wall_image, wall_rect)
                elif cell == PATH:
                    pygame.draw.rect(screen, WHITE, rect)

# Hàm vẽ người chơi
def draw_player(player):
    rect = pygame.Rect(player[0] * TILE_SIZE, player[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    screen.blit(player_image, rect)
def draw_player2(player):
    rect = pygame.Rect(player[0] * TILE_SIZE, player[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    screen.blit(player2_image, rect)
# Hàm kiểm tra va chạm với thức ăn
def check_food(player, food):
    return player == food

# Hàm di chuyển người chơi
def move_player(player, direction):
    x, y = player
    dx, dy = direction
    new_x, new_y = x + dx, y + dy
    if 0 <= new_x < COLS and 0 <= new_y < ROWS and maze[new_y][new_x] != WALL:
        return new_x, new_y
    return x, y

# Hàm tạo vị trí mới cho thức ăn
def generate_food(maze):
    while True:
        x, y = randrange(COLS), randrange(ROWS)
        if maze[y][x] == PATH:
            return x, y

def draw_food(food):
    # rect = pygame.Rect(food[0] * TILE_SIZE, food[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    # pygame.draw.rect(screen, GREEN, rect)

    rect = pygame.Rect(food[0] * TILE_SIZE, food[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    screen.blit(food_image, rect)

def bfs(start, goal):
    global Node_count
    global search_time
    start_time = time.time()
    queue = deque([(start, [])])
    visited = set()
    vertex_count = 0  # Thêm biến đếm
    #queued_vertices = set() 
    while queue:
        current, path = queue.popleft()

        if current == goal:
            #print("Nodes:", vertex_count)  # In số đỉnh đã thêm vào queue
            Node_count=vertex_count
            return path

        if current not in visited:
            visited.add(current)
            x, y = current
            neighbors = [(x + dx, y + dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]]
            valid_neighbors = [neighbor for neighbor in neighbors if maze[neighbor[1]][neighbor[0]] != WALL]
            for neighbor in valid_neighbors:
                queue.append((neighbor, path + [neighbor]))
                queued_vertices.add(neighbor)
                vertex_count += 1  # Tăng biến đếm và in ra trước khi tăng giá trị
    end_time = time.time()
    search_time = end_time - start_time
    
    return None

from collections import deque

def dfs(start, goal):
    stack = [(start, [])]
    visited = set()
    vertex_count = 0
    global Node_count
    while stack:
        current, path = stack.pop()

        if current == goal:
            #print("Nodes:", vertex_count)
            Node_count=vertex_count
            return path

        if current not in visited:
            visited.add(current)
            x, y = current
            neighbors = [(x + dx, y + dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]]
            valid_neighbors = [neighbor for neighbor in neighbors if maze[neighbor[1]][neighbor[0]] != WALL]
            for neighbor in valid_neighbors:
                stack.append((neighbor, path + [neighbor]))
                queued_vertices.add(neighbor)
                vertex_count += 1

    return None

def ucs(start, goal):
    queue = PriorityQueue()
    queue.put((0, start, []))  # Add the start node with cost 0
    visited = set()
    vertex_count = 0
    global Node_count
    while not queue.empty():
        cost, current, path = queue.get()
        
        if current == goal:
            #print("Nodes:", vertex_count)
            Node_count=vertex_count
            return path
        
        if current not in visited:
            visited.add(current)
            x, y = current
            neighbors = [(x + dx, y + dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]]
            valid_neighbors = [neighbor for neighbor in neighbors if maze[neighbor[1]][neighbor[0]] != WALL]
            for neighbor in valid_neighbors:
                new_cost = cost + 1  # Increment the cost by 1 for each step
                queue.put((new_cost, neighbor, path + [neighbor]))
                queued_vertices.add(neighbor)
                vertex_count += 1
    
    return None
def move_player_AI(player, path):
    pygame.time.delay(50)
    if path:
        return path[0], path[1:]
    return player, path

def ids(start, goal, max_depth):
    for depth in range(max_depth + 1):
        result = depth_limited_dfs(start, goal, depth)
        if result is not None:
            return result
    return None

def depth_limited_dfs(start, goal, max_depth):
    stack = deque([(start, [])])
    visited = set()
    vertex_count = 0
    global Node_count
    while stack:
        current, path = stack.pop()

        if current == goal:
            #print("Nodes:", vertex_count)
            Node_count=vertex_count
            return path

        if current not in visited and len(path) <= max_depth:
            visited.add(current)
            x, y = current
            neighbors = [(x + dx, y + dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]]
            valid_neighbors = [neighbor for neighbor in neighbors if maze[neighbor[1]][neighbor[0]] != WALL]
            for neighbor in valid_neighbors:
                stack.append((neighbor, path + [neighbor]))
                queued_vertices.add(neighbor)
                vertex_count += 1

    return None

def heuristic(current, goal):
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

def greedy(start, goal):
    queue = PriorityQueue()
    queue.put((heuristic(start, goal), start, []))  # Add the start node with heuristic cost
    visited = set()
    vertex_count = 0
    global Node_count
    while not queue.empty():
        _, current, path = queue.get()

        if current == goal:
            #print("Nodes:", vertex_count)
            Node_count=vertex_count
            return path

        if current not in visited:
            visited.add(current)
            x, y = current
            neighbors = [(x + dx, y + dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]]
            valid_neighbors = [neighbor for neighbor in neighbors if maze[neighbor[1]][neighbor[0]] != WALL]
            for neighbor in valid_neighbors:
                queue.put((heuristic(neighbor, goal), neighbor, path + [neighbor]))
                queued_vertices.add(neighbor)
                vertex_count += 1

    return None

def Astar(start, goal):
    queue = PriorityQueue()
    queue.put((heuristic(start, goal), start, []))  # Add the start node with heuristic cost
    visited = set()
    vertex_count = 0
    global Node_count
    while not queue.empty():
        _, current, path = queue.get()

        if current == goal:
            #print("Nodes:", vertex_count)
            Node_count=vertex_count
            return path

        if current not in visited:
            visited.add(current)
            x, y = current
            neighbors = [(x + dx, y + dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]]
            valid_neighbors = [neighbor for neighbor in neighbors if maze[neighbor[1]][neighbor[0]] != WALL]
            for neighbor in valid_neighbors:
                queue.put((heuristic(neighbor, goal) + len(path), neighbor, path + [neighbor]))
                queued_vertices.add(neighbor)
                vertex_count += 1

    return None
# Tạo mê cung và vị trí ban đầu cho người chơi và thức ăn
maze = generate_maze()
player_pos = (1, 1)
player2_pos=(31,21)
re_player_pos = player_pos
food_pos = generate_food(maze)
re_food_pos = food_pos
bfs_button_rect = pygame.Rect(WIDTH - 190, 10, 80, 50)
dfs_button_rect = pygame.Rect(WIDTH - 95, 10, 80, 50)
ucs_button_rect = pygame.Rect(WIDTH - 190, 70, 80, 50)
id_button_rect = pygame.Rect(WIDTH - 95, 70, 80, 50)
greedy_button_rect = pygame.Rect(WIDTH - 190, 130, 80, 50)
astar_button_rect = pygame.Rect(WIDTH - 95, 130, 80, 50)
PVP_button_rect = pygame.Rect(WIDTH - 190, 190, 80, 50)
AI_button_rect = pygame.Rect(WIDTH - 190, 190, 80, 50)

# Biến lưu trạng thái game
running = True  
key_pressed = None
bfs_path = None
dfs_path = None
ucs_path = None
ids_path = None
greedy_path = None
astar_path = None
PVP_check=False
score1=0
score2=0
# Vòng lặp chính
while running:
    
    if PVP_check==False:
        food_found = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                key_pressed = event.key
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if bfs_button_rect.collidepoint(event.pos):
                    bfs_path = bfs(player_pos, food_pos)
                    print(search_time)
                elif dfs_button_rect.collidepoint(event.pos):
                    dfs_path = dfs(player_pos, food_pos)
                elif ucs_button_rect.collidepoint(event.pos):
                    ucs_path = ucs(player_pos, food_pos)
                elif id_button_rect.collidepoint(event.pos):
                    ids_path = ids(player_pos, food_pos, 1000)
                elif greedy_button_rect.collidepoint(event.pos):
                    greedy_path = greedy(player_pos, food_pos)
                elif astar_button_rect.collidepoint(event.pos):  # Thêm nút A*
                    astar_path = Astar(player_pos, food_pos)
                elif PVP_button_rect.collidepoint(event.pos):
                    PVP_check=True
        
        # Xử lý sự kiện di chuyển chỉ khi một phím được nhấn
        if key_pressed is not None:
            direction = None
            if key_pressed == pygame.K_RIGHT:
                direction = (1, 0)
            elif key_pressed == pygame.K_LEFT:
                direction = (-1, 0)
            elif key_pressed == pygame.K_DOWN:
                direction = (0, 1)
            elif key_pressed == pygame.K_UP:
                direction = (0, -1)

            if direction is not None:
                player_pos = move_player(player_pos, direction)

                # Kiểm tra va chạm với thức ăn
                if check_food(player_pos, food_pos):
                    food_pos = generate_food(maze)

                key_pressed = None  # Đặt lại biến key_pressed để chờ sự kiện mới
        elif bfs_path:  # Nếu có đường đi từ BFS
            player_pos, bfs_path = move_player_AI(player_pos, bfs_path)
            # Kiểm tra va chạm với thức ăn
            if check_food(player_pos, food_pos) and not food_found:
                queued_vertices=set()
                food_found = True
                #food_pos = generate_food(maze)
                player_pos = re_player_pos
                food_pos = re_food_pos
                
        elif dfs_path:  # Nếu có đường đi từ BFS
            player_pos, dfs_path = move_player_AI(player_pos, dfs_path)
            # Kiểm tra va chạm với thức ăn
            if check_food(player_pos, food_pos)and not food_found:
                queued_vertices=set()
                food_found = True
                #food_pos = generate_food(maze)
                player_pos = re_player_pos
                food_pos = re_food_pos

        elif ucs_path:  # Nếu có đường đi từ BFS
            player_pos, ucs_path = move_player_AI(player_pos, ucs_path)
            # Kiểm tra va chạm với thức ăn
            if check_food(player_pos, food_pos)and not food_found:
                queued_vertices=set()
                food_found = True
                #food_pos = generate_food(maze)
                player_pos = re_player_pos
                food_pos = re_food_pos

        elif ids_path:  # Nếu có đường đi từ BFS
            player_pos, ids_path = move_player_AI(player_pos, ids_path)
            # Kiểm tra va chạm với thức ăn
            if check_food(player_pos, food_pos)and not food_found:
                queued_vertices=set()
                food_found = True
            # food_pos = generate_food(maze)
                player_pos = re_player_pos
                food_pos = re_food_pos
        
        elif greedy_path:  # Nếu có đường đi từ greedy
            player_pos, greedy_path = move_player_AI(player_pos, greedy_path)
            # Kiểm tra va chạm với thức ăn
            if check_food(player_pos, food_pos)and not food_found:
                queued_vertices=set()
                food_found = True
            # food_pos = generate_food(maze)
                player_pos = re_player_pos
                food_pos = re_food_pos

        elif astar_path:  # Nếu có đường đi từ A*
            player_pos, astar_path = move_player_AI(player_pos, astar_path)
            # Kiểm tra va chạm với thức ăn
            if check_food(player_pos, food_pos) and not food_found:
                queued_vertices=set()
                food_found = True
                # food_pos = generate_food(maze)
                player_pos = re_player_pos
                food_pos = re_food_pos
        
        # Xóa màn hình
        screen.fill(STEEL_BLUE)

        # Vẽ mê cung
        draw_maze(maze)

        # Vẽ người chơi
        draw_player(player_pos)

        # Vẽ thức ăn
        draw_food(food_pos)

        pygame.draw.rect(screen, CHIFFON, bfs_button_rect)  # Đỏ, nằm bên phải và ngoài mê cung
        font = pygame.font.Font(None, 36)
        text = font.render("BFS", True, BLACK)
        text_rect = text.get_rect(center=(bfs_button_rect.x + bfs_button_rect.width // 2, bfs_button_rect.y + bfs_button_rect.height // 2))
        screen.blit(text, text_rect)

        pygame.draw.rect(screen, CHIFFON, dfs_button_rect)  # Đỏ, nằm bên phải và ngoài mê cung
        font = pygame.font.Font(None, 36)
        text = font.render("DFS", True, BLACK)
        text_rect = text.get_rect(center=(dfs_button_rect.x + dfs_button_rect.width // 2, dfs_button_rect.y + dfs_button_rect.height // 2))
        screen.blit(text, text_rect)

        pygame.draw.rect(screen, CHIFFON, ucs_button_rect)  # Đỏ, nằm bên phải và ngoài mê cung
        font = pygame.font.Font(None, 36)
        text = font.render("UCS", True, BLACK)
        text_rect = text.get_rect(center=(ucs_button_rect.x + ucs_button_rect.width // 2, ucs_button_rect.y + ucs_button_rect.height // 2))
        screen.blit(text, text_rect)

        pygame.draw.rect(screen, CHIFFON, id_button_rect)  # Đỏ, nằm bên phải và ngoài mê cung
        font = pygame.font.Font(None, 36)
        text = font.render("ID", True, BLACK)
        text_rect = text.get_rect(center=(id_button_rect.x + id_button_rect.width // 2, id_button_rect.y + id_button_rect.height // 2))
        screen.blit(text, text_rect)

        pygame.draw.rect(screen, CHIFFON, greedy_button_rect)
        font = pygame.font.Font(None, 36)
        text = font.render("Grd", True, BLACK)
        text_rect = text.get_rect(center=(greedy_button_rect.x + greedy_button_rect.width // 2, greedy_button_rect.y + greedy_button_rect.height // 2))
        screen.blit(text, text_rect)

        
        pygame.draw.rect(screen, CHIFFON, astar_button_rect)
        font = pygame.font.Font(None, 36)
        text = font.render("A*", True, BLACK)
        text_rect = text.get_rect(center=(astar_button_rect.x + astar_button_rect.width // 2, astar_button_rect.y + astar_button_rect.height // 2))
        screen.blit(text, text_rect)

        pygame.draw.rect(screen, CHIFFON, AI_button_rect)
        font = pygame.font.Font(None, 36)
        text = font.render("PvP", True, BLACK)
        text_rect = text.get_rect(center=(AI_button_rect.x + AI_button_rect.width // 2, AI_button_rect.y + AI_button_rect.height // 2))
        screen.blit(text, text_rect)
        
        text1 = font.render(f"Nodes: {Node_count}", True, (0, 0, 0)) 
        text2 = font.render(f"Time: {search_time:.1f} ", True, (0, 0, 0))
        text_rect1 = text1.get_rect()
        text_rect2 = text2.get_rect()
        text_rect1.bottomright = (WIDTH - 10, 500)
        text_rect2.bottomright = (WIDTH - 10, 540)
        screen.blit(text1, text_rect1)
        screen.blit(text2, text_rect2)
        # Cập nhật màn hình
        pygame.display.flip()

        # Đặt tốc độ khung hình
        pygame.time.Clock().tick(120)
    else:
        food_found = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                key_pressed = event.key
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # if bfs_button_rect.collidepoint(event.pos):
                #     bfs_path = bfs(player_pos, food_pos)
                # elif dfs_button_rect.collidepoint(event.pos):
                #     dfs_path = dfs(player_pos, food_pos)
                # elif ucs_button_rect.collidepoint(event.pos):
                #     ucs_path = ucs(player_pos, food_pos)
                # elif id_button_rect.collidepoint(event.pos):
                #     ids_path = ids(player_pos, food_pos, 1000)
                # elif greedy_button_rect.collidepoint(event.pos):
                #     greedy_path = greedy(player_pos, food_pos)
                # elif astar_button_rect.collidepoint(event.pos):  # Thêm nút A*
                #     astar_path = Astar(player_pos, food_pos)
                if AI_button_rect.collidepoint(event.pos):
                    PVP_check=False
        # Xử lý sự kiện di chuyển chỉ khi một phím được nhấn
        if key_pressed is not None:
            direction = None
            direction2=None
            if key_pressed == pygame.K_RIGHT:
                direction = (1, 0)
            elif key_pressed == pygame.K_LEFT:
                direction = (-1, 0)
            elif key_pressed == pygame.K_DOWN:
                direction = (0, 1)
            elif key_pressed == pygame.K_UP:
                direction = (0, -1)

            if key_pressed == ord('d'):
                direction2 = (1, 0)
            elif key_pressed == ord('a'):
                direction2 = (-1, 0)
            elif key_pressed == ord('s'):
                direction2 = (0, 1)
            elif key_pressed == ord('w'):
                direction2 = (0, -1)

            if direction is not None:
                player_pos = move_player(player_pos, direction)
                
            if direction2 is not None:
                player2_pos = move_player(player2_pos, direction2)
                
                # Kiểm tra va chạm với thức ăn
            if check_food(player_pos, food_pos):
                score1+=1
                food_pos = generate_food(maze)
            if check_food(player2_pos, food_pos):
                score2+=1
                food_pos = generate_food(maze)
            key_pressed = None  # Đặt lại biến key_pressed để chờ sự kiện mới
        elif bfs_path:  # Nếu có đường đi từ BFS
            player_pos, bfs_path = move_player_AI(player_pos, bfs_path)
            # Kiểm tra va chạm với thức ăn
            if check_food(player_pos, food_pos) and not food_found:
                queued_vertices=set()
                food_found = True
                #food_pos = generate_food(maze)
                player_pos = re_player_pos
                food_pos = re_food_pos
                
        elif dfs_path:  # Nếu có đường đi từ BFS
            player_pos, dfs_path = move_player_AI(player_pos, dfs_path)
            # Kiểm tra va chạm với thức ăn
            if check_food(player_pos, food_pos)and not food_found:
                queued_vertices=set()
                food_found = True
                #food_pos = generate_food(maze)
                player_pos = re_player_pos
                food_pos = re_food_pos

        elif ucs_path:  # Nếu có đường đi từ BFS
            player_pos, ucs_path = move_player_AI(player_pos, ucs_path)
            # Kiểm tra va chạm với thức ăn
            if check_food(player_pos, food_pos)and not food_found:
                queued_vertices=set()
                food_found = True
                #food_pos = generate_food(maze)
                player_pos = re_player_pos
                food_pos = re_food_pos

        elif ids_path:  # Nếu có đường đi từ BFS
            player_pos, ids_path = move_player_AI(player_pos, ids_path)
            # Kiểm tra va chạm với thức ăn
            if check_food(player_pos, food_pos)and not food_found:
                queued_vertices=set()
                food_found = True
            # food_pos = generate_food(maze)
                player_pos = re_player_pos
                food_pos = re_food_pos
        
        elif greedy_path:  # Nếu có đường đi từ greedy
            player_pos, greedy_path = move_player_AI(player_pos, greedy_path)
            # Kiểm tra va chạm với thức ăn
            if check_food(player_pos, food_pos)and not food_found:
                queued_vertices=set()
                food_found = True
            # food_pos = generate_food(maze)
                player_pos = re_player_pos
                food_pos = re_food_pos

        elif astar_path:  # Nếu có đường đi từ A*
            player_pos, astar_path = move_player_AI(player_pos, astar_path)
            # Kiểm tra va chạm với thức ăn
            if check_food(player_pos, food_pos) and not food_found:
                queued_vertices=set()
                food_found = True
                # food_pos = generate_food(maze)
                player_pos = re_player_pos
                food_pos = re_food_pos
        
        # Xóa màn hình
        screen.fill(STEEL_BLUE)

        # Vẽ mê cung
        draw_maze(maze)

        # Vẽ người chơi
        draw_player(player_pos)
        draw_player2(player2_pos)
        # Vẽ thức ăn
        draw_food(food_pos)

        pygame.draw.rect(screen, CHIFFON, bfs_button_rect)  # Đỏ, nằm bên phải và ngoài mê cung
        font = pygame.font.Font(None, 36)
        text = font.render("BFS", True, BLACK)
        text_rect = text.get_rect(center=(bfs_button_rect.x + bfs_button_rect.width // 2, bfs_button_rect.y + bfs_button_rect.height // 2))
        screen.blit(text, text_rect)

        pygame.draw.rect(screen, CHIFFON, dfs_button_rect)  # Đỏ, nằm bên phải và ngoài mê cung
        font = pygame.font.Font(None, 36)
        text = font.render("DFS", True, BLACK)
        text_rect = text.get_rect(center=(dfs_button_rect.x + dfs_button_rect.width // 2, dfs_button_rect.y + dfs_button_rect.height // 2))
        screen.blit(text, text_rect)

        pygame.draw.rect(screen, CHIFFON, ucs_button_rect)  # Đỏ, nằm bên phải và ngoài mê cung
        font = pygame.font.Font(None, 36)
        text = font.render("UCS", True, BLACK)
        text_rect = text.get_rect(center=(ucs_button_rect.x + ucs_button_rect.width // 2, ucs_button_rect.y + ucs_button_rect.height // 2))
        screen.blit(text, text_rect)

        pygame.draw.rect(screen, CHIFFON, id_button_rect)  # Đỏ, nằm bên phải và ngoài mê cung
        font = pygame.font.Font(None, 36)
        text = font.render("ID", True, BLACK)
        text_rect = text.get_rect(center=(id_button_rect.x + id_button_rect.width // 2, id_button_rect.y + id_button_rect.height // 2))
        screen.blit(text, text_rect)

        pygame.draw.rect(screen, CHIFFON, greedy_button_rect)
        font = pygame.font.Font(None, 36)
        text = font.render("Grd", True, BLACK)
        text_rect = text.get_rect(center=(greedy_button_rect.x + greedy_button_rect.width // 2, greedy_button_rect.y + greedy_button_rect.height // 2))
        screen.blit(text, text_rect)

        
        pygame.draw.rect(screen, CHIFFON, astar_button_rect)
        font = pygame.font.Font(None, 36)
        text = font.render("A*", True, BLACK)
        text_rect = text.get_rect(center=(astar_button_rect.x + astar_button_rect.width // 2, astar_button_rect.y + astar_button_rect.height // 2))
        screen.blit(text, text_rect)

        pygame.draw.rect(screen, CHIFFON, PVP_button_rect)
        font = pygame.font.Font(None, 36)
        text = font.render("1P", True, BLACK)
        text_rect = text.get_rect(center=(PVP_button_rect.x + PVP_button_rect.width // 2, PVP_button_rect.y + PVP_button_rect.height // 2))
        screen.blit(text, text_rect)

        text1 = font.render(f"Score 1: {score1}", True, (0, 0, 0)) 
        text2 = font.render(f"Score 2: {score2}", True, (0, 0, 0)) 
        text_rect1 = text1.get_rect()
        text_rect2 = text2.get_rect()
        text_rect1.bottomright = (WIDTH - 75, 300)
        text_rect2.bottomright = (WIDTH - 75, 350)
        screen.blit(text1, text_rect1)
        screen.blit(text2, text_rect2)
        
        # screen.blit("Score Player 1: "+score1_text, (WIDTH - 190, 300))
        # screen.blit("Score Player 2: "+score2_text, (WIDTH - 190, 390))
        # Cập nhật màn hình
        pygame.display.flip()

        # Đặt tốc độ khung hình
        pygame.time.Clock().tick(120)
# Kết thúc Pygame
pygame.quit()
sys.exit()