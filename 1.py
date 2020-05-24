import pygame
import copy
import random

FPS = 20  # кадров в секунду для обновления экрана
# размеры
win_width = 1300  # ширина окна программы в пикселях
win_height = 800  # высота

# поле
board_column = 10  # столбцов
board_line = 10  # строк
size_rect = 70  # ширина и высота

# Количество места по бокам доски до края окна
x_otstup = int((win_width - size_rect * board_column) / 2)
y_otstup = int((win_height - size_rect * board_line) / 2)

# картинки
bg = pygame.image.load('bg.jpg')



# константы для значений направления
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
row_above_board = 'row above board'  # произвольное нецелое значение

def main():
    global win, board_rect, img, this_clock
    pygame.init()
    this_clock = pygame.time.Clock()
    win = pygame.display.set_mode((win_width, win_height))  # cоздание окна
    pygame.display.set_caption('Три в ряд')  # название окна

    # загрузка фотографий
    img = []
    for i in range(1, 7):
        gem_image = pygame.image.load('%s.png' % i)
        if gem_image.get_size() != (size_rect, size_rect):
            # плавно масштабировать поверхность до произвольного размера
            gem_image = pygame.transform.smoothscale(gem_image, (size_rect, size_rect))
        img.append(gem_image)

    board_rect = []
    for x in range(board_column):  # рисуем квадраты
        board_rect.append([])
        for y in range(board_line):
            r = pygame.Rect((x_otstup + (x * size_rect),  # rect(x,y, ширина,высота)
                             y_otstup + (y * size_rect),
                             size_rect,
                             size_rect))
            board_rect[x].append(r)  # хранит коордиаты квадратов

    while True:
        run()


def run():
    win.blit(bg, (0, 0))  # фон
    game_board = get_blank_board()  # получаем структуру поля, список в списке, с указателем -1
    score = 0
    fill_board_and_animate(game_board, [], score)
    #draw_board(board)  # рисуем камни

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                pygame.quit()


def fill_board_and_animate(board, points, score):
    drop_slots = get_slots(board)  # указываем расположение наших камней
    while drop_slots != [[]] * board_column:
        # делать анимацию выпадения, пока есть еще драгоценные камни
        moving_gems = get_dropping_gems(board)
        for x in range(len(drop_slots)):
            if len(drop_slots[x]) != 0:
                # заставить самый низкий драгоценный камень в каждом слоте начать движение в направлении вниз
                moving_gems.append({'imageNum': drop_slots[x][0], 'x': x, 'y': row_above_board, 'direction': DOWN})
            #print(moving_gems)

        board_copy = get_board_copy_minus_gems(board, moving_gems)  # делает пустыми все строки, кроме первой
        print('---', board_copy)
        animate_moving_gems(board_copy, moving_gems, points, score)
        move_gems(board, moving_gems)

        # Make the next row of gems from the drop slots
        # the lowest by deleting the previous lowest gems.
        for x in range(len(drop_slots)):
            if len(drop_slots[x]) == 0:
                continue
            board[x][0] = drop_slots[x][0]
            del drop_slots[x][0]

# 1
def get_blank_board():
    # Создать и вернуть пустую структуру данных доски.
    board = []
    for x in range(board_column):
        board.append([-1] * board_line)
    return board

# 2
def get_slots(board):  # указываем расположение наших 6-ти камней
    board_copy = copy.deepcopy(board)
    drop_slots = []
    for i in range(board_column):
        drop_slots.append([])
    print(drop_slots)

    # подсчитать количество пустых мест в каждом столбце на доске
    for x in range(board_column):
        for y in range(board_line - 1, -1, -1):
            if board_copy[x][y] == -1:  # если в структуре -1, значит этот квадрат не заполнен(нет камня)
                index_img = list(range(len(img)))  # [0,1,2,3,4,5]
                for offsetX, offsetY in ((0, -1), (1, 0), (0, 1), (-1, 0)):  # исключить два камня рядом
                    gem = get_gem_at(board_copy, x + offsetX, y + offsetY)  # возвращает указаный камень
                    if gem is not None and gem in index_img:
                        index_img.remove(gem)

                new_gem = random.choice(index_img)
                board_copy[x][y] = new_gem  # нужен для сверки соседей
                drop_slots[x].append(new_gem)  # новая структура с камнями, где не совпадают соседи

    return drop_slots

