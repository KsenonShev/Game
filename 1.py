import pygame

# размеры
win_width = 1600  # ширина окна программы в пикселях
win_height = 900  # высота

# поле
board_column = 10  # столбцов
board_line = 10  # строк
size_rect = 64  # площадб квадратов на поле

# Количество места по бокам доски до края окна
x_otstup = int((win_width - size_rect * board_column) / 2)
y_otstup = int((win_height - size_rect * board_line) / 2)

# картинки
bg = pygame.image.load('bg.jpg')

clock = pygame.time.Clock()

def main():
    global win, board_rect
    pygame.init()
    win = pygame.display.set_mode((0, 0), pygame.RESIZABLE)  # cоздание окна
    pygame.display.set_caption('Три в ряд')  # название окна
    win.blit(bg, (0, 0))

    board_rect = []

    for x in range(board_column):
        board_rect.append([])
        for y in range(board_line):
            r = pygame.Rect((x_otstup + (x * size_rect),
                             y_otstup + (y * size_rect),
                             size_rect,
                             size_rect))
            board_rect[x].append(r)


def drawBoard():
    for x in range(board_column):
        for y in range(board_line):
            pygame.draw.rect(win, (0, 0, 255), board_rect[x][y], 1)
    pygame.display.update()


run = True
while run:
    main()
    drawBoard()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


pygame.quit()
