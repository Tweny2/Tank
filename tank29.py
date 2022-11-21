"""
v1.28

    新增功能：
        1.添加开场鸡汤音效
        2.添加子弹音效







"""

import pygame,time,random
_display=pygame.display
COLOR_BLACK = pygame.Color(0, 0, 0)
COLOR_RED=pygame.Color(255,0,0,)


version='v1.28'

class MainGame():
    # 游戏主窗口
    window=None
    SCREEN_HEIGHT=500
    SCREEN_WIDTH=800
    #创建我方坦克
    TANK_P1=None
    #存储所有敌方坦克
    EnemyTank_list=[]
    #要创建的敌方坦克的数量
    EnemyTank_count = 5
    #储存我方子弹的列表
    Bullet_list=[]
    #存储敌方子弹的列表
    enemyBulletList=[]
    #爆炸效果列表
    explodeList = []
    #墙壁列表
    wallList = []


    # 开始游戏方法
    def startGame(self):
        _display.init()
        # 加载主窗口（借鉴官方文档）
        MainGame.window=_display.set_mode([MainGame.SCREEN_WIDTH,MainGame.SCREEN_HEIGHT])
        #加载敌我坦克
        self.createMyTank()
        self.createEnemyTank()
        #加载墙壁
        self.createWalls()
        #设置游戏标题
        _display.set_caption("坦克大战"+version)
        #让窗口持续刷新
        while True:
            #窗口颜色填充
            MainGame.window.fill(COLOR_BLACK)
            #在循环中持续完成事件的获取
            self.getEvent()
            #将绘制文字得到的小画布，粘贴到窗口中
            MainGame.window.blit(self.getTextSurface("剩余敌方坦克%d辆"%len(MainGame.EnemyTank_list)),(5,5))
            #调用展示墙壁的方法
            self.blitWalls()
            #调用展示我方坦克的方法
            if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                MainGame.TANK_P1.displayTank()
            else:
                del MainGame.TANK_P1
                MainGame.TANK_P1 = None
            #调用循环展示敌方坦克
            self.blitEnemyTank()
            #根据坦克的开关状态，调用坦克的移动方法
            if MainGame.TANK_P1 and not MainGame.TANK_P1.stop:
                MainGame.TANK_P1.move()
                #调用碰撞墙壁的方法
                MainGame.TANK_P1.hitWalls()
                MainGame.TANK_P1.hitEnemyTank()
            time.sleep(0.03)
            #调用渲染子弹列表的一个方法
            self.blitBullet()
            #调用渲染敌方子弹列表的一个方法
            self.blitEnemyBullet()
            #调用展示爆炸效果的方法
            self.displayExplodes()


            #窗口的刷新
            _display.update()
    #创建我方坦克的方法
    def createMyTank(self):
        # 创建我方坦克
        MainGame.TANK_P1 = MyTank(400, 300)
        #创建音乐对象
        music = Music("img/startC.mp3")
        #调用播放音乐方法
        music.play()
    #创建敌方坦克
    def createEnemyTank(self):
        top=100
        speed=random.randint(3,6)
        for i in range(MainGame.EnemyTank_count):
            #每次都随机生成一个left值
            left = random.randint(1, 7)
            eTank=EnemyTank(left*100,top,speed)
            MainGame.EnemyTank_list.append(eTank)
    #创建墙壁的方法
    def createWalls(self):
        for i in range(1,6):
            wall = Wall(145*i,160)
            MainGame.wallList.append(wall)
    #将墙壁加入到窗口中
    def blitWalls(self):
        for wall in MainGame.wallList:
            if wall.live:
                wall.displayWall()
            else:
                MainGame.wallList.remove(wall)
    #将敌方坦克加入到窗口中
    def blitEnemyTank(self):
        for eTank in MainGame.EnemyTank_list:
            if eTank.live:
                eTank.displayTank()
                #eTank移动的方法
                eTank.randMove()
                #调用敌方坦克与墙壁的碰撞方法
                eTank.hitWalls()
                #调用敌方坦克的射击
                eBullet = eTank.shot()
                #敌方子弹是否是None，如果不为None则添加到敌方子弹列表中
                if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                    # 调用敌方坦克碰撞我方坦克方法
                    eTank.hitMyTank()
                if eBullet:
                    #将子弹存储到敌方子弹列表
                    MainGame.enemyBulletList.append(eBullet)
            else:
                MainGame.EnemyTank_list.remove(eTank)
    #将我方子弹加入到窗口中
    def blitBullet(self):
        for bullet in MainGame.Bullet_list:
            #如果子弹还活着，绘制出来，否则，直接从列表中移除该子弹
            if bullet.live:
                bullet.displayBullet()
                #让子弹移动
                bullet.bulletMove()
                #调用我方子弹与敌方坦克的碰撞方法
                bullet.hitEnemyTank()
                #调用判断我方子弹是否碰撞到墙壁的方法
                bullet.hitWall()
            else:
                MainGame.Bullet_list.remove(bullet)
    #将敌方子弹加入到窗口中
    def blitEnemyBullet(self):
        for eBullet in MainGame.enemyBulletList:
            #如果子弹还活着，绘制出来，否则，直接从列表中移除该子弹
            if eBullet.live:     #判断敌方子弹是否存活
                eBullet.displayBullet()
                #让子弹移动
                eBullet.bulletMove()
                #调用是否碰到墙壁的方法
                eBullet.hitWall()
                if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                    eBullet.hitMyTank()
            else:
                MainGame.enemyBulletList.remove(eBullet)
    #展示爆炸效果列表
    def displayExplodes(self):
        for explode in MainGame.explodeList:
            if explode.live:
                explode.displayExplode()
            else:
                MainGame.explodeList.remove(explode)
    #获取程序运行期间所有事件（鼠标事件，键盘事件）
    def getEvent(self):
        #1.获取所有事件aaa
        eventList=pygame.event.get()
        #2.对事件进行判断处理（1、点击关闭按钮   2、按下键盘上的某个按键）
        for event in eventList:
            #判断event.type 是否quit,如果是退出的话，直接调用程序结束方法
            if event.type==pygame.QUIT:
                self.endGame()
            #判断事件类型是否为按键按下，如果是，继续判断按键是哪一个按键，来进行对应的处理
            if event.type==pygame.KEYDOWN:
                #点击ESC按键让我方坦克重生
                if event.key == pygame.K_ESCAPE and not MainGame.TANK_P1:
                    #调用创建我方坦克的方法
                    self.createMyTank()
                if MainGame.TANK_P1 and MainGame.TANK_P1.live:

                    # 判断按下的是上、下、左、右
                    if event.key == pygame.K_a:
                        print("坦克向左调头，移动")
                        MainGame.TANK_P1.direction = 'L'
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_d:
                        print("坦克向右调头，移动")
                        MainGame.TANK_P1.direction = 'R'
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_w:
                        print("坦克向上调头，移动")
                        MainGame.TANK_P1.direction = 'U'
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_s:
                        print("坦克向下调头，移动")
                        MainGame.TANK_P1.direction = 'D'
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_SPACE:
                        MainGame.TANK_P1.stop = True
                        print("发射子弹")
                        if len(MainGame.Bullet_list) < 3:
                            # 产生一颗子弹
                            m = Bullet(MainGame.TANK_P1)
                            # 将子弹加入到子弹列表
                            MainGame.Bullet_list.append(m)
                            #新增子弹发射音效
                            music = Music("img/missileS.mp3")
                            music.play()
                        else:
                            print("子弹数量不足")
                        print("当前屏幕中的子弹数量为：%d" % len(MainGame.Bullet_list))

            #结束游戏方法
            if event.type==pygame.KEYUP:
                #松开的如果是方向键，才更改移动开关状态：
                if event.key == pygame.K_a or event.key==pygame.K_d or event.key == pygame.K_w  or event.key==pygame.K_s:
                   if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                       # 修改坦克的状态
                       MainGame.TANK_P1.stop = True
    #左上角文字绘制的功能
    def getTextSurface(self,text):
        #初始化字体模块
        pygame.font.init()
        #查看系统支持的字体
        #fontList=pygame.font.get_fonts()
        #选中一个合适字体
        font=pygame.font.SysFont("kaiti",18)
        #使用对应的字符完成相关内容的绘制
        textSurface=font.render(text,True,COLOR_RED)
        return textSurface

    # 结束游戏
    def endGame(self):
        print("GAME OVER")
        exit()#结束python解释器
