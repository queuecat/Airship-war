import pygame
import sys
#导入所有pygame.locals里的变量（比如下面大写的QUIT变量）
from pygame.locals import *
import random


class flyShip(object):
    """定义一个飞艇类"""
    def __init__(self):
        """定义初始化方法"""
        self.shipStatus = pygame.image.load("飞艇.png")#飞艇图片
        self.width = self.shipStatus.get_width()  # 飞艇宽度
        self.height = self.shipStatus.get_height()  # 飞艇高度
        self.shipX = 50  # 飞艇所在X轴坐标
        self.shipY = 220  # 飞艇所在Y轴坐标,即上下飞行高度
        self.Speed = 10  # 单次移动高度
        self.dead = False  # 默认飞艇生命状态为活着
    def isDead(self):# 检测飞艇是否需要死亡
        for badship in badShips:
            #碰撞检测
            if(badship.shipX <= self.shipX + self.width and badship.shipX + badship.width >= self.shipX and badship.shipY <= self.shipY + self.height and badship.shipY + badship.height >= self.shipY ):
                self.dead = True# 飞艇置死
                self.shipStatus = pygame.image.load("飞艇dead.png")#更换飞艇图片



class BadFlyShip(object):
    """定义一个敌对飞艇类"""
    def __init__(self):
        """定义初始化方法"""
        self.shipStatus = pygame.image.load("飞艇2.png")#飞艇图片
        self.width = self.shipStatus.get_width()#飞艇宽度
        self.height = self.shipStatus.get_height()#飞艇高度
        self.shipX = 1030  # 飞艇所在X轴坐标,即左右飞行高度
        self.shipY = random.randint(0,510-self.height)  # 飞艇所在Y轴坐标,即上下飞行高度
        self.Speed = random.randint(1,5)  # 移动速度
        self.SpeedY = random.randint(1,2)  # 垂直移动速度
        self.range = random.randint(50,100) # 上下移动范围
        self.rangeT = self.shipY - self.range if  ((self.shipY - self.range) > 0) else 0 # 上范围
        self.rangeB = self.shipY + self.range if  ((self.shipY + self.range) < size[1]-self.height) else size[1]-self.height # 上范围
        self.dead = False  # 默认飞艇生命状态为活着

    def updateX(self):
        """水平移动"""
        self.shipX-=self.Speed
        if(self.shipX<=-50 or self.shipY>= size[1]):
            badShips.remove(self)
    def updateY(self):
        """垂直移动"""
        if(self.SpeedY>0):#向下移动
            #检测是否触底
            if(self.shipY+self.SpeedY>self.rangeB):
                self.shipY = self.rangeB
                self.SpeedY=-self.SpeedY
            else:
                self.shipY += self.SpeedY
        elif(self.SpeedY<0):#向上移动
            #检测是否触顶
            if (self.shipY + self.SpeedY < self.rangeT):
                self.shipY = self.rangeT
                self.SpeedY = -self.SpeedY
            else:
                self.shipY += self.SpeedY
    def isDead(self):# 检测飞艇是否需要死亡
        for bullet in bullets:
            #碰撞检测
            if(bullet.bulletX <= self.shipX + self.width and bullet.bulletX + bullet.width >= self.shipX and bullet.bulletY <= self.shipY + self.height and bullet.bulletY + bullet.height >= self.shipY ):
                self.Speed = 0#飞艇坠落
                self.rangeB = size[1]#飞艇坠落
                self.SpeedY = 2 #飞艇坠落
                self.shipStatus = pygame.image.load("飞艇dead2.png")#更换飞艇图片
                bullets.remove(bullet) # 子弹使用
                if (not self.dead):
                    global point
                    point += 1
                self.dead = True #飞艇置死


class Bullet:
    """定义子弹飞艇类"""
    def __init__(self):
        self.bulletStatus = pygame.image.load("子弹.png")  # 子弹图片
        self.width = self.bulletStatus.get_width()  # 子弹宽度
        self.height = self.bulletStatus.get_height()  # 子弹高度
        self.bulletX = 50 + ship.width  # 子弹所在X轴坐标,即左右飞行高度
        self.bulletY = ship.shipY + ship.height / 2 # 子弹所在Y轴坐标,即上下飞行高度
        self.Speed = 3  # 移动速度
        self.dead = False  # 检测子弹是否被激发
    def updateX(self):
        """水平移动"""
        self.bulletX+=self.Speed
        if(self.dead or self.bulletX>= size[0]):
            bullets.remove(self)
