import pygame
import copy
import random

# размеры
win_width = 1600  # ширина окна программы в пикселях
win_height = 900  # высота

# поле
board_column = 10  # столбцов
board_line = 10  # строк
size_rect = 70  # ширина и высота

# Количество места по бокам доски до края окна
x_otstup = int((win_width - size_rect * board_column) / 2)
y_otstup = int((win_height - size_rect * board_line) / 2)

# картинки
bg = pygame.image.load('bg.jpg')

clock = pygame.time.Clock()


def main():
    global win, board_rect, img
    pygame.init()
    win = pygame.display.set_mode((0, 0), pygame.RESIZABLE)  # cоздание окна
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
    for x in range(board_column):
        board_rect.append([])
        for y in range(board_line):
            r = pygame.Rect((x_otstup + (x * size_rect),  # rect(x,y, ширина,высота)
                             y_otstup + (y * size_rect),
                             size_rect,
                             size_rect))
            board_rect[x].append(r)

    while True:
        run()


def run():
    win.blit(bg, (0, 0))  # фон
    game_board = get_blank_board()  # получаем структуру поля, список в списке, с указателем -1
    board = get_slots(game_board)  # указываем расположение наших 6-ти камней
    draw_board(board)  # рисуем камни

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                pygame.quit()


def get_blank_board():
    # Создать и вернуть пустую структуру данных доски.
    board = []
    for x in range(board_column):
        board.append([-1] * board_line)
    return board


def get_slots(board):  # указываем расположение наших 6-ти камней
    board_copy = copy.deepcopy(board)

    drop_slots = []
    for i in range(board_column):
        drop_slots.append([])

    # подсчитать количество пустых мест в каждом столбце на доске
    for x in range(board_column):
        for y in range(board_line - 1, -1, -1):
            if board_copy[x][y] == -1:
                index_img = list(range(len(img)))  # [0,1,2,3,4,5]
                for offsetX, offsetY in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                    gem = get_gem_at(board_copy, x + offsetX, y + offsetY)  # возвращает указаный камень
                    if gem is not None and gem in index_img:
                        index_img.remove(gem)

                new_gem = random.choice(index_img)
                board_copy[x][y] = new_gem
                drop_slots[x].append(new_gem)
    print(drop_slots)
    return drop_slots


def get_gem_at(board, x, y):  # возвращает указаный камень
    if x < 0 or y < 0 or x >= board_column or y >= board_line:
        return None
    else:
        return board[x][y]


def draw_board(board):
    print(board)
    for x in range(board_column):
        for y in range(board_line):
            pygame.draw.rect(win, (255, 255, 255), board_rect[x][y], 1)
            gem_to_draw = board[x][y]
            if gem_to_draw != -1:
                win.blit(img[gem_to_draw], board_rect[x][y])
    # pygame.display.update()


if __name__ == '__main__':
    main()