class BaseItem(pygame.sprite.Sprite):
    def __int__(self):
        pygame.sprite.Sprite.__init__(self)
class Tank(BaseItem):
    def __init__(self,left,top):
        self.images={
            'U':pygame.image.load("img/MyTank_U.png"),
            'D':pygame.image.load("img/MyTank_D.png"),
            'L':pygame.image.load("img/MyTank_L.png"),
            'R':pygame.image.load("img/MyTank_R.png"),

        }
        self.direction='U'
        self.image=self.images[self.direction]
        #坦克所在区域    Rect->
        self.rect=self.image.get_rect()
        #指定坦克初始化位置,分别距x，y轴的位置
        self.rect.left=left
        self.rect.top=top
        #新增速度属性
        self.speed=5
        #新增属性：坦克的移动开关
        self.stop=True
        #新增属性  live  用来记录，坦克是否活着
        self.live=True
        #新增属性：用来记录坦克移动之前的坐标(用于坐标还原时使用)
        self.oldLeft = self.rect.left
        self.oldTOP = self.rect.top

    # Tank移动方法
    def move(self):
        #先记录移动之前的坐标
        self.oldLeft = self.rect.left
        self.oldTOP = self.rect.top
        #判断坦克的方向进行移动
        if self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction=='R':
            if self.rect.left+self.rect.height<MainGame.SCREEN_WIDTH:
                self.rect.left += self.speed
        elif self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction=='D':
            if self.rect.top+self.rect.width<MainGame.SCREEN_HEIGHT:
                self.rect.top += self.speed
    def stay(self):
        self.rect.left = self.oldLeft
        self.rect.top = self.oldTOP
    #新增碰撞墙壁的方法
    def hitWalls(self):
        for wall in MainGame.wallList:
            if pygame.sprite.collide_rect(wall, self):
                self.stay()
    # 坦克射击方法
    def shot(self):
        return Bullet(self)
    #展示坦克(将坦克这个surface绘制到窗口中   blit())
    def displayTank(self):
        #1.重新设置坦克的图片
        self.image=self.images[self.direction]
        #2.将坦克加入到窗口中
        MainGame.window.blit(self.image,self.rect)
