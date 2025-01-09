import pygame as pg
import random
import numpy as np
import gym
from gym import spaces
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
import os

# Инициализируем библиотеку pg
pg.init()

# Определяем размеры окна
window_size = (1280, 720)

# Задаем название окна
pg.display.set_caption("PathAi")

# Создаем окно
screen = pg.display.set_mode(window_size)

# Задаем цвет фона
background_color = (0, 0, 0)  # черный

# Задаем цвет игрока
player_color = (255, 255, 255)  # белый

# Задаем цвет зеленого квадрата
green_square_color = (0, 100, 0)  # темно-зеленый

# Задаем цвет красного квадрата
red_square_color = (100, 0, 0)  # темно-красный

# Задаем размер игрока и квадратов
player_size = (50, 50)
square_size = (50, 50)

# Задаем начальную позицию игрока
player_pos = [window_size[0] // 2, window_size[1] // 2]

# Задаем скорость игрока
player_speed = 5

# Задаем начальное количество очков
score = 10

# Инициализируем шрифт
font = pg.font.Font(None, 36)

# Инициализируем таймер
clock = pg.time.Clock()
last_update_time = pg.time.get_ticks()

# Начальная позиция зеленого квадрата
green_square_pos = [0, 0]

# Начальные позиции красных квадратов
red_squares_pos = []

# Функция для движения игрока
def move_player(direction):
    if direction == 'up' and player_pos[1] - player_speed >= 0:
        player_pos[1] -= player_speed
    elif direction == 'down' and player_pos[1] + player_speed + player_size[1] <= window_size[1]:
        player_pos[1] += player_speed
    elif direction == 'left' and player_pos[0] - player_speed >= 0:
        player_pos[0] -= player_speed
    elif direction == 'right' and player_pos[0] + player_speed + player_size[0] <= window_size[0]:
        player_pos[0] += player_speed

# Функция для рандомного спавна зеленого квадрата
def spawn_green_square():
    green_square_pos[0] = random.randint(0, window_size[0] - square_size[0])
    green_square_pos[1] = random.randint(0, window_size[1] - square_size[1])

# Функция для рандомного спавна красных квадратов
def spawn_red_squares():
    red_squares_pos.clear()
    num_red_squares = random.randint(4, 10)
    for _ in range(num_red_squares):
        while True:
            pos = [random.randint(0, window_size[0] - square_size[0]), random.randint(0, window_size[1] - square_size[1])]
            red_square_rect = pg.Rect(pos[0], pos[1], square_size[0], square_size[1])
            if not (red_square_rect.colliderect(pg.Rect(player_pos[0], player_pos[1], player_size[0], player_size[1])) or
                    red_square_rect.colliderect(pg.Rect(green_square_pos[0], green_square_pos[1], square_size[0], square_size[1])) or
                    any(red_square_rect.colliderect(pg.Rect(other_pos[0], other_pos[1], square_size[0], square_size[1])) for other_pos in red_squares_pos)):
                red_squares_pos.append(pos)
                break

# Функция для получения позиции игрока
def get_player_position():
    return player_pos

# Функция для получения позиции зеленого квадрата
def get_green_square_position():
    return green_square_pos

# Функция для получения позиций всех красных квадратов
def get_red_squares_positions():
    return red_squares_pos

# Создание среды для игры
class GameEnv(gym.Env):
    def __init__(self):
        super(GameEnv, self).__init__()
        self.observation_space = spaces.Box(low=0, high=max(window_size), shape=(4,), dtype=np.float32)
        self.action_space = spaces.Discrete(4)  # 4 действия: вверх, вниз, влево, вправо
        self.reset()

    def reset(self):
        global player_pos, green_square_pos, red_squares_pos, score
        player_pos = [window_size[0] // 2, window_size[1] // 2]
        spawn_green_square()
        spawn_red_squares()
        score = 10
        return self._next_observation()

    def _next_observation(self):
        player_rect = pg.Rect(player_pos[0], player_pos[1], player_size[0], player_size[1])
        green_square_rect = pg.Rect(green_square_pos[0], green_square_pos[1], square_size[0], square_size[1])
        red_squares_rects = [pg.Rect(pos[0], pos[1], square_size[0], square_size[1]) for pos in red_squares_pos]

        obs = [player_pos[0], player_pos[1], green_square_pos[0], green_square_pos[1]]
        return np.array(obs)

    def step(self, action):
        global score
        directions = ['up', 'down', 'left', 'right']
        move_player(directions[action])

        player_rect = pg.Rect(player_pos[0], player_pos[1], player_size[0], player_size[1])
        green_square_rect = pg.Rect(green_square_pos[0], green_square_pos[1], square_size[0], square_size[1])
        red_squares_rects = [pg.Rect(pos[0], pos[1], square_size[0], square_size[1]) for pos in red_squares_pos]

        reward = -1  # Штраф за каждый ход

        if player_rect.colliderect(green_square_rect):
            reward += 10
            score += 10
            spawn_green_square()
            spawn_red_squares()

        for red_square_rect in red_squares_rects:
            if player_rect.colliderect(red_square_rect):
                reward -= 50
                score -= 50
                red_squares_pos.remove([red_square_rect.x, red_square_rect.y])
                break

        done = score <= 0
        obs = self._next_observation()
        return obs, reward, done, {}

    def render(self, mode='human'):
        screen.fill(background_color)
        pg.draw.rect(screen, player_color, (*player_pos, *player_size))
        pg.draw.rect(screen, green_square_color, (*green_square_pos, *square_size))
        for red_square_pos in red_squares_pos:
            pg.draw.rect(screen, red_square_color, (*red_square_pos, *square_size))
        score_text = font.render(f"Score: {score}", True, player_color)
        screen.blit(score_text, (10, 10))
        pg.display.flip()

# Проверка среды
env = GameEnv()
check_env(env, warn=True)

# Функция для запроса пользователя
def ask_user():
    print("Выберите действие:")
    print("1. Обучить модель")
    print("2. Использовать обученную модель")
    choice = input("Введите номер действия: ")
    return choice

# Основная функция
def main():
    choice = ask_user()

    if choice == '1':
        # Создание модели
        model = PPO('MlpPolicy', env, verbose=1)

        # Обучение модели
        model.learn(total_timesteps=10000)

        # Сохранение модели
        model.save("ppo_game")
        print("Модель обучена и сохранена.")
    elif choice == '2':
        if os.path.exists("ppo_game.zip"):
            # Загрузка модели
            model = PPO.load("ppo_game")

            # Основной игровой цикл
            running = True
            obs = env.reset()
            while running:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        running = False

                action, _states = model.predict(obs)
                obs, rewards, done, info = env.step(action)
                env.render()

                if done:
                    obs = env.reset()

                clock.tick(60)
        else:
            print("Обученная модель не найдена. Пожалуйста, сначала обучите модель.")
    else:
        print("Неверный выбор. Пожалуйста, запустите программу снова.")

    # Завершаем работу pg
    pg.quit()

if __name__ == "__main__":
    main()
