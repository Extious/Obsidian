---
title: Git基础
tags:
  - git
update: 2025-04-06
---
## 安装git
网址[https://git-scm.com/downloads](https://git-scm.com/downloads)上安装
安装之后要设置自身全局配置
```bash
git config --global user.name "Your Name"
git config --global user.email "email@example.com"
```
## 创建版本库
初始化一个git仓库
```bash
git init
```
添加文件到git仓库
```bash
git add <file>
```
## 分支管理
可视化教程参考[git分支管理教程](https://learngitbranching.js.org/?locale=zh_CN)
## 本地
### status
查看工作区状态
```bash
git status
```
### commit
```bash
# git commit 命令会在本地新生成一个节点
git commit
# 使用amend参数可以修改最近的提交
git commit --amend
```
### branch
分支相当于节点指针
```bash
# 生成新分支
git branch newbranch
# 切换到另一个分支
# 也可以使用 git checkout newbranch
# -b可以缺省新建分支
git switch newbranch 
# 可以使用-f参数强制修改branch指向的节点
git branch -f main HEAD~4
# 可以使用-u参数设置本地分支和远程分支的跟踪
```
### merge
```bash
# 合并其他分支
git merge newbranch
```
### rebase
```bash
# 变基到其他分支上完成合并
git rebase newbranch
# -i 可以互动选取变基时可选的提交节点,由此可以实现cherry-pick效果
git rebase HEAD~4
```
### checkout
checkout可以让你的工作区在各个结点之间自由移动
```bash
# 使用哈希值
git checkout commit_id
# 使用分支名
git checkout newbranch
# 使用相对引用
git checkout main^ # 或者git checkout main~1
```
### reset和revert
* reset:可以撤销节点回到历史上任何一个节点,撤销后的节点相当于不存在
* revert:可以撤销某个提交,产生一个新的节点
```bash
git reset commit_id
git revert commit_id
```
### cherry-pick
cherry-pick可以将某些提交放在当前节点的下面
```bash
git cherry-pick commit_id_1 commit_id_2
```
### tag
对于一些特殊的提交节点(特定的版本)可以使用tag打标签
```bash
git tag v0 commit_id	# commit_id可选,默认为HEAD节点
```
### describe
使用describe命名可以查看到当前或指定节点到最近tag的距离
```bash
# 下述命令输出:v0_2_commit_id
# v0为最近tag;2为当前节点到最近tag的距离;commit_id为当前的提交节点hash
# 可以跟指定节点替代当前节点:git describe main
git describe 
```
## 远程
远程仓库相当于本地仓库的拷贝,在本地远程分支的名字是`<remote name>/<branch name>`,`<remote name>`默认为origin
### clone
```bash
# 使用clone可以将远程的代码拷贝到本地
git clone url	# url使用http://协议或这git://协议
```
### fetch
fetch命令用于从远程仓库获取数据,但是并没有修改本地文件
```bash
# 下述命令完成了仅有的两个步骤:
# 	1. 从远程仓库下载本地仓库中缺失的提交记录
# 	2. 更新远程分支指针
# 如果没有参数,更新所有远程分支
git fetch
# 不在乎当前分支,指定fetch分支(本地分支和远程分支相同,但是本地分支位置不变,只是origin/main改变)
git fetch origin main
# 当本地分支和远程分支不同时也可以指定fetch分支,但是本地分支不能是当前分支
git fetch origin <origin>:<local>
# 当origin参数位置为空时在本地创建一个分支
git fetch origin :<local>
```
### pull
pull相当于将fetch和merge/rebase两个步骤合为一个步骤
```bash
# 默认pull是先fetch再merge,可以使用rebase参数做修改
git pull
git pull --rebase
# git pull的其他参数都是fetch+merge形式,其中merge是在当前分支下merge
```
### push
push是将本地的提交更新到远程仓库中
```bash
git push
# 不在乎当前分支,指定push分支(本地分支和远程分支相同)
git push origin main
# 当本地分支和远程分支不同时也可以指定push分支
git push origin <source>:<destination>
# 当source为空时会删除远程分支
git push origin :<destination>
```
### remote tracking
使用clone之后本地分支和远程分支默认建立连接,使用git push和git pull自动指向对应的分支
使用下述命令可以建立连接
```bash
git checkout -b side origin/main	# 本地side和origin/main建立连接
```
修改最近一次提交git commit --amend
```bash
git commit --amend
```
## 时光穿梭
### 版本回退
查看工作区状态
```bash
git status
```
查看修改的内容
```bash
git diff
```
查看提交历史，可以得知提交ID，即commit_id
```bash
git log
```
#### reset
HEAD指向的是当前的版本，使用命令指向历史的版本
```bash
git reset --hard commit_id
#根据commit_id回退到指定版本
git reset HEAD^
#将版本库回退一个版本，一个^一个版本
git reset HEAD~n
#将版本库回退n个版本
```
reset命令中有三个参数
* soft：软回退表示将本地版本库的头指针重置到指定的版本，且这次提交后的所有变更移动到暂存区
* 默认mixed：将本地版本库的头指针重置到指定的版本，且重置暂存区，所有变更移动到工作区
* hard：将本地版本库的头指针重置到指定的版本，重置暂存区和工作区
> 此外：git reset HEAD filename 回退文件，将文件从暂存区回退到工作区，不能使用参数
#### reflog
重返未来则用命令
```bash
git reflog
#查看所有分支的操作记录之后使用git reset --hard commit_id命令回到原来的版本
```
### Git stash用法
Git stash用于将未提交的修改保存起来，用于后续恢复当前工作目录
```bash
git stash save "stash_name"
#给每一个stash加一个message，用于记录版本
git stash pop
#or git stash apply
#恢复最新缓存的工作目录（第一个），并删除缓存堆栈中的哪个stash（pop删除但是apply不删除）
git stash list
#查看所有的stash，在使用git stash之前使用，默认是第一个
git stash drop
#移除最新的stash，后边也可以跟指定的stash的名字
```
### 工作区和暂存区
工作区git add到暂存区，然后git commit到本地仓库
### 管理修改
只有git add之后才能git commit到本地仓库
查看工作区和版本库里最新版本的区别：
```bash
git diff HEAD --<file>
```
### 撤销修改
场景1：当改乱工作区的文件内容后，要丢弃修改
```bash
git checkout --file
```
场景2：如果已经添加到了暂存区要丢弃修改，先：
```bash
git reset HEAD <file>
```
在按场景1操作。
场景3：提交到了版本库，参考版本回退
### 删除文件
先rm file删除工作区文件，在使用命令删除本地仓库文件
```bash
git rm file
git commit -m "remove file"
```
如果删错了，版本库中还有，可以一键还原
```bash
git checkout -- file
#从版本库中拉取
git checkout --hard HEAD
#从版本库中拉取，撤销所有的更改
```
git checkout其实是用版本库里的版本替代工作区的版本，无论修改还是删除都可以一键还原
## 远程仓库
### 添加远程库
首先创建ssh key
```bash
ssh-keygen -t rsa -C "youremail@example"
```
在用户主目录里找到.ssh目录，id_rsa.pub是公钥，将里边的ssh复制，在GitHub上打开Account settings的“SSH Key“页面
然后将本地库和远程库关联
```bash
git remote add origin git@server-name:path/repo-name.git
```
上述命令中origin是指定的远程库名称
然后是将本地库的代码推送到远程库
```bash
git push -u origin master
```
第一次要有-u,上述的master为分支的名称，首次会发生警告
查看远程库信息
```bash
git remote
```
### 从远端库克隆
与远程库建立关联后可以直接git clone
```bash
git clone git@server-name:path/repo-name.git
```
也可以使用https协议
如果要克隆gitlab中的项目，要输入username和password登录，GIT_TERMINAL_PROMPT控制是否会出现登录界面
## 分支管理
### Feature分支
切回dev分支
```bash
git switch dev
```
**强行删除分支：**
```bash
git branch -D feature-vulcan
```
### 多人协作
查看远程库信息
```bash
git remote
git remote -v
```
#### 推送分支
```bash
git push <远程主机名> <本地分支名>:<远程分支名>
git push origin master
#将本地的master分支推送到origin主机的master分支，如果master不存在则会被新建
git push origin :master
#等同于git push origin --delete master，表示删除指定的远程分支
git push origin
#如果当前分支与远程分支存在追踪关系，则本地分支和远程分支都可省略
git push
#如果当前分支和多个主机存在追踪关系，可以使用使用git push -u origin master指定一个默认主机，之后就可以直接使用git push
```
#### 抓取分支
```bash
git clone git@github.com:username/reporstoryname.git
```
注意clone的时候只能clone到main这一个分支
clone其他分支时
```bash
git checkout -b dev origin/dev
```
当与他人的合并产生冲突时先git pull
```bash
git pull <远程主机名> <远程分支名>:<本地分支名>
git pull origin master:test
#将远程的master分支和本地的test分支合并
git pull origin master
#默认和当前分支合并
```
解决冲突后再推送
如果git pull还是失败，那么因为本地dev和远程的origin/dev未建立链接，应设置链接
```bash
git branch --set-upstream-to=origin/dev dev
git pull
```
rebase操作可以把本地未push的分叉提交历史整理成直线
## 标签管理
### 创建标签
切换到本分支
```bash
git tag v1.0
```
git tag 可以查看到所有标签
如果要打历史的标签可以先查找历史版本
```bash
git log --pretty=oneline --abbrev-commit
```
上边--pretty=oneline表示每个版本一行输出；--abbrev-commit表示提交号只显示前几位,找到对应的commit id
```bash
git tag v0.9 f52c633
```
若要查看标签信息
```bash
git show v0.9
```
还可以给标签添加信息说明
```bash
git tag -a v0.1 -m "version 0.1 released" 1094adb
```
### 操作标签
删除标签
```bash
git tag -d v1.0
```
将标签推送到远程库
```bash
git push origin v1.0
git push origin --tags
```
删除远程库的标签
```bash
git tag -d v0.9
git push origin :refs/tags/v0.9
```