def createMap():
    """定义创建地图的方法"""
    screen.blit(bg, bgPosition)  # 将背景图片画到窗口上
    if(not ship.dead):# 我方飞艇存活
        # 显示飞艇
        screen.blit(ship.shipStatus, (ship.shipX, ship.shipY))
        # 显示子弹
        for bullet in bullets:
            screen.blit(bullet.bulletStatus, (bullet.bulletX, bullet.bulletY))
            # 子弹水平移动
            bullet.updateX()

        if(Play):#检测是否点击开始游戏
            play_text = "PLAY" #play
            play_font = pygame.font.SysFont("Arial", 70)
            play_surf = play_font.render(play_text, 1, (255, 255, 255))
            screen.blit(play_surf, [screen.get_width() / 2 - play_surf.get_width() / 2, 200])
            rule_text = "使用上下或ws键控制飞艇躲避来袭敌人，按下空格发射子弹击落敌方飞艇"  # 玩法
            rule_font = pygame.font.SysFont("simHei", 20)
            rule_surf = rule_font.render(rule_text, 1, (255, 255, 255))
            screen.blit(rule_surf, [screen.get_width() / 2 - rule_surf.get_width() / 2, 50])
        else:
            # 积分板
            showPoint()
            createBadShip()  # 向敌人列表中添加敌人对象
            # 遍历敌人列表
            for badShip in badShips:
                # 显示敌人
                screen.blit(badShip.shipStatus, (badShip.shipX, badShip.shipY))
                # 敌人水平移动
                badShip.updateX()
                # 敌人垂直移动
                badShip.updateY()
                # 检测是否被击中
                badShip.isDead()

        # 检测飞艇是否死亡
        ship.isDead()
    else:#我方飞艇死亡，显示结束信息等待关闭窗口
        # 遍历敌人列表
        for badShip in badShips:
            # 显示敌人
            screen.blit(badShip.shipStatus, (badShip.shipX, badShip.shipY))
        # 显示飞艇
        screen.blit(ship.shipStatus, (ship.shipX, ship.shipY))
        final_text1 = "Game Over"
        final_text2 = " GitHub: https://github.com/queuecat/Airship-war"
        final_text3 = "© QueueCat"
        ft1_font = pygame.font.SysFont("Arial", 70)  # 设置第一行文字字体
        ft1_surf = ft1_font.render(final_text1, 1, (255, 255, 255))  # 设置第一行文字颜色
        ft2_font = pygame.font.SysFont("Arial", 30)  # 设置第二行文字字体
        ft2_surf = ft2_font.render(final_text2, 1, (255, 255, 255))  # 设置第二行文字颜色
        ft3_font = pygame.font.SysFont("Arial", 30)  # 设置第三行文字字体
        ft3_surf = ft3_font.render(final_text3, 1, (255, 255, 255))  # 设置第三行文字颜色
        screen.blit(ft1_surf, [screen.get_width() / 2 - ft1_surf.get_width() / 2, 100])  # 设置第一行文字显示位置
        screen.blit(ft2_surf, [screen.get_width() / 2 - ft2_surf.get_width() / 2, 300])  # 设置第二行文字显示位置
        screen.blit(ft3_surf, [screen.get_width() / 2 - ft3_surf.get_width() / 2, 400])  # 设置第三行文字显示位置


    # 背景移动
    if(-(bgPosition[0]-1)<bgsize[0]-size[0]):
        bgPosition[0]-=1
    else:
        bgPosition[0]=0
    pygame.display.flip()  # 更新全部显示
def createBadShip():#创建敌方飞机
    global oldTime,count,createTime,fps
    # if((int)(time.time()) % createTime == 0 and (int)(time.time()) != oldTime):
    if(oldTime == 0):
        badShips.append(BadFlyShip())
        oldTime = createSurface+1
    if (createSurface % (createTime*fps) == 0 and createSurface != oldTime):
        oldTime=createSurface
        badShips.append(BadFlyShip())
        count -= 1
        if(count<=0):
            count=5
            fps = 1 if fps-1<=0  else fps-1
