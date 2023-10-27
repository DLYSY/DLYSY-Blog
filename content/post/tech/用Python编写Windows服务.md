---
title: "用 Python 编写 Windows 服务" #标题
date: 2023-08-01T20:57:22+08:00 #创建时间
categories: 
- Windows
tags: 
- Python
- Windows
description: &description "本文说明了如何使用 PyWin32 编写基于 Python 的 Windows 服务。" #描述
summary: *description
weight: # 输入1可以顶置文章，用来给文章展示排序，不填就默认按时间排序
draft: false # 是否为草稿
---
# 前言

我的服务器是 Windows，有一些开机自启的常驻服务相比使用“任务计划程序”，“Windows 服务”更加容易管理，我就想将代码迁移到 Windows 服务，由于我只会 Python，就想能不能去找一个现成的 Windows 服务框架直接改改就能用。

但是找来找去，大多数的博客给的代码示例都只能简单的调用`pythonservice.exe`运行服务，不能打包为 exe 文件（很多博主说可以打包，估计他自己都没尝试过，实际打出来的包会报错）。这样在服务器部署时还需要安装 Python 不说，每一个独立的Python环境只能启动一个服务，需要使用 conda。造成了严重的资源浪费和环境污染。

于是我参考了一个
[Github 上的示例项目](https://github.com/HaroldMills/Python-Windows-Service-Example/tree/master)
自己撸了一个 Windows 服务框架。

# 前置工作

## 安装 Python

## PyWin32

安装使用：

```pwsh
pip install pywin32
```

~~不要使用conda，实测会导致产生“Windows无法启动服务”的错误。~~

现在3.11以上版本的conda可用

```pwsh
conda install -c conda-forge pywin32
```

但我不知道这到底是不是3.11修复的，至少现在的3.11+可以这么装了，如果你编写的程序无法正常使用，还是请尝试使用`pip`。

## pyinstaller（可选）

`pyinstaller`用于打包可执行文件，不是必须项。

安装使用：

```pwsh
pip install pyinstaller
```

或者

```pwsh
conda install -c conda-forge pyinstaller>=5.12
```

*当`Python`版本为3.11+时，使用`conda`安装时请指定版本大于5.12，`conda`默认会安装低版本的`pyinstaller`，使用3.11+版本的`Python`时会导致打包的可执行文件出现`找不到address库`的错误。*

# 编写服务

## 导入包

```python
import win32serviceutil
import win32service
import win32event
import servicemanager
from threading import Event
from sys import argv,exit
```

*对于`pywin32`相关的包，尽量直接使用`import`而不是`from ... import ...`的形式，否则可能出现无法启动服务的问题。*

## 通过重写类来实现服务

自行修改下面的类实现自己的功能

```python
class service_example(win32serviceutil.ServiceFramework):
    _svc_name_ = "my service" #服务名
    _svc_display_name_ = "my first service" #服务在windows系统中显示的名称
    _svc_description_ = "这是一个服务" #服务描述


    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.stop=Event()
    

    def __stop(self):
        '''
        服务停止时运行函数
        '''
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.stop.set()


    def SvcDoRun(self):
        '''
        服务运行时调用的函数
        '''
        while not self.stop.is_set():

            #<这里添加需要服务循环执行的代码/接口>

            self.stop.wait(300)#下次循环间隔，自行调整
    
    
    def SvcStop(self):
        '''
        在服务管理器中选择停止服务时自动调用该函数
        '''
        self.__stop()


    def SvcShutdown(self):
        '''
        Windows 系统关机时自动调用该函数
        '''
        self.__stop()
```

这里使用了`threading.Event()`来进行循环等待，不要使用`time.sleep()`，`sleep()`会造成忙等。比如`sleep(300)`那么程序将会强制挂起300s，如果你在此期间在服务管理器停止服务，那么程序依然会到300s挂起完成后再停止，`Event()`则没有这样的问题。

## 服务启动逻辑

服务启动的逻辑与一般程序不同，需要特定流程来启动。

### 打包为exe文件的情况

打包为exe文件的服务需要分三步启动

```python
if len(argv) == 1 and argv[0].endswith('.exe') and not argv[0].endswith(r'pythonservice.exe'):
    try:
        '''
        尝试以服务运行
        '''
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(service_example)
        servicemanager.StartServiceCtrlDispatcher()

    except pywintypes.error:
        '''
        如果收到pywintypes.error异常，则当前不是以服务形式运行
        '''
        #<这里添加打包为exe文件后，不使用服务而是直接运行的代码>
```

打包为 exe 文件的 `help` 命令支持（可选）

```python
elif len(argv) == 2 and argv[1] == 'help':
    print('''
        这是帮助    #自行修改 help 信息
    ''')
    exit()
```

### 不打包的情况

- 直接使用 `python xxx.py` 执行脚本文件

```python
elif len(argv) == 1 and argv[0].endswith('.py'):
    #<这里添加以python.exe xxx.py形式运行时的代码>
```

- 使用 `python xxx.py install` 安装服务时的服务启动逻辑：

```python
#如果你的Python<=3.10
elif argv[0].endswith('pythonservice.exe') and __name__=="__main__":
    win32serviceutil.HandleCommandLine(service_example)

#如果Python>=3.11
else:
    win32serviceutil.HandleCommandLine(service_example)
```

**请注意Python的版本和相应的代码，否则也会无法正常运行。**

# 安装服务

## 打包为可执行文件

- 打包

```pwsh
pyinstaller --hidden-import=win32timezone xxx.py -F --clean
```

- 安装（需要管理员权限）

```pwsh
xxx.exe install
```

## 直接调用Python运行

```pwsh
python xxx.py install
```

无论使用哪种方法，现在都可以在服务管理器中看到该服务了。至于如何使用`sc.exe`或 GUI 管理服务，这都已经超出本文范畴，不再赘述。

# 后记

Github上有
[我的DDNS项目](https://github.com/DLYSY/CloudFlareDDNS-WindowsService-Python)
，就是基于该框架所构建的，并且在我的服务器上持续运行了一年，状态良好，可以作为你编写类似服务的一个参考。不过，由于一些原因（主要是 Windows 对 UDP 端口转发的糟糕支持和 IIS 反向代理的各种奇葩小问题），现在我已将该服务器下的工作负载迁移至 OpenSUSE ，未来对于 PyWin32 的相关学习不会像写这篇博客时那么积极了。

在我的项目中我使用了 logging 包以便我能够更好的追踪服务的运行状态，但这也不属于本文应有的范畴，故不在此讨论。