""" invader.py - Copyright 2016 Kenichiro Tanaka """

import sys

from random import randint

import pygame

from pygame.locals import Rect, QUIT, KEYDOWN, \

                          K_LEFT, K_RIGHT, K_SPACE

​

pygame.init()

pygame.key.set_repeat(5, 5)

SURFACE = pygame.display.set_mode((600, 600))                                                                                     #78

FPSCLOCK = pygame.time.Clock()                                                                                                                   #78

​

class Drawable:                              전체 그리는 대상에 공통되는 기능을 제공하는 부모클래스로 객체는 아님 #77

     """ 전체의 그리기 객체의 슈퍼 클래스 """

     def __init__(self, rect, offset0, offset1):                                                                                                    #77

rect는 초기위치, offset0은 첫번째 장 이미지의 옵셋값, offset1은 두번째 장 이미지의 옵셋값

          strip = pygame.image.load("strip.png")                                                                           ​이미지 로드 #77

          self.images = (pygame.Surface((24, 24), pygame.SRCALPHA),

                                   pygame.Surface((24, 24), pygame.SRCALPHA))                   그리는 이미지의 배열 #77

          self.rect = rect                                                                                                 그리는 위치와 크기 초기화 #77

          self.count = 0                                                                   그리는 이미지를 전환하기 위한 카운터 초기화 #77

          self.images[0].blit(strip, (0, 0),

                                        Rect(offset0, 0, 24, 24))                                                                                             #77

          self.images[1].blit(strip, (0, 0),

                                        Rect(offset1, 0, 24, 24))                                                     두장의 이미지를 설정함 #77

각각의 이미지는 strip.png 로부터 특정 위치를 복사

​

     def move(self, diff_x, diff_y):                                                                                                       이동한다 #77

          """ 객체를 이동 """

          self.count += 1                                                                                                                                          #77

          self.rect.move_ip(diff_x, diff_y)                                                                                                            #77

Rect 클래스의 move 메서드를 호출해도 원래의 직사각형 위치는 변하지 않음. 이동후의 새 Rect가 반환됨

move_ip 메서드는 스스로 이동하고 반환값은 없음 ip 는 in-place(그 장소에서)라는 뜻이고 #26에서 다뤘음

​

     def draw(self):                                                                                                                         자신을 그린다 #77

          """ 객체를 그리기 """

          image = self.images[0] if self.count % 2 == 0 \                                                                               #77

                              else self.images[1]

count 값이 짝수일때에는 image[0], 홀수일때에는 image[1]을 그림 #77

          SURFACE.blit(image, self.rect.topleft)                                                                                                  #77

​

class Ship(Drawable):                                                                                                                 내 캐릭터 객체 #79

     """ 내 캐릭터 객체 """

     def __init__(self):                                                                                                                                            #79

          super().__init__(Rect(300, 550, 24, 24), 192, 192)        부모 클래스의 생성자를 명시적으로 호출 #79

내 캐릭터의 초기 위치와 크기 지정

내 캐릭터는 두장의 이미지를 전환할 필요가 없기때문에 같은 옵셋값 192를 지정함

​

class Beam(Drawable):                                                                                                                          빔 객체 #79

     """ 빔 객체 """

     def __init__(self):                                                                                                                                            #79

          super().__init__(Rect(300, 0, 24, 24), 0, 24)     옵셋 위치를 0, 24로 함으로써 빔 이미지가 전환됨 #79

​

class Bomb(Drawable):                                                                                                                      폭탄 객체 #79

     """ 폭탄 객체 """

     def __init__(self):                                                                                                                                            #79

          super().__init__(Rect(300, -50, 24, 24), 48, 72)                                                                                #79

옵셋 위치를 48과 72로 폭탄 이미지가 바뀜

          self.time = randint(5, 220)                                                                                                                      #79

폭탄을 던지는 타이밍을 조정하는 속성 프로퍼티 time을 추가하고 5~220사이의 난수로 초기화

​

class Alien(Drawable):                                                                                                                    외계인 객체 #77

     """ 외계인 객체 """

     def __init__(self, rect, offset, score):                                                                                                          #77

          super().__init__(rect, offset, offset+24)                                                                                               #77

          self.score = score                                                                                                                                        #77

옵셋위치 off와 외계인을 쓰러뜨렸을 때의 점수 score를 인수로 얻음

score는 프로퍼티로 등록

​

