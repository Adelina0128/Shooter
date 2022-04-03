#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer

# подгружаем отдельно функции для работы со шрифтом
font.init()
font_titles = font.SysFont('Corbel', 80)
font_subtitles = font.SysFont('Corbel', 35, True) # третий параметр True означает что шрифт будет жирным, четвертый - курсив
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.SysFont('Arial', 36)
lose_boss = font_titles.render('Ты пропустил босса!', True, (180, 0, 0))
restart = font_subtitles.render('R - перезапуск', True, (255, 255, 255))  # сообщение о рестарте
#музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
pain_sound = mixer.Sound('pain.ogg')
collide = mixer.Sound('smeh.ogg')
win_sound = mixer.Sound('win.ogg')
lose_sound = mixer.Sound('lose.ogg')
#картинки:
img_back = 'galaxy.jpg' #фон игры
img_hero = 'Korabl.png' #герой
img_enemy = 'ufo.png' # враг1
img_boss = 'boss.png' # босс
img_bullet = 'bullet.png' #пуля1
img_bullet2 = 'fire_bullet.png' # пуля2
img_ast = 'asteroid.png' #астероид

#счетчики:
score = 0 # сбито кораблей 
goal = 30 # кораблей нужно для победы
lost = 0 # пропущено кораблей
max_lost = 3 # максимальное кол-во проущенных кораблей
life = 5 # очки жизни
boss_life = 5 # очки жизни у босса
first_start = False # переменная чтобы игра не начиналась после запуска
boss_time = False # переменная которая определяет появится босс или нет
boss_comming=20
show_hud = True # переменная которая отвечает за отображение худа
difficult = None

class GameSprite(sprite.Sprite):
    #конструктор  класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x 
        self.rect.y = player_y 
    #метод отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#класс-наследник для спрайта-игрока(управляется стрелками)
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed() #метод для подключения управления
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 85:
            self.rect.x += self.speed
    #метод 'выстрел' (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
    def fire2(self):
        bullet2 = Bullet(img_bullet2, self.rect.centerx, self.rect.top, 30, 40, -15)
        bullets.add(bullet2)

#класс-наследник для врага
class Enemy(GameSprite):
    #движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        #исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Boss(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, lifes_count):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y, 1)
        self.lifes = lifes_count # у босса новое поле для количества жизней
    def update(self):
        global finish
        self.rect.y += self.speed
        if self.rect.y > win_height:
            mixer.music.stop() # останавливаем музыку
            collide.play()
            finish = True
            window.blit(background, (0, 0))
            window.blit(lose_boss, (win_width / 2 - lose_boss.get_width() / 2, 200))
            window.blit(restart, (win_width / 2 - restart.get_width() / 2, 300))

class Asteroid(GameSprite):
    #движение астероидов
    def update(self):
        self.rect.y += self.speed
        global lost
        #исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0

#класс спрайта пули
class Bullet(GameSprite):
    #движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        #исчезает, если дойдет до края экрана
        if self.rect.y < 0:
            self.kill()
            
            
#Игровая сцена:
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Shooter')
background = transform.scale(image.load(img_back), (win_width, win_height))

#Персонажи игры:
ship = Player(img_hero, 5, win_height - 100, 90, 90, 10)
# создание группы спрайтов врагов
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
boss = Boss(img_boss, randint(80, win_width - 80), -40, 80, 81, 10)

#создание группы спрайтов-астероидов
asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Asteroid(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(0, 4))
    asteroids.add(asteroid)

# группа спрайтов-пуль
bullets = sprite.Group()

#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#основной цикл игры:
run = True

rel_time = False #флаг, отвечающий за перезарядку

rel_time2 = False

num_fire = 0 #переменная для подсчета выстрелов

num_fire2 = 0