# 3
def get_gem_at(board, x, y):  # возвращает указаный камень
    if x < 0 or y < 0 or x >= board_column or y >= board_line:
        return None
    else:
        return board[x][y]

# 4
def draw_board(board):
    for x in range(board_column):
        for y in range(board_line):
            pygame.draw.rect(win, (255, 255, 255), board_rect[x][y], 1)  # board_rect - хранит коордиаты квадратов
            gem_to_draw = board[x][y]
            if gem_to_draw != -1:
                win.blit(img[gem_to_draw], board_rect[x][y])
    # pygame.display.update()

# 5
def get_dropping_gems(board):
    # Найти все драгоценные камни, которые имеют пустое пространство под ними
    board_copy = copy.deepcopy(board)
    dropping_gems = []
    for x in range(board_column):
        for y in range(board_line - 2, -1, -1):
            if board_copy[x][y + 1] == -1 and board_copy[x][y] != -1:  # если клетка снизу пуста, а на один выше нет
                # Это пространство падает, если не пустое, но пространство под ним
                dropping_gems.append({'imageNum': board_copy[x][y], 'x': x, 'y': y, 'direction': DOWN})
                board_copy[x][y] = -1
    return dropping_gems

# 6
def get_board_copy_minus_gems(board, moving_gems):
    board_copy = copy.deepcopy(board)
    print(board_copy)
    # Удалите некоторые драгоценные камни из этой копии структуры данных
    for gem in moving_gems:
        if gem['y'] != row_above_board:  # если строка не самая первая(сверху)
            board_copy[gem['x']][gem['y']] = -1
    return board_copy

# 7
def animate_moving_gems(board, gems, pointsText, score):
    # pointsText - это словарь с ключами 'x', 'y' и 'points'
    progress = 0  # прогресс в 0 означает начало, 100 означает завершение.
    while progress < 100:
        win.blit(bg, (0, 0))
        draw_board(board)
        for gem in gems:  # Нарисуй каждый драгоценный камень.
            draw_moving_gem(gem, progress)
        draw_score(score)
        for pointText in pointsText:
            this_font = pygame.font.Font('freesansbold.ttf', 36)  # шрифт
            points_surf = this_font.render(str(pointText['points']), 1, (200, 200, 200))
            points_rect = points_surf.get_rect()
            points_rect.center = (pointText['x'], pointText['y'])
            win.blit(points_surf, points_rect)

        pygame.display.update()
        this_clock.tick(FPS)
        progress += 25  # # От 1 до 100, большее число означает более быструю анимацию

# 8
def draw_moving_gem(gem, progress):
    # Нарисуйте драгоценный камень, скользящий в направлении, указанном его клавишей направления
    movex = 0
    movey = 0
    progress *= 0.01

    if gem['direction'] == UP:
        movey = -int(progress * size_rect)
    elif gem['direction'] == DOWN:
        movey = int(progress * size_rect)
    elif gem['direction'] == RIGHT:
        movex = int(progress * size_rect)
    elif gem['direction'] == LEFT:
        movex = -int(progress * size_rect)

    basex = gem['x']
    basey = gem['y']
    if basey == row_above_board:
        basey = -1

    pixelx = x_otstup + (basex * size_rect)
    pixely = y_otstup + (basey * size_rect)
    r = pygame.Rect((pixelx + movex, pixely + movey, size_rect, size_rect))
    win.blit(img[gem['imageNum']], r)

# 9
def draw_score(score):
    this_font = pygame.font.Font('freesansbold.ttf', 36)  # шрифт
    score_img = this_font.render(str(score), 1, (200, 200, 200))
    score_rect = score_img.get_rect()
    score_rect.bottomleft = (10, win_height - 6)
    win.blit(score_img, score_rect)

# 10
def move_gems(board, moving_gems):
    # movingGems is a list of dicts with keys x, y, direction, imageNum
    for gem in moving_gems:
        if gem['y'] != row_above_board:
            board[gem['x']][gem['y']] = -1
            movex = 0
            movey = 0
            if gem['direction'] == LEFT:
                movex = -1
            elif gem['direction'] == RIGHT:
                movex = 1
            elif gem['direction'] == DOWN:
                movey = 1
            elif gem['direction'] == UP:
                movey = -1
            board[gem['x'] + movex][gem['y'] + movey] = gem['imageNum']
        else:
            # gem is located above the board (where new gems come from)
            board[gem['x']][0] = gem['imageNum'] # move to top row


if __name__ == '__main__':
    main()