class MyTank(Tank):
    def __init__(self,left,top):
        super(MyTank,self).__init__(left,top)
    #新增主动碰撞到敌方坦克的方法
    def hitEnemyTank(self):
        for eTank in MainGame.EnemyTank_list:
            if pygame.sprite.collide_rect(eTank,self):
                self.stay()
class EnemyTank(Tank):
    def __init__(self,left,top,speed):
            super(EnemyTank,self).__init__(left,top)
            #self.live=True  (第二种方法)
            # 加载图片集
            self.images = {
                'U': pygame.image.load("img/Enemy1_U.png"),
                'D': pygame.image.load("img/Enemy1_D.png"),
                'L': pygame.image.load("img/Enemy1_L.png"),
                'R': pygame.image.load("img/Enemy1_R.png"),

            }
            self.direction =self.randDirection()
            self.image = self.images[self.direction]
            # 坦克所在区域    Rect->
            self.rect = self.image.get_rect()
            # 指定坦克初始化位置,分别距x，y轴的位置
            self.rect.left = left
            self.rect.top = top
            # 新增速度属性
            self.speed = speed
            self.stop=True
            #新增步数属性，用来控制敌方坦克随即移动
            self.step=50

    def randDirection(self):
        num= random.randint(1,4)
        if num==1:
            return 'U'
        elif num == 2:
            return 'D'
        elif num == 3:
            return 'L'
        elif num == 4:
            return 'R'
    #随机移动
    def randMove(self):
            if self.step<=0:
                self.direction=self.randDirection()
                self.step=50
            else:
                self.move()
                #让步数递减
                self.step-=1
    #重写shot()
    def shot(self):
        #随机生成100以内的数
        num=random.randint(1,100)
        if num<10:
            return Bullet(self)
    #新增敌方坦克主动碰撞我方坦克的方法
    def hitMyTank(self):
        if pygame.sprite.collide_rect(self,MainGame.TANK_P1):
            #让敌方坦克停下来
            self.stay()
