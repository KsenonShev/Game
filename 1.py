import pygame, random

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

    # загрузка фотографий(глянуть расширенный вариант)
    img = []
    for i in range(1, 7):
        gemImage = pygame.image.load('%s.png' % i)
        if gemImage.get_size() != (size_rect, size_rect):
            gemImage = pygame.transform.smoothscale(gemImage, (size_rect, size_rect))  # плавно масштабировать поверхность до произвольного размера
        img.append(gemImage)
        print(img)

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
    win.blit(bg, (0, 0))
    gameBoard = getBlankBoard()
    drawBoard(gameBoard)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                pygame.quit()


def getBlankBoard():
    # Создать и вернуть пустую структуру данных доски.
    board = []
    for x in range(board_column):
        board.append([-1] * board_line)
    print(board)
    return board


def drawBoard(board):
    for x in range(board_column):
        for y in range(board_line):
            pygame.draw.rect(win, (255, 255, 255), board_rect[x][y], 1)
            gemToDraw = board[x][y]
            if gemToDraw == -1:
                i = random.randrange(0, 6)
                win.blit(img[i], board_rect[x][y])
    # pygame.display.update()


if __name__ == '__main__':
    main()
