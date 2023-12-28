---
title: "使用RD网关访问内网远程桌面" #标题
date: 2023-12-01T15:04:45+08:00 #创建时间
categories: 
- Windows
tags: 
- Windows
- RDP
description: &description "" #描述
summary: *description
weight: # 输入1可以顶置文章，用来给文章展示排序，不填就默认按时间排序
draft: true # 是否为草稿
---
# 前言

RD 网关可以使外网能够访问内网的远程桌面，对于内网 Windows 机器较多的环境非常好用。相比使用PPTP、L2TP，RD 网关基于 SSL，可以提供更好的安全性。而相比 IKEv2 ，RD网关的部署更加简单。

全网关于如何部署和使用 RD 网关的文章很少，且大多基于 Windows Server 2008，比较古早且存在细节丢失、图片失效等问题，几乎没法用作参考。

我在摸索了一段时间后成功在内网部署了 RD 网关，与

# 准备工作

## 安装好 Windows