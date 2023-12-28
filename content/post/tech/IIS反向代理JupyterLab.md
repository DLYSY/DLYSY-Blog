---
title: "IIS 反向代理 JupyterLab"
date: 2023-05-01 
draft: false
tags: 
- Windows
- IIS
- Jupyter
description: &description "以 JupyterLab 为例，就此说明如何在 IIS 中反向代理 WebSocket。"
summary: *description
categories: 
- Windows
---
# 前言

全网关于 JupyterLab + Nginx 的文章不少，不过我个人的服务器是 Windows Server。虽然 Nginx 在 Windows 上也能用，但在 Windows 上 IIS 毕竟与系统集成，还有好用的 GUI（前提是没有用 Server Core），我就想能不能用 IIS 做反向代理。

本文简单的描述了我搭建 IIS 反向代理的过程，不过由于我在个人服务器上已经配置好了，所以写本文时全程在虚拟机上模拟。

# 前置工作

## 安装并配置好 Jupyter

安装和配置 Jupyter 不属于本文的范畴，这里不再做相关说明。

需要在 Jupyter 配置文件中做如下设置：

`c.ServerApp.allow_origin = '*'`

*注：这是为反向代理可以运行而进行的必要设置，其他设置如 password、serverip 等请根据需要配置。具体请参考
[JupyterServer官方文档](https://jupyter-server.readthedocs.io/en/stable/operators/public-server.html)*。

我使用 JupyterLab 作为演示，理论上 Jupyter 全系列服务通用，包括 Lab、Notebook 和 Server（Hub 没用过不知道行不行）。

## 安装好 Windows Server

安装选项请使用 Desktop Experience，除非你可以熟练使用 PowerShell。

演示使用 Windows Server 2022 Datacenter，Standard 版本只是 Hyper-V 做了一些限制，和 Datacenter 没什么区别。

请使用 Windows Server 2016 及以上版本，因为目前只有 IIS 10 支持 WebSocket 协议，而 Windows Server 2016 及以后的版本才支持 IIS 10。

*注：虽然 IIS 8.5 及以前版本也可以通过自定义 URL 重写规则的方式实现 WebSocket 反向代理，但是我既没有测试过，也不会去测试。Windows Server 2012 是一个已经发布了十多年的操作系统，专门去研究它是没有意义的。*

虽然我不推荐，但是 Windows 10/11 理论上也可以用。

我默认你对 Windows Server 和 IIS 有一定了解，至少应该会修改站点的路径、绑定和权限啥的，不至于出问题不知所措。

## 配置好网络

确保 IIS 主机和 Jupyter 主机可以通信（可以通过ping检查）。

打开防火墙相关端口（如 Jupyter 默认8888）或关闭防火墙（不建议长时间关闭防火墙，这样做很危险）。

在本文中，IIS 服务器的 IP：192.168.56.6，Jupyter 服务器的 IP：192.168.56.5。

# 准备工作

## 安装 IIS

在服务器管理器的右上角选择“管理” $\to$ “添加角色和功能”

![3.1-1](https://dlysy.github.io/PictureBeds/DLYSYBlog/tech/IIS反向代理JupyterLab/3.1-1.PNG)

然后一直选择下一步，直到“选择服务器角色”；如图选择“web服务器(IIS)”

![3.1-2](https://dlysy.github.io/PictureBeds/DLYSYBlog/tech/IIS反向代理JupyterLab/3.1-2.PNG)

在“角色服务”中选择“WebSocket协议”**（这一步很重要，选漏了 IIS 将无法代理 WebSocket ，无法正常使用）**，其他功能不是必须，可以按需选择。

![3.1-3](https://dlysy.github.io/PictureBeds/DLYSYBlog/tech/IIS反向代理JupyterLab/3.1-3.PNG)

## 安装[ARR](https://www.iis.net/downloads/microsoft/application-request-routing)和[URL重写模块](https://www.iis.net/downloads/microsoft/url-rewrite)

请等待上一步 IIS 安装完成再进行这步，防止出错

安装过程略，一路下一步即可，没什么需要注意的。

# 配置 IIS 反向代理

打开 IIS 管理器，在左侧导航栏选择你的服务器$\to $在右侧双击“Application Request Routing Cache”打开

![4-1](https://dlysy.github.io/PictureBeds/DLYSYBlog/tech/IIS反向代理JupyterLab/4-1.PNG)

然后在右边选择“Server Proxy Settings...”

![4-2](https://dlysy.github.io/PictureBeds/DLYSYBlog/tech/IIS反向代理JupyterLab/4-2.PNG)

接下来把“Enable Proxy”打上勾，然后在右边选择应用

![4-3](https://dlysy.github.io/PictureBeds/DLYSYBlog/tech/IIS反向代理JupyterLab/4-3.PNG)

在右侧导航栏选择你的站点，然后双击进入“URL重写”（我这里用 IIS 默认创建的站点做演示）

![4-4](https://dlysy.github.io/PictureBeds/DLYSYBlog/tech/IIS反向代理JupyterLab/4-4.PNG)

点击“添加规则”$\to$选择“反向代理”$\to$“确定”

![4-5](https://dlysy.github.io/PictureBeds/DLYSYBlog/tech/IIS反向代理JupyterLab/4-5.PNG)

接下来配置反向代理，在顶上的文本框输入你 Jupyter 服务器的地址或域名或主机名+端口。**然后请务必打勾“启用SSL卸载”！无论你的反向代理目标是否使用 SSL！**

*注：如果很清楚你在干什么 ~~（那你就不该来看这篇教程了（误））~~，则可以选择不启用 SSL 卸载，但如果你不知道是否需要启用，请不要随意把勾去掉。*

然后点击“确定”。

![4-6](https://dlysy.github.io/PictureBeds/DLYSYBlog/tech/IIS反向代理JupyterLab/4-6.PNG)

如果你在 Jupyter 上配置了 SSL 则还有下面两步：

1. 双击打开你刚刚创建的规则

![4-7](https://dlysy.github.io/PictureBeds/DLYSYBlog/tech/IIS反向代理JupyterLab/4-7.PNG)

2. 将下面的 http 改成 https，最后在右边点击“应用”

*注：如果在 Jupyter 上配置了 SSL，必须确保 IIS 主机信任 Jupyter 上 SSL 的 CA（SSL 主机名不对没关系，关键是 CA 要信任），否则将会发生502（好像是502.3）的服务器错误。*

![4-8](https://dlysy.github.io/PictureBeds/DLYSYBlog/tech/IIS反向代理JupyterLab/4-8.PNG)

配置完成之后访问反向代理的地址就可以看到界面了

![4-9](https://dlysy.github.io/PictureBeds/DLYSYBlog/tech/IIS反向代理JupyterLab/4-9.PNG)

至此反向代理配置完成

# 后记

## 关于 IIS 使用 SSL

个人使用 Certify The Web 申请 Let's Encrypt SSL 证书。

## 关于将Jupyter作为守护进程运行

说到后台常驻应用，我很喜欢将它包装为一个系统服务的形式，一遍进行统一管理。

Linux 可以包装为 systemd 服务，Windows 可以调用 win32api 进行封装。

不过这些都不是本文应该讨论的范畴，在此不再作额外说明。