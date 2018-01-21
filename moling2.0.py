# coding: utf-8
# 魔灵辅助2.0
import os
import time
import wda
from PIL import Image as Images, ImageDraw
import pytesseract
import json
import threading
# import atx
import moling.base as BaseApp

# d = atx.connect()
c = wda.Client()
s = c.session()

screenshot_backup_dir = 'screenshot_backups/'
if not os.path.isdir(screenshot_backup_dir):
    os.mkdir(screenshot_backup_dir)
# 截屏
def pull_screenshot():
    c.screenshot('1.png')
# 格式化图片
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
# 保存收货的页面
def save_debug_creenshot(ts, im):
	c.screenshot('{}{}.png'.format(screenshot_backup_dir, ts))

class App(BaseApp.Base):
	# 执行状态
	status = False;
	# 线程对象
	threadObject = '';
	# 状态文字
	statusTips = '未开始';
	# 选中的脚本
	jiaoben = '';
	# 配置脚本
	config = '';
	# 战斗次数
	num = 0;
	# 死亡次数
	deathNum = 0;
	# 购买能量次数
	buyNum = 0;
	# 是否调试
	debug = False;


	def __init__(self):
		BaseApp.Base.__init__(self, self.start, self.stop)

		# 开始战斗
	def start(self):
		if self.status == True :
			return True;
		self.status = True;
		self.alertTips.config(text='运行ing')
		self.threadObject = threading.Thread(target=self.__handle, name='LoopThread')
		self.threadObject.start();

	# 暂停
	def stop(self):
		self.status = False;
		self.alertTips.config(text='暂停ing') 


	# 执行开始
	def __handle(self):
		currentAction = self.jiaoben.get();
		fileName = 'ta.json';
		if(currentAction == '狗粮'):
			fileName = 'gouliang.json';
		
		if currentAction == '地下城':
			fileName = 'dixiacheng.json';

		if currentAction == '裂缝':
			fileName = 'liefeng.json';

		with open('./config/'+fileName, 'r') as f:
			self.config = json.load(f)

		while self.status:
			pull_screenshot();
			im = Images.open("./1.png");
			img = im.convert('L');
			img=binarizing(img,118);
			data = pytesseract.image_to_string(img);
			# self.insertMsg(data)
			data = data.lower();
			self.__handleAction(data, im);
			time.sleep(1);
	# 动作开始
	def __handleAction(self, researchMsg, im):
		print(researchMsg);
		for key in self.config:
			if researchMsg.find(self.config[key]['researchTitle']) != -1 :
				msg = self.config[key]['returnMsg']
				# 当处于胜利的时候.需要点击出宝箱,后再点击取消胜利品弹框
				if key == 'victory':
					self.num +=	1;
					msg = self.config[key]['returnMsg'].format(self.num);
					# 第一次点击,出现宝箱
					s.tap(self.config[key]['coordinate'][0], self.config[key]['coordinate'][1]);
					time.sleep(2);
					# 第二次点击,取消,以防时间消耗.最后继续点击多一次
					s.tap(self.config[key]['coordinate'][0], self.config[key]['coordinate'][1]);
					time.sleep(1);
					save_debug_creenshot(int(time.time()), im);
					# s.tap(self.config[key]['coordinate'][0], self.config[key]['coordinate'][1]);
				# 战斗死亡.需要点击多一次显示
				if key == 'defeat':
					s.tap(self.config[key]['coordinate'][0], self.config[key]['coordinate'][1]);
					time.sleep(1);
				# 购买完能量.需要关闭购买成功提示,然后关闭商店窗口
				if key == 'closeBuyAndShop':
					self.buyNum +=1;
					msg = self.config[key]['returnMsg'].format(self.buyNum);
					# 发送消息提醒
					self.insertMsg(msg);
					# 公用点击
					s.tap(self.config[key]['coordinate'][0][0], self.config[key]['coordinate'][0][1]);
					time.sleep(0.5);
					s.tap(self.config[key]['coordinate'][1][0], self.config[key]['coordinate'][1][1]);
					return True;
				# 战斗死亡,增加死亡记录
				if key == 'death' or key == 'defeat':
					self.deathNum += 1;

				# 发送消息提醒
				self.insertMsg(msg);
				# 公用点击
				s.tap(self.config[key]['coordinate'][0], self.config[key]['coordinate'][1]);
				countMsg = "战斗{}次\n死亡{}次\n购买能量{}次\n".format(self.num,self.deathNum, self.buyNum);
				self.countText.config(text=countMsg)
				return True;

	def open(self):
		BaseApp.Base.mainloop(self);


app = App();
app.open();

