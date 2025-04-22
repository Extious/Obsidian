---
title: Linux会话
tags:
  - linux
update: 2025-04-05
---
对于linux的终端内会话的管理，本文章介绍nohup和tmux的使用
## nohup
### 介绍
nohup 英文全称 no hang up（不挂起），用于在系统后台不挂断地运行命令，退出终端不会影响程序的运行。nohup 命令，在默认情况下（非重定向时），会输出一个名叫 nohup.out 的文件到当前目录下，如果当前目录的 nohup.out 文件不可写，输出重定向到 $HOME/nohup.out 文件中。
### 语法使用
```bash
nohup command [arg...] [ &]
```
1. command：要执行的命令。
2. arg：一些参数，可以指定输出文件。
3.  &amp;：让命令在后台执行，终端退出后命令仍旧执行。
常见用法：
```bash
nohup [mycommamd] > nohup_output.log 2>&1 &  
```
如果忽略输出：
```bash
nohup [mycommamd] > /dev/null 2>&1 & 
```
输入nohup命令之后会返回任务id和进程pid
通过以下命令进行查找：
```bash
ps -aux | grep [mycommand.sh]  
pgrep -a [mycommand.sh]  
jobs -l 
```
通过以下命令终止进程：
```bash
kill -9 [pid]
```
## tmux
命令行的典型使用方式是，打开一个终端窗口（terminal window，以下简称&quot;窗口"），在里面输入命令。用户与计算机的这种临时的交互，称为一次"**会话**"（session）。Tmux 就是会话与窗口的&quot;解绑&quot;工具，将它们彻底分离。和screen的功能比较类似，但是tmux的功能更强大：
```bash
# tmux的层次：
-session1
---window1
------subwindow1
------subwindow2
------subwindow3
------subwindow4
---window2
-session2
---window3
---window4
```
### 常用方法
```bash
# 开启新session
tmux
# 开启新session并命名
tmux new -s my_session
# 显示所有session
tmux ls
# 使用session编号接入
tmux attach -t 0
# 使用session名称接入
tmux attach -t <session-name>
tmux a -t name #简写
# 使用session编号kill
tmux kill-session -t 0
# 使用session名称kill
tmux kill-session -t <session-name>
# 使用session编号切换
tmux switch -t 0
# 使用session名称切换
tmux switch -t <session-name>
# 重命名会话
tmux rename-session -t 0 <new-name>
# 选择需要跳转的session会话
Ctrl + b s
# 重命名当前会话
Ctrl + b $
# 断开当前session
Ctrl + b d
# 在当前session中多加一个window
Ctrl + b c
# 在一个session中的多个window中作出选择
Ctrl + b w
# 关闭当前session中的当前window
Ctrl + b x
# 进入tmux翻屏模式, 实现上下翻页
Ctrl + b [  
### 进入翻屏模式后PgUp PgDn 实现上下翻页（mac可以用fn + ↑ ↓实现上下翻页）
### q 退出翻屏模式
#############
# 其他常用快捷键
##############
Ctrl + b ！  #关闭一个session中所有窗口
Ctrl + b % #将当前窗口分成左右两分
Ctrl + b " #将当前窗口分成上下两分
Ctrl + b 方向键 #让光标在不同的窗口中跳转 
Ctrl + b 方向键 #按住C+b不放，同时按住方向键，可以调节光标所在窗口的大小 
```
### 结对编程
通过ssh连上服务器之后使用tmux进入同一个session可以共享屏幕和操作，非常适合结对编程。
### 参考链接
[Tmux使用教程](https://www.ruanyifeng.com/blog/2019/10/tmux.html)