def main():

     """ 메인 루틴 """

     sysfont = pygame.font.SysFont(None, 72)

     scorefont = pygame.font.SysFont(None, 36)

     message_clear = sysfont.render("!!CLEARED!!",

                                                                     True, (0, 255, 225))

     message_over = sysfont.render("GAME OVER!!",

                                                                     True, (0, 255, 225))

     message_rect = message_clear.get_rect()

     message_rect.center = (300, 300)                                                                                              메시지 초기화

     game_over = False                                                                                                                          게임오버 여부

     moving_left = True                                                      외계인 전체가 왼쪽 방향으로 움직이고 있는지 여부 #78

     moving_down = False                                             외계인 전체가 아래쪽 방향으로 움직이고 있는지 여부 #78

     move_interval = 20                                                                   외계인이 이동할 때까지의 프레임 수(간격) #78

     counter = 0                                                                                                                                   시간관리용 #78

     score = 0                                                                                                                                                           점수

     aliens = []                                                                                                       외계인 객체를 저장하는 리스트 #77

     bombs = []                                                                                                        폭탄 객체를 저장하는 리스트 #79

     ship = Ship()                                                                                                                내 캐릭터 객체가 생성 #79

     beam = Beam()                                                                                                                       빔 객체가 생성 #79

​

     # 외계인 나열과 초기화                                                                                             외계인의 초기 위치 설정 #77

     for ypos in range(4):                                                                                                                                      #77

          offset = 96 if ypos < 2 else 144                                                                                                               #77

          for xpos in range(10):                                                                                                                               #77

               rect = Rect(100+xpos*50, ypos*50 + 50, 24, 24)                                                                        #77

               alien = Alien(rect, offset, (4-ypos)*10)                                                        줄별로 점수가 달라짐 #77

세로 방향의 루프가 ypos, 가로 방향의 루프가 xpos인 이중 루프

하나의 for문으로 이미지를 전환하기 위해선 한줄의 if문을 사용함

               aliens.append(alien)                                                                                                              aliens에 저장

​

     # 폭탄을 설정

     for _ in range(4):

          bombs.append(Bomb())                          외계인을 만든 후에 폭탄을 4개 만들어 배열 bombs에 추가 #79

​

     while True:

          ship_move_x = 0                                                        내 캐릭터의 이동거리 ship_move_x 을 0으로 초기화

          for event in pygame.event.get():

               if event.type == QUIT:

                    pygame.quit()

                    sys.exit()

               elif event.type == KEYDOWN:

                    if event.key == K_LEFT:

                         ship_move_x = -5

                    elif event.key == K_RIGHT:

                         ship_move_x = +5                                                                   좌우키면 내 캐릭터의 이동량을 설정

                    elif event.key == K_SPACE and beam.rect.bottom < 0:

                         beam.rect.center = ship.rect.center

스페이스키, 그리고 빔이 발사중이 아니면 빔 위치를 내 캐릭터 위치로 초기화

​

          if not game_over:

               counter += 1

               # 내 캐릭터를 이동

               ship.move(ship_move_x, 0)

​

               # 빔을 이동

               beam.move(0, -15)

​

               # 외계인을 이동

               area = aliens[0].rect.copy()                                                                                                                 #78

리스트 맨 앞의 외계인 직사각형 aliens[0].rect를 복사해서 변수 area에 저장

aliens[0]으로 하는 이유는 첫번째 외계인이 없어질때까지 계속 게임이 진행되어야 하기때문

예를들어 aliens[5]로 하면 게임이 정상적으로 진행이 되다가

외계인이 5개가 남아 aliens[5]가 없어졌을때 게임이 진행되지 않음

               for alien in aliens:                                                                                                                                  #78

                    area.union_ip(alien.rect)                                                                                                                #78

Rect 클래스의 union_ip 메서드는 인수의 직사각형을 포함하도록 크기를 변경

area에 대해서 모든 외계인을 호출함으로써 모든 외계인을 포함하는 최소 직사각형을 구함

Rect 클래스의 union 메서드는 자신과 인수의 Rect를 포함하는 최소 Rect를 반환함​

​

               if counter % move_interval == 0:                                                                                                     #78

외계인이 이동할 때까지의 프레임 수(간격)

처음엔 1초에 1번씩 외계인이 움직임

                    move_x = -5 if moving_left else 5                                                                     왼쪽부터 움직임 #78

                    move_y = 0                                                                                                                                        #78

​

                   if (area.left < 10 or area.right > 590) and \                                                                               #78

                                    not moving_down:                                                                                                          #78

외계인 집단의 직사각형이 양쪽 끝에 도달했을 때

                       moving_left = not moving_left                                                          좌우 이동 방향을 반전함 #78

                       move_x, move_y = 0, 24                                                             아래 방향으로의 이동량 설정 #78

                       move_interval = max(1, move_interval - 2)

            move_interval 값을 줄여서 외계인 속도를 올림 #78

                       moving_down = True                                                      아래방향 이동 플래그를 True로 설정 #78

                  else:                                                                                                                                                       #78

                       moving_down = False                                                                                                                  #78

