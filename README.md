# 魔灵召唤自动化脚本
## 游戏模式

> 这个脚本只是能帮你减少那些重复的行为.不能让你越级打怪.

## 原理说明

1. 打开游戏到副本界面

2. 用 ADB 工具获取当前手机截图，并用 ADB 将截图 pull 上来
```shell
adb shell screencap -p /sdcard/autojump.png
adb pull /sdcard/autojump.png .
```

3. 识别图片文字/进行图片比对,判断当前的环境.

4. 用 ADB 工具点击屏幕对应环境的位置

## 使用教程

相关软件工具安装，和使用步骤请参考 [Android 和 iOS 操作步骤](https://github.com/wangshub/wechat_jump_game/wiki/Android-%E5%92%8C-iOS-%E6%93%8D%E4%BD%9C%E6%AD%A5%E9%AA%A4)

## FAQ

> 配置流程

1. 需要先对截图的图片进行获取坐标点.

2. ipad等设备读取文字会出错(可能是我的设备问题),所以ipad采取的是图片比对的方式.需要预先把几个判断环境的图片预存.详细请看config目录下

3. 如果你对环境安装和操作步骤不熟悉？
    - [Android 和 iOS 操作步骤](https://github.com/wangshub/wechat_jump_game/wiki/Android-%E5%92%8C-iOS-%E6%93%8D%E4%BD%9C%E6%AD%A5%E9%AA%A4)


## 借鉴了这个文章,非常感谢![python 微信《跳一跳》辅助](https://github.com/wangshub/wechat_jump_game)