import pygame as pg
import random

# инициализируем библиотеку pg
pg.init()

# определяем размеры окна
window_size = (1280, 720)

# задаем название окна
pg.display.set_caption("PathAi")

# создаем окно
screen = pg.display.set_mode(window_size)

# задаем цвет фона
background_color = (0, 0, 0)  # черный

# задаем цвет игрока
player_color = (255, 255, 255)  # белый

# задаем цвет зеленого квадрата
green_square_color = (0, 100, 0)  # темно-зеленый


# задаем размер игрока и квадратов
player_size = (50, 50)
square_size = (50, 50)

# задаем начальную позицию игрока
player_pos = [window_size[0] // 2, window_size[1] // 2]

# задаем скорость игрока
player_speed = 5

# задаем начальное количество очков
score = 10

# инициализируем шрифт
font = pg.font.Font(None, 36)

# инициализируем таймер
clock = pg.time.Clock()
last_update_time = pg.time.get_ticks()


# функция для движения игрока
def move_player(direction):
    if direction == 'up' and player_pos[1] - player_speed >= 0:
        player_pos[1] -= player_speed
    elif direction == 'down' and player_pos[1] + player_speed + player_size[1] <= window_size[1]:
        player_pos[1] += player_speed
    elif direction == 'left' and player_pos[0] - player_speed >= 0:
        player_pos[0] -= player_speed
    elif direction == 'right' and player_pos[0] + player_speed + player_size[0] <= window_size[0]:
        player_pos[0] += player_speed


# функция для рандомного спавна зеленого квадрата
def spawn_green_square():
    green_square_pos[0] = random.randint(0, window_size[0] - square_size[0])
    green_square_pos[1] = random.randint(0, window_size[1] - square_size[1])



# функция для получения позиции игрока
def get_player_position():
    return player_pos


# функция для получения позиции зеленого квадрата
def get_green_square_position():
    return green_square_pos



# начальная позиция зеленого квадрата
green_square_pos = [0, 0]
spawn_green_square()



def __init__(self, LearningRate=0.01, Epsilon=0.3):

        super().__init__()

        # Слои
        self.inp = nn.Linear(12, 1024)
        self.hidden1 = nn.Linear(1024, 1024)
        self.out = nn.Linear(1024, 4)
        
        # Инициализация слоев
        init.uniform_(self.inp.weight, -1, 1)
        init.uniform_(self.hidden1.weight, -1, 1)
        init.uniform_(self.out.weight, -1, 1)

        
        # Память
        self.memory_states = []
        self.memory_actions = []
        self.memory_rewards = []
        self.memory_next_states = []
        self.memory_isdones = []
        self.memory_len = 0
        self.loses = []
        self.rewards_per_epoch = []

        self.optimizer = optim.Adam(self.parameters(), lr=LearningRate)
        self.criterion = nn.MSELoss()
        self.epsilon = Epsilon
        self.activation = nn.LeakyReLU()



def train_snake(self):
        if (self.memory_len == 0):
            return
        memory_len = self.memory_len
        states, actions, rewards, next_states, isdones = self.samplebatch()

        NeuroNowAnswer = self.forward(states)
        NeuroNextAnswer = self.forward(next_states)
        predicted_now_value = NeuroNowAnswer[range(memory_len), actions]
        predicted_future_value = t.max(NeuroNextAnswer, dim=1)[0]
        predict_target = rewards + predicted_future_value*isdones
        loss = self.criterion(predict_target, predicted_now_value)
        self.loses.append(loss.cpu().item())
        self.rewards_per_epoch.append(t.sum(rewards.cpu()).item())
        self.optimizer.zero_grad()
        loss.backward()
        if (self.inp.weight.grad.norm() < 0.0001):
            self.inp.weight.grad.data += t.FloatTensor([0.001]).cuda()
        self.optimizer.step()
        print(f"Ошибка: {loss}")


train_snake()
# основной игровой цикл
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # получаем состояние клавиш
    keys = pg.key.get_pressed()
    if keys[pg.K_UP]:
        move_player('up')
    if keys[pg.K_DOWN]:
        move_player('down')
    if keys[pg.K_LEFT]:
        move_player('left')
    if keys[pg.K_RIGHT]:
        move_player('right')

    # обновляем счет каждую секунду
    current_time = pg.time.get_ticks()
    if current_time - last_update_time >= 1000:  # 1000 миллисекунд = 1 секунда
        score -= 1
        last_update_time = current_time

    # проверяем столкновение игрока с зеленым квадратом
    player_rect = pg.Rect(player_pos[0], player_pos[1], player_size[0], player_size[1])
    green_square_rect = pg.Rect(green_square_pos[0], green_square_pos[1], square_size[0], square_size[1])
    if player_rect.colliderect(green_square_rect):
        score += 10
        spawn_green_square()

    # заполняем фон заданным цветом
    screen.fill(background_color)

    # рисуем игрока
    pg.draw.rect(screen, player_color, (*player_pos, *player_size))

    # рисуем зеленый квадрат
    pg.draw.rect(screen, green_square_color, (*green_square_pos, *square_size))

    # рендерим текст с количеством очков
    score_text = font.render(f"Score: {score}", True, player_color)

    # отображаем текст на экране
    screen.blit(score_text, (10, 10))

    # обновляем экран для отображения изменений
    pg.display.flip()

    # ограничиваем FPS
    clock.tick(60)

# завершаем работу pg
pg.quit()