def keydown(key):#用于每隔50毫秒按下一次键盘
    if (createSurface % 4 == 0):
        if (key == 1073741906 or key == 119):  # 上将或W键
            ship.shipY = ship.shipY - ship.Speed if ((ship.shipY - ship.Speed) > 0) else 0
        elif (key == 1073741905 or key == 115):  # 下键或S键
            ship.shipY = ship.shipY + ship.Speed if ((ship.shipY + ship.Speed) < size[1] - ship.shipStatus.get_height()) else size[1] - ship.shipStatus.get_height()

def showPoint():
    global point
    point_text1 = "积分："+str(point)
    point_font = pygame.font.SysFont("simHei", 20)  # 设置第一行文字字体
    point_surf = point_font.render(point_text1, 1, (255, 255, 255))  # 设置第一行文字颜色
    screen.blit(point_surf, [0, 0])  # 设置第一行文字显示位置
if __name__ == '__main__':
    pygame.init()  # 初始化pygame
    pygame.font.init()  # 初始化字体
    fpsClock = pygame.time.Clock() # 获得pygame的时钟
    size = width, height = 1030, 510  # 设置窗口大小
    screen = pygame.display.set_mode(size)  # 显示窗口
    pygame.display.set_caption('飞艇大战')  # 设置标题
    pygame.display.set_icon(pygame.image.load('飞艇.png'))  # 设置窗口图标
    font = pygame.font.SysFont("Arial", 50)  # 设置字体和大小
    bg = pygame.image.load('bg.jpg')  # 加载背景图片
    bgsize = bg.get_size() # 存储图片大小
    bgPosition = [0,0]# 存储背景图片偏移量
    ship = flyShip()# 实例化飞艇
    #badShip = BadFlyShip()#实例化敌人
    badShips = []#敌人序列
    bullets = [] # 子弹序列
    count = 5  # 每5个飞船后增加难度
    createTime = 6 #创建飞艇间隔
    fps = 60 # 更新时间
    oldTime = 0 # 互斥锁
    createSurface = 1 # 充当计算机时间
    Play = True #显示游戏开始界面
    pygame.key.set_repeat(250,50)
    isdowbKey = False # 上下按键检测变量
    point = 0 # 积分
    while True:  # 循环确保窗口一直显示
        # 检测上下键是否被按下，按下则调用方法使其继续运动（防止其他事件打断该事件）
        if(isdowbKey and not ship.dead):
            downKeys = pygame.key.get_pressed()
            if (downKeys[K_UP] == 1 or downKeys[K_w] == 1):
                keydown(K_UP)
            elif (downKeys[K_DOWN] == 1 or downKeys[K_s] == 1):
                keydown(K_DOWN)
            else:
                isdowbKey = False
        for event in pygame.event.get():  # 遍历所有事件

            if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
                sys.exit()

            if event.type == pygame.KEYDOWN and not ship.dead:# 键盘按下事件
                #获取所有按键元组
                keys = pygame.key.get_pressed()
                if(event.key==1073741906 or event.key==119):#上将或W键
                    # ship.shipY = ship.shipY - ship.Speed if ((ship.shipY - ship.Speed) > 0) else 0
                    isdowbKey = True
                elif(event.key==1073741905 or event.key==115):#下键或S键
                    # ship.shipY = ship.shipY + ship.Speed if ((ship.shipY + ship.Speed) < size[1] - ship.shipStatus.get_height()) else size[1] - ship.shipStatus.get_height()
                    isdowbKey = True
            if event.type == KEYUP and not ship.dead:
                if (event.key == K_SPACE):
                    bullets.append(Bullet())
            if event.type ==  MOUSEBUTTONDOWN:
                pressed_array = pygame.mouse.get_pressed()
                for index in range(len(pressed_array)):
                    if pressed_array[index]:
                        if index == 0:
                            Play = False# 鼠标点击后，进入游戏



        createMap()# 更新地图
        createSurface += 1

        fpsClock.tick(60)  # 设置时钟间隔
    pygame.quit()  # 退出pygame