​

                 for alien in aliens: #78

                       alien.move(move_x, move_y)                                            전체 외계인에게 그 이동을 적용함 #78

최소 직사각형이 화면 오른쪽 끝에 도달하면 아래로 이동해서 왼쪽방향으로

왼쪽 끝에 도착하면 아래로 이동해서 오른쪽 방향으로 움직여야함

프레임마다 외계인을 너무 빨리 움직이지 않으려고 어느 정도의 간격으로 이동할지 변수 move_interval을 사용

counter가 이 값의 배수가 되었을때 이동함

이동량은 변수 move_x 와 move_y에 설정함​

​

            if area.bottom > 550:                                                 외계인집단의 직사각형의 아래쪽이 550보다 커지면

                 game_over = True                                                             외계인이 화면 아래까지 왔기때문에 게임오버

​

           # 폭탄을 이동

           for bomb in bombs:

폭탄투하 코드로 이번 구현에서는 대기 상태의 폭탄은 화면 밖에 배치하기로 함 #79

                if bomb.time < counter and bomb.rect.top < 0:                 폭탄 투하시간이 지났으면 투하시작 #79

                    enemy = aliens[randint(0, len(aliens) - 1)]              어느 외계인이 투하할지를 난수로 정하고 #79

                    bomb.rect.center = enemy.rect.center

그 외계인의 직사각형을 폭탄 투하 시작위치로 설정 #79

​

                if bomb.rect.top > 0:                                                                          폭탄 투하중(대기상태가 아님) #79

                    bomb.move(0, 10)                                                                             폭탄을 아래로 10만큼 이동 #79

​

                if bomb.rect.top > 600:                                                              폭탄이 화면 아래까지 도달했을 때 #79

                    bomb.time += randint(50, 250)                                                  폭탄 투하 시각을 난수로 결정 #79

                    bomb.rect.top = -50                                                   폭탄을 화면 밖에 배치하고 대기 상태로 함 #79

​

                if bomb.rect.colliderect(ship.rect):                                                                                                  #79

폭탄이 내 캐릭터와 충돌했으면(colliderect는 #59에서 다뤘음)

colliderect는 두 사각형이 겹치는지(충돌) 여부를 반환

                    game_over = True                                                                                                            게임오버 #79

​

          # 빔과 외계인 충돌?                                                                                         내 캐릭터가 발사한 빔 처리 #79

          tmp = []                                                                                                                                                        #79

          for alien in aliens:                                                                                                                                       #79

               if alien.rect.collidepoint(beam.rect.center):                                                                                   #79

빔이 외계인과 충돌했는지 collidepoint를 사용해 판정

collidepoint는 점이 자신에게 포함되는지 아닌지 여부 반환

ex) collidepoint(x, y) : (x, y)라는 점이 자신에게 포함되는지 아닌지 여부 반환

                   beam.rect.top = -50                                  충돌했으면 빔을 화면 밖에 배치해서 대기상태로 하고 #79

                   score += alien.score                                                                                                     점수를 더함 #79

               else:                                                                                                                                                         #79

                   tmp.append(alien)                            빔이 충돌한 외계인을 제거하기 위하여 임시변수 tmp 사용 #79

충돌하지 않은 외계인만 aliens 에 저장됨

          aliens = tmp                                                                                                                                                #79

          if len(aliens) == 0:                                                                                  배열 aliens 의 길이가 0이 되면 #79

               game_over = True                                                                      모든 외계인을 쓰러뜨려서 게임오버 #79

​

     # 그리기

     SURFACE.fill((0, 0, 0))                                                                                                 배경을 검정색으로 칠하고

     for alien in aliens:                                                                                                                                외계인 그림

          alien.draw()

     ship.draw()                                                                                                                                      내 캐릭터 그림

     beam.draw()                                                                                                                                               빔 그림

     for bomb in bombs:                                                                                                                               폭탄 그림

          bomb.draw()

​

     score_str = str(score).zfill(5)

     score_image = scorefont.render(score_str,

                                        True, (0, 255, 0))

     SURFACE.blit(score_image, (500, 10))                                                                                   점수를 나타내고

​

     if game_over:

          if len(aliens) == 0:

               SURFACE.blit(message_clear, message_rect.topleft)

          else:

               SURFACE.blit(message_over, message_rect.topleft)                                                        메시지 표시

​

     pygame.display.update()                                                                                                           화면에 반영하고

     FPSCLOCK.tick(20)                                                                                                                 프레임 레이트 조정

​

if __name__ == '__main__':

     main()

​