while run:
    #событие нажатия на кнопку "Закрыть"
    for e in event.get():
        if e.type == QUIT:
            run = False
        #событие нажатия на пробел - спрайт стреляет
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 10 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()

                if num_fire >= 10 and rel_time == False:
                    last_time = timer()
                    rel_time = True

            if e.key == K_TAB   :
                if num_fire2 < 5 and rel_time2 == False:
                    num_fire2 = num_fire2 + 1
                    fire_sound.play()
                    ship.fire2()

                if num_fire2 >= 5 and rel_time2 == False:
                    last_time = timer()
                    rel_time2 = True
            
            # рестарт - клавиша R, сработает только если игра закончена
            elif e.key == K_r and finish:  
                # обнуляемся
                score = 0 # сбито кораблей 
                goal = 30 # кораблей нужно для победы
                lost = 0 # пропущено кораблей
                max_lost = 3 # максимальное кол-во проущенных кораблей
                life = 5 # очки жизни
                boss_life = 5 # очки жизни у босса
                first_start = False # переменная чтобы игра не начиналась после запуска
                boss_time = False # переменная которая определяет появится босс или нет
                boss_comming=20
                show_hud = True # переменная которая отвечает за отображение худа
                difficult = None
                for monster in monsters:
                    monster.kill() # убираем всех врагов
                for asteroid in asteroids:
                    asteroid.kill() # убиваем все астероиды
                ship = Player(img_hero, 5, win_height - 100, 90, 90, 10)
                # создание группы спрайтов врагов
                monsters = sprite.Group()
                for i in range(1, 6):
                    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
                    monsters.add(monster)
                boss = Boss(img_boss, randint(80, win_width - 80), -40, 80, 81, 10)

                #создание группы спрайтов-астероидов
                asteroids = sprite.Group()
                for i in range(1,3):
                    asteroid = Asteroid(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(0, 4))
                    asteroids.add(asteroid)

                # группа спрайтов-пуль
                bullets = sprite.Group()
                finish = False

                for bullet in bullets:
                    ''' удаляем все пули которые на сцене, если этого
                        не сделать они продолжат лететь после рестарта '''
                    bullet.kill()
                if boss_time:
                    boss.kill()
                    boss_time = False
                finish = False
                mixer.music.play() # воспроизводим музыку только при начале игры
            elif e.key == K_h and not first_start and not finish and not pause:
                show_hud = not show_hud # переворачиваем значение худа
# сама игра: действия спрайтов, проверка правил игры, перерисовка
    if not finish:
        #обновление фона
        window.blit(background, (0, 0))

        #производим движения спрайтов
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        if score >= 10 and boss_life!=0:
            window.blit(font2.render("BOSS: " + str(boss.lifes), 1, (255, 0, 0)), (10, 140)) # обновляем счетчик
            boss.update()


        #обновляем их при каждом новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        if score >= 10 and boss_life!=0:
            boss.reset()

        #перезарядка1
        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('Ждите, перезарядка...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0 #сбрасываем счетчик пуль
                rel_time = False #сбрасываем флаг перезарядки

        #перезарядка2
        if rel_time2 == True:
            now_time2 = timer()

            if now_time2 - last_time < 3:
                reload = font2.render('Ждите, перезарядка...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire2 = 0 #сбрасываем счетчик пуль
                rel_time2 = False #сбрасываем флаг перезарядки

        # появление босса
        if score == 10:
            cols = sprite.spritecollide(boss, bullets, True) # собираем касания с пулями
            for col in cols:
                boss.lifes -= 1 # отнимаем боссу жизни
            if show_hud:
                window.blit(font2.render("BOSS: " + str(boss.lifes), 1, (255, 0, 0)), (10, 140)) # обновляем счетчик
            boss.update()
            boss.reset()
            if boss.lifes <= 0: # если у босса кончились жизни
                boss_time = False 
                score += 5 
                boss.kill() # совсем убиваем его со сцены
        if not boss_time and boss_comming - score <= 0: # если не время босса и "когда должен прийти босс" - "текущие очки" меньше или равно нулю, то пришло время выпускать босса
            boss_time = True
            boss = Boss(img_boss, randint(80, win_width - 80), -40, 80, 81, 5) # параметра скорости нет, скорость у боссов - 1
                
        # проверка столкновения пули и монстра(и монстр и пуля при касании исчезнут)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            #этот цикл повториться столько раз, сколько монстров подбито
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        cols = sprite.spritecollide(boss, bullets, True) # собираем касания с пулями
        for col in cols:
            boss.lifes -= 1 # отнимаем боссу жизни

        if boss.lifes <= 0: # если у босса кончились жизни
                boss_time = False 
                score += 5 
                boss.kill() # совсем убиваем его со сцены
                boss_life = 0
        # если спрайт коснулся врага, уменьшает жизни
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life - 1
            pain_sound.play()

        #проигрыш
        if life == 0 or lost >= max_lost or ship.rect.colliderect(boss):
            finish = True
            window.blit(lose, (200, 200))
            window.blit(restart, (win_width / 2 - restart.get_width() / 2, 300))
            lose_sound.play()
        # проверка выигрыша: сколько очков набрали?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
            window.blit(restart, (win_width / 2 - restart.get_width() / 2, 300))
            win_sound.play()
        #пишем текст на экране
        text = font2.render('Счет: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        
        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        #задаем разный цвет в зависимости от кол-ва жизней
        if life >= 4:
            life_color = (0, 150, 0) 
        if life == 3:
            life_color = (150, 150, 0)
        if life <= 2:
            life_color = (150, 0, 0)

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))

        display.update()
    #цикл срабатывает каждую 0.05 секунд
    time.delay(50)