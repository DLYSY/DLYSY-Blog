---
title: "在 OpenSUSE 上部署 PHP+Nginx" #标题
date: 2023-10-01T15:04:45+08:00 #创建时间
categories: 
- Linux
tags: 
- Linux
- Nginx
- PHP
description: &description "以 OpenSUSE Tumbleweed 为例主要解决如何在使用 AppArmor 的 Linux 发行版上使用 PHP FPM 的问题。" #描述
summary: *description
weight: # 输入1可以顶置文章，用来给文章展示排序，不填就默认按时间排序
draft: true # 是否为草稿
---
# 背景

Windows+IIS 的组合我用了两年，觉得GUI简单直观，对 CGI（主要是PHP）的支持也非常好，也对于我这样不需要太多复杂配置的新手非常友好。但在使用两年后，我逐渐对 HTTP 服务器有了更高的要求，包括但不限于反向代理的 Header 传递、反向代理的缓存调整、文件上传的大小限制等等。IIS 功能太过复杂，相关资料又特别少，有些配置死活搞不对，使我对放弃 IIS 有了一些想法。

不过，即使 IIS 有一些小问题，我也不想完全取代他，毕竟 GUI 配置确实方便，很多时候不需要查资料，即使望文生义也可以大致明白一些功能该如何使用。但就在前不久，我忽然有了 UDP 端口转发的需求，由于 Windows 系统组件`netsh.exe`不支持 UDP 转发，这让我想到 Nginx，然而 Nginx on Windows 也不能使用 UDP 的端口转发，这就迫使我必须转向 Linux+Nginx 结构。

最近将我的绝大多数前端服务器迁移到了 OpenSUSE+Nginx；

# 准备工作

## Linux 发行版

安装好 OpenSUSE ,其他使用 AppArmor 的发行版（如 Ubuntu）应该在之后的操作上原理相同，但 OpenSUSE 可以使用 YaST，我在本文将会全程使用 KDE + YaST 进行操作，纯命令行操作 AppArmor 不在本文讨论范畴内。

Linux 安装方法和过程本文也不作详细说明。

## Nginx & PHP FPM

```bash
sudo zypper install nginx
sudo zypper install php8
sudo zypper install php8-fpm
```

## PHP 应用 （以 phpMyAdmin 为例）

我这里使用`phpMyAdmin`做示例，当然，你也可以用其他 PHP 应用，原理相同。

可以直接使用`zypper`安装：

```bash
sudo zypper install phpMyAdmin
```

`zypper`会附带安装`Apache2`，但本文的内容是`Nginx`，所以自动安装的`Apache2`不用管它，不用`systemctl`启动就OK。

或者参考
[phpMyAdmin的文档](https://docs.phpmyadmin.net/zh_CN/latest/)
进行手动下载安装，这里不在进行说明。

# 
# 关闭 AppArmor
# 在 AppArmor中进行授权