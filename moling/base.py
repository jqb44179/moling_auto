# coding: utf-8
# 魔灵辅助2.0 base gui样式模块
import os
import shutil
import time
import threading
# import atx
from tkinter import *
from  tkinter  import ttk

class Base(Frame):

	# 状态文字
	statusTips = '未开始';
	# 识别当前设备
	currentDevice = 'mobile';

	def __init__(self,startCommand,stopCommand,device="mobile"):
		Frame.__init__(self, master=None)
		self.master.title('魔灵召唤');
		self.master.geometry("500x300");
		self.currentDevice = device;
		# self.master.resizable(False, False);
		self.pack()
		self.__createWidgets(startCommand, stopCommand)

	# 创建布局
	def __createWidgets(self,startCommand, stopCommand):
		# 创建主框架
		mainFrame = Frame(self);
		mainFrame.pack();
		# 头部按钮区域
		topFrame = Frame(mainFrame);
		topFrame.pack(side=TOP);
		# 创建下拉框
		self.__craeteCombobox(topFrame);
		# 底部展示战斗日志以及统计
		bottomFrame = Frame(mainFrame);
		bottomFrame.pack(side=BOTTOM);
		# 左下展示战斗日志
		leftFrame = Frame(bottomFrame);
		leftFrame.pack(side=LEFT);
		# 右下展示统计
		rightFrame = Frame(bottomFrame);
		rightFrame.pack(side=RIGHT);

		self.alertTips = Label(topFrame, 
			text=self.statusTips,    # 标签的文字
			bg='green',     # 背景颜色
			font=('Arial', 12),     # 字体和字体大小
			width=15, height=2  # 标签长宽
		);
		self.alertTips.pack();
		# 创建按钮
		self.__createButton(topFrame,'开始',startCommand, LEFT);
		self.__createButton(topFrame,'暂停',stopCommand, LEFT);

		Label(leftFrame,text="战斗日志").pack();
		Label(rightFrame, text="战斗统计").pack();

		alertScroll = Scrollbar(bottomFrame);
		alertScroll.pack(side=RIGHT, fill=Y);

		self.alertText = Text(leftFrame,width=30,height=50)
		self.alertText.pack(side=BOTTOM, fill=Y)

		self.countText = Label(rightFrame,text="",justify='left');
		self.countText.pack();

	# 创建按钮
	def __createButton(self,frame, text, command, side=None):
		button = Button(frame, text=text, command=command);
		# if side != None:
		button.pack(side=side);

	# 脚本配置选择
	def __craeteCombobox(self,frame):
		Label(frame, text='选择脚本').pack();
		self.jiaoben = ttk.Combobox(frame, width=12, state='readonly');
		if self.currentDevice == 'mobile':
			self.jiaoben['values'] = ('地下城', '狗粮','塔','裂缝')
		else:
			self.jiaoben['values'] = ('巨人','龙','死亡','塔','裂缝', '狗粮');

		self.jiaoben.grid(column=1, row=0)
		self.jiaoben.current(0)
		self.jiaoben.pack();

	# 插入提示
	def insertMsg(self,msg):
		self.alertText.insert(END, msg+'\n');
		self.alertText.see(END)