class Bullet(BaseItem):
    def __init__(self,tank):
        pass
        #图片
        self.image=pygame.image.load('img/Missile.png')
        #方向（坦克方向）
        self.direction= tank.direction
        #位置
        self.rect=self.image.get_rect()
        if self.direction=='U':

            self.rect.left=tank.rect.left+tank.rect.width/2-self.rect.width/2
            self.rect.top=tank.rect.top-self.rect.height
        elif self.direction=='D':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top +tank.rect.height
        elif self.direction=='L':
            self.rect.left = tank.rect.left - self.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.width/2-self.rect.width/2
        elif self.direction=='R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top +tank.rect.width/2-self.rect.width/2
        #速度
        self.speed=7
        #用来记录子弹是否活着
        self.live = True
    # 子弹移动方法
    def bulletMove(self):
        if self.direction == "U":
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                #修改状态值
                self.live = False
        elif self.direction == "D":
            if self.rect.top < MainGame.SCREEN_HEIGHT-self.rect.height:
                self.rect.top += self.speed
            else:
                #修改状态值
                self.live = False
        elif self.direction == "L":
            if self.rect.left>0:
                self.rect.left -= self.speed
            else:
                #修改状态值
                self.live = False
        elif self.direction == "R":
            if self.rect.left < MainGame.SCREEN_WIDTH-self.rect.width:
                self.rect.left += self.speed
            else:
                #修改状态值
                self.live = False
    # 子弹展示方法
    def displayBullet(self):
        MainGame.window.blit(self.image,self.rect)
    #新增我方子弹碰撞敌方坦克的方法
    def hitEnemyTank(self):
        for eTank in MainGame.EnemyTank_list:
            if pygame.sprite.collide_rect(eTank,self):
                #产生一个爆炸效果
                explode = Explode(eTank)
                #将爆炸效果加入到爆炸效果列表中
                MainGame.explodeList.append(explode)
                self.live=False
                eTank.live=False
    #新增敌方子弹与我方坦克的碰撞方法
    def hitMyTank(self):
        if pygame.sprite.collide_rect(self,MainGame.TANK_P1):
            # 产生爆炸效果，并加入到爆炸效果列表中
            explode = Explode(MainGame.TANK_P1)
            MainGame.explodeList.append(explode)
            #修改子弹状态
            self.live = False
            #修改我方坦克状态
            MainGame.TANK_P1.live = False
    #新增子弹与墙壁的碰撞方法
    def hitWall(self):
        for wall in MainGame.wallList:
            if pygame.sprite.collide_rect(wall,self):
                #修改子弹的attribute of live
                self.live = False
                wall.hp -= 1
                if wall.hp <= 0:
                    wall.live = False
class Explode():
    def __init__(self,tank):
        self.rect = tank.rect
        self.step = 0
        self.images = [
            pygame.image.load("img/blast_01.png"),
            pygame.image.load("img/blast_02.png"),
            pygame.image.load("img/blast_03.png"),
            pygame.image.load("img/blast_04.png"),
            pygame.image.load("img/blast_05.png"),
            pygame.image.load("img/blast_06.png")
        ]
        self.image = self.images[self.step]
        self.live = True
    # 展示爆炸效果
    def displayExplode(self):
        if self.step < len(self.images):
            MainGame.window.blit(self.image,self.rect)
            self.image = self.images[self.step]
            self.step += 1
        else:
            self.live = False
            self.step = 0
class Wall():
    def __init__(self,left,top):
        self.image = pygame.image.load("img/steel.gif")
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        #用来判断墙壁是否应该在窗口中展示
        self.live = True
        #用来记录墙壁的生命值
        self.hp = 3
    # 展示墙壁的方法
    def displayWall(self):
        MainGame.window.blit(self.image,self.rect)
class Music():
    def __init__(self,fileName):
        self.fileName = fileName
        #先初始化混合器
        pygame.mixer.init()
        pygame.mixer.music.load(self.fileName)
    # 开始播放音乐
    def play(self):
        pygame.mixer.music.play(loops=0)
MainGame().startGame()











