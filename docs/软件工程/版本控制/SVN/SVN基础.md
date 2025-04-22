---
title: SVN基础
tags:
  - svn
update: 2025-04-06
---
## SVN简介
Subversion(SVN) 是一个开源的集中式版本控制系統, 也就是说 Subversion 管理着随时间改变的数据。  这些数据放置在一个中央资料档案库(repository) 中。 这个档案库很像一个普通的文件服务器, 不过它会记住每一次文件的变动。  这样你就可以把档案恢复到旧的版本, 或是浏览文件的变动历史。
## SVN特点
* 统一版本号：Subversion下，任何一次提交都会对所有文件增加到同一个新版本号，即使是提交并不涉及的文件，版本号相同的文件构成软件的一个版本。
* 原子提交：一次提交不管是单个还是多个文件，都是作为一个整体提交的。在这当中发生的意外例如传输中断，不会引起数据库的不完整和数据损坏。
* 多级管理系统：
  * 超级管理员：对所有配置库具有完全权限
  * 目录管理员：对指定的目录/SVN库进行权限管理
  * 普通用户：可以查看用户名、查看权限设置、修改自己的密码。
* 自动合并：源代码以行为单位。
## 客户端
### checkout
* 通过`svn://192.168.0.1(具体的svn服务器地址)/CurryCoder01 --username=user01`，如下所示：
```bash
svn checkout svn://192.168.0.1/CurryCoder01 --username=user01
# drwxr-xr-x 6 root root  ./
# drwxr-xr-x 3 root root  ../
# drwxr-xr-x 2 root root  branches/
# drwxr-xr-x 4 root root  .svn/
# drwxr-xr-x 2 root root  tags/
# drwxr-xr-x 2 root root  trunk/
```
### update
在推送前使用`svn update`合并之前其他人的提交
再使用`svn commit -m ""`提交自己的修改
## 服务端
### 创建版本库
* 创建版本库目录
```bash
sudo mkdir /opt/svn
```
* 使用SVN命令创建版本库
```bash
sudo svnadmin create /opt/svn/CurryCoder
# drwxr-xr-x 6 root root  ./
# drwxr-xr-x 4 root root  ../
# drwxr-xr-x 2 root root  conf/
# drwxr-sr-x 6 root root  db/
# -r--r--r-- 1 root root  format
# drwxr-xr-x 2 root root  hooks/
# drwxr-xr-x 2 root root  locks/
# -rw-r--r-- 1 root root  README.txt
```
* 使用svnserve启动服务
```bash
svnserve -d -r 目录 --listen-port 端口号     # 默认3690端口
```
  * 单库svnserve方式：一个svnserve只能为一个版本库工作
```bash
svnserve -d -r /opt/svn/CurryCoder
```
  * 多库svnserve方式：指定到版本的上级目录，一个svnserve可以为多个版本库工作。
```bash
svnserve -d -r /opt/svn
```
### 配置参数
* 配置参数
* 服务配置：**`/opt/svn/CurryCoder/conf/svnserve.conf`
```
[general]
anon-access = none     # 控制非授权用户访问版本库的权限
auth-access = write   # 控制授权用户访问版本库的权限。
password-db = /home/svn/passwd
authz-db = /home/svn/authz # 指定权限配置文件名，通过该文件可以实现以路径为基础的访问控制。除非指定绝对路径，否则文件位置为相对conf目录的相对路径。默认值：authzrealm = tiku # 指定版本库的认证域，即在登录时提示的认证域名称。
```
* 用户名口令文件passwd：用户名口令文件由svnserve.conf的配置项password-db指定，默认为conf目录中的passwd。该文件仅由一个[users]配置段组成:
```bash
[users]  
admin = admin # <用户名> = <口令>
CurryCoder = 123456
```
  * 权限配置文件：由svnserve.conf的配置项authz-db指定，默认为conf目录中的authz。该配置文件由一个[groups]配置段和若干个版本库路径权限段组成：
```bash
[groups]   # <用户组> = <用户列表>
g_admin = admin,CurryCoder
[admintools:/] # [<版本库名>:<路径>]
@g_admin = rw
* =
[test:/home/CurryCoder]
CurryCoder = rw
* = r
```