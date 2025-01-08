import pygame

# инициализируем библиотеку Pygame
pygame.init()

# определяем размеры окна
window_size = (300, 300)

# задаем название окна
pygame.display.set_caption("PathAi")

# создаем окно
screen = pygame.display.set_mode(window_size)

# задаем цвет фона
background_color = (0, 0, 0)  # черный

# заполняем фон заданным цветом
screen.fill(background_color)

# обновляем экран для отображения изменений
pygame.display.flip()

# показываем окно, пока пользователь не нажмет кнопку "Закрыть"
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
