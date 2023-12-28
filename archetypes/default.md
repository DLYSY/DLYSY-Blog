---
title: "{{ replace .File.ContentBaseName "-" " " | title }}"
date: {{ .Date }}
categories: 
- 分类
tags: 
- 标签1
- 标签2
description: &description "描述"
summary: *description
weight: # 输入1可以顶置文章，用来给文章展示排序，不填就默认按时间排序
draft: true # 是否为草稿
---
