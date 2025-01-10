import gym
from gym import spaces
import numpy as np
import random
import pygame as pg

class PathAiEnv(gym.Env):
    def __init__(self):
        super(PathAiEnv, self).__init__()

        # Определяем пространство действий
        self.action_space = spaces.Discrete(4)  # 4 действия: вверх, вниз, влево, вправо

        # Определяем пространство состояний
        self.observation_space = spaces.Box(low=0, high=1, shape=(4,), dtype=np.float32)

        # Инициализируем параметры среды
        self.window_size = (1280, 720)
        self.player_size = (50, 50)
        self.square_size = (50, 50)
        self.player_speed = 5
        self.score = 10
        self.player_pos = [self.window_size[0] // 2, self.window_size[1] // 2]
        self.green_square_pos = [0, 0]
        self.spawn_green_square()

        # Инициализируем Pygame
        pg.init()
        self.screen = pg.display.set_mode(self.window_size)
        pg.display.set_caption("PathAi")
        self.clock = pg.time.Clock()
        self.font = pg.font.Font(None, 36)

        # Флаг для управления рендерингом
        self.render_enabled = True

    def spawn_green_square(self):
        self.green_square_pos[0] = random.randint(0, self.window_size[0] - self.square_size[0])
        self.green_square_pos[1] = random.randint(0, self.window_size[1] - self.square_size[1])

    def step(self, action):
        # Выполняем действие
        if action == 0 and self.player_pos[1] - self.player_speed >= 0:
            self.player_pos[1] -= self.player_speed
        elif action == 1 and self.player_pos[1] + self.player_speed + self.player_size[1] <= self.window_size[1]:
            self.player_pos[1] += self.player_speed
        elif action == 2 and self.player_pos[0] - self.player_speed >= 0:
            self.player_pos[0] -= self.player_speed
        elif action == 3 and self.player_pos[0] + self.player_speed + self.player_size[0] <= self.window_size[0]:
            self.player_pos[0] += self.player_speed

        # Проверяем столкновение игрока с зеленым квадратом
        player_rect = np.array([self.player_pos[0], self.player_pos[1], self.player_pos[0] + self.player_size[0], self.player_pos[1] + self.player_size[1]])
        green_square_rect = np.array([self.green_square_pos[0], self.green_square_pos[1], self.green_square_pos[0] + self.square_size[0], self.green_square_pos[1] + self.square_size[1]])
        if self.rect_collision(player_rect, green_square_rect):
            self.score += 10
            self.spawn_green_square()

        # Обновляем счет каждую секунду
        self.score -= 1

        # Вычисляем расстояние до цели
        distance_to_target = np.linalg.norm(np.array(self.player_pos) - np.array(self.green_square_pos))

        # Возвращаем состояние, награду, done и информацию
        state = np.array([self.player_pos[0], self.player_pos[1], self.green_square_pos[0], self.green_square_pos[1]], dtype=np.float32)
        reward = self.score

        # Добавляем поощрение за приближение к цели и наказание за отдаление
        if distance_to_target < self.previous_distance_to_target:
            reward += 1  # Поощрение за приближение
        else:
            reward -= 1  # Наказание за отдаление

        self.previous_distance_to_target = distance_to_target

        done = self.score <= 0
        info = {}

        return state, reward, done, info

    def reset(self):
        # Сбрасываем состояние среды
        self.player_pos = [self.window_size[0] // 2, self.window_size[1] // 2]
        self.score = 10
        self.spawn_green_square()
        self.previous_distance_to_target = np.linalg.norm(np.array(self.player_pos) - np.array(self.green_square_pos))
        state = np.array([self.player_pos[0], self.player_pos[1], self.green_square_pos[0], self.green_square_pos[1]], dtype=np.float32)
        return state

    def rect_collision(self, rect1, rect2):
        return not (rect1[2] <= rect2[0] or rect1[0] >= rect2[2] or rect1[3] <= rect2[1] or rect1[1] >= rect2[3])

    def render(self, mode='human'):
        # Рендеринг среды, если включен
        if self.render_enabled:
            self.screen.fill((0, 0, 0))  # Черный фон
            pg.draw.rect(self.screen, (255, 255, 255), (*self.player_pos, *self.player_size))  # Белый игрок
            pg.draw.rect(self.screen, (0, 100, 0), (*self.green_square_pos, *self.square_size))  # Темно-зеленый квадрат
            score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))
            pg.display.flip()
            self.clock.tick(60)

    def close(self):
        pg.quit()

    def enable_render(self):
        self.render_enabled = True

    def disable_render(self):
        self.render_enabled = False
