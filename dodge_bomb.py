import os
import sys
import pygame as pg
import random
import time

WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rect: pg.rect) -> tuple[bool,bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：横方向，縦方向の画面内外判定結果
    画面内ならTrue，画面外ならFalse
    """
    vertical,horizontal = True, True
    if (rect.left < 0) or (rect.right > WIDTH):
        vertical = False
    if (rect.top < 0) or (rect.bottom > HEIGHT):
        horizontal = False
    return vertical, horizontal

def GameOver(screen:pg.surface) -> None:
    """
    ゲームオーバー時にゲームオーバーの画面を表示する関数
    """
    box=pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(box, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT,))
    box.set_alpha(200)

    img=pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 1.2)

    moji = pg.font.Font(None, 60)
    text = moji.render("Game Over", True, (255, 255, 255))

    
    screen.blit(box, [0, 0])
    screen.blit(text, [400, 325])
    screen.blit(img, [320, 320])
    screen.blit(img, [660, 320])
    pg.display.update()
    time.sleep(5)
    


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img=pg.Surface((20,20))
    pg.draw.circle(bb_img,(255,0,0) , (10,10) , 10)
    bb_img.set_colorkey((0,0,0))
    bb_rct=bb_img.get_rect()
    bb_rct.center=(random.randint(0,WIDTH),random.randint(0,HEIGHT))
    vx=5
    vy=5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct): # 爆弾に当たったらゲームオーバー
            print("ゲームオーバー")
            GameOver(screen)
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        DELTA={ pg.K_UP : (0,-5) , # 移動量の辞書
                pg.K_DOWN : (0,5) ,
                pg.K_RIGHT : (5,0) ,
                pg.K_LEFT : (-5,0) }
        sum_mv = [0, 0]
        for key,value in DELTA.items():
            if key_lst[key]:
                sum_mv[0]+=value[0]
                sum_mv[1]+=value[1]
                
        kk_rct.move_ip(sum_mv) # こうかとんの移動
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])

        bb_rct.move_ip(vx,vy) # 爆弾の移動
        vertical,horizontal=check_bound(bb_rct)
        if not vertical:
            vx*=-1
        if not horizontal:
            vy*=-1

        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img,bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
