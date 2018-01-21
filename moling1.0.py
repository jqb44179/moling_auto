# coding: utf-8
import os
import shutil
import time
import math
import wda
from PIL import Image, ImageDraw
import pytesseract
import random
import json
# import atx

# d = atx.connect()
c = wda.Client()
s = c.session()

num = 0;
purchaseNum = 0;

screenshot_backup_dir = 'screenshot_backups/'
if not os.path.isdir(screenshot_backup_dir):
    os.mkdir(screenshot_backup_dir)

def pull_screenshot():
    c.screenshot('1.png')

def binarizing(img,threshold):
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img

def save_debug_creenshot(ts, im):
	# draw = ImageDraw.Draw(im)
	# # 对debug图片加上详细的注释
	# draw.line((piece_x, piece_y) + (board_x, board_y), fill=2, width=3);
	# draw.line((piece_x, 0, piece_x, im.size[1]), fill=(255, 0, 0))
	# draw.line((0, piece_y, im.size[0], piece_y), fill=(255, 0, 0))
	# draw.line((board_x, 0, board_x, im.size[1]), fill=(0, 0, 255))
	# draw.line((0, board_y, im.size[0], board_y), fill=(0, 0, 255))
	# draw.ellipse((piece_x - 10, piece_y - 10, piece_x + 10, piece_y + 10), fill=(255, 0, 0))
	# draw.ellipse((board_x - 10, board_y - 10, board_x + 10, board_y + 10), fill=(0, 0, 255))
	# del draw
	# im.save('{}{}_d.png'.format(screenshot_backup_dir, ts))
	c.screenshot('{}{}.png'.format(screenshot_backup_dir, ts))
    # im.save('{}{}_d.png'.format(screenshot_backup_dir, ts))

# 战利品取消
def tapCancel():
    s.double_tap(550, 900);
# 开始战斗
def tapStart():
	s.tap(200, 1100);
# 再来一局
def tapReplay():
    s.tap(380, 450);
# 没能量时弹出的yes按钮
def tapEnergyShop():
    s.tap(241, 241);
# 副本列表的时候选择副本
def tapGiant():
	s.tap(100,1080);
# 
def tapEnergy():
	s.tap(350,380);
# 死亡的时候选择否不符合
def tapDeathContinue():
	s.tap(250,850);
# 购买成功后的确定按钮
def tapCancelPurchase():
	s.tap(290,230);
	time.sleep(0.5);
	s.tap(660,1100)

def handleAction(researchMsg,im):
	## 战斗完成后,继续游戏
	if(researchMsg.find('Replay') != -1 or researchMsg.find('Next Stage') != -1):
		print("战斗结束,再次开始");
		tapReplay();
		return True;
	## 战斗胜利,点击宝箱获得符文
	if(researchMsg.find('VICTOR') != -1 or researchMsg.find('RESULT') != -1):
		global  num;
		num	+=	1;
		msg = '战斗胜利,已完成战斗{}次'.format(num);
		print(msg);
		tapCancel();
		time.sleep(2);
		tapCancel();
		time.sleep(2);
		save_debug_creenshot(int(time.time()), im);
		tapCancel();
		return True;
	## 副本选择界面,点击参加战斗
	if(researchMsg.find('leader') != -1 or researchMsg.find('Leader') != -1):
		print("战斗再次开始");
		tapStart();
		return True;
	## 副本列表页面.选择当前选择栏最下方的副本
	if(researchMsg.find('Item Drop Info') != -1):
		print("跳出界面,重新回去");
		tapGiant();
		return True;
	## 能量耗尽.点击购买能量,开打商店
	if(researchMsg.find('Not enough Energy') != -1):
		print("没有足够能量了");
		tapEnergyShop();
		return True;
	## 打开能量购买商店后选择购买能量
	if(researchMsg.find('Shop') != -1):
		print("打开能量购买商店");
		tapEnergyShop();
		return True;
	## 死亡后不选择原地复活
	if(researchMsg.find('continue the battle') != -1):
		print("战斗死亡,不复活");
		tapDeathContinue();
		return True;
	## 战斗失败,点击界面,然后重新发起战斗
	if(researchMsg.find('DEFE') != -1):
		print("战斗失败.");
		tapReplay();
		time.sleep(1);
		tapReplay();
		return True;
	## 确定购买能量.
	if(researchMsg.find('Purchase with 30 Crystal') != -1):
		print("确定购买能量.");
		tapEnergyShop();
		return True;
	## 能量购买成功.关闭购买窗口
	if(researchMsg.find('Purchase successful') != -1):
		global  purchaseNum;
		purchaseNum +=1;
		msg = "购买能量成功.已购买{}此".format(purchaseNum);
		print(msg);
		tapCancelPurchase();
		return True;


	# print('没有执行任何操作');
	# save_debug_creenshot(int(time.time()), im);


def main():
	# s.tap(470, 900);
	# for x in range(200,500,30):
	# 	for j in range(200,800,30):
	# 		print(x,j);
	# 		s.tap(x,j);
    # while True:
    	pull_screenshot();
    	im = Image.open("./1.png");
    	img = im.convert('L');
    	img=binarizing(img,190);
    	# img.show();
    	data = pytesseract.image_to_string(img);
    	print(data)
    	# handleAction(data, im);
    	# time.sleep(1);
		    


if __name__ == '__main__':
    main()

