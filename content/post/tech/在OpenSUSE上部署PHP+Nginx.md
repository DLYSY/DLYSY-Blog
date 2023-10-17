---
title: "在 OpenSUSE 上部署 PHP+Nginx" #标题
date: 2023-10-01T15:04:45+08:00 #创建时间
author: DLYSY #作者
categories: 
- Linux
tags: 
- Linux
- Nginx
- PHP
description: "本文以 OpenSUSE Tumbleweed 为例主要解决如何在使用 AppArmor 的 Linux 发行版上使用 PHP-FPM 的问题" #描述
weight: # 输入1可以顶置文章，用来给文章展示排序，不填就默认按时间排序
draft: true # 是否为草稿
comments: true #是否展示评论
showToc: true # 显示目录
TocOpen: true # 自动展开目录
hidemeta: false # 是否隐藏文章的元信息，如发布日期、作者等
showbreadcrumbs: true #顶部显示当前路径
---
**！！！注意！！！**

**1. 本文写于2023年10月，当前 PHP 版本为8.2.11，Nginx 版本为1.25.2，随着软件的更新，本文所说明的方法可能会在某日失效。**

**2. **

**3. 由于各人环境不同，我不保证我的方法在你的环境上一定完全不会出问题。遇到问题请善用搜索引擎，我不一定会遇到和你一样的问题，也不一定知道解决方法。**

# 背景

Windows+IIS 的组合我用了两年，觉得GUI简单直观，对 CGI（主要是PHP）的支持也非常好，也对于我这样不需要太多复杂配置的新手非常友好。但在使用两年后，我逐渐对 HTTP 服务器有了更高的要求，包括但不限于反向代理的 Header 传递、反向代理的缓存调整、文件上传的大小限制等等。IIS 功能太过复杂，相关资料又特别少，有些配置死活搞不对，使我对放弃 IIS 有了一些想法。

不过，即使 IIS 有一些小问题，我也不想完全取代他，毕竟 GUI 配置确实方便，很多时候不需要查资料，即使望文生义也可以大致明白一些功能该如何使用。但就在前不久，我忽然有了 UDP 端口转发的需求，由于 Windows 系统组件`netsh.exe`不支持 UDP 转发，这让我想到 Nginx，然而 Nginx on Windows 也不能使用 UDP 的端口转发，这就迫使我必须转向 Linux+Nginx 结构。

最近将我的绝大多数前端服务器迁移到了 OpenSUSE+Nginx；

# 准备工作