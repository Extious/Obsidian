---
title: 完整Git开发规范
tags:
  - git
update: 2025-04-06
---
## 分支策略
![image](https://picture.zhaozhan.site/git-strategy.png)
1. **master**主分支,用于生产环境的主分支
2. **test**分支,用于测试环境分支,一般可以自动CICD
3. **release**分支,用于生产环境分支,只能通过master合并进入
4. fix/* 分支,用于修补线上bug分支
5. feat/* 分支,用于开发功能分支
6. refactor/* 分支,用于重构代码
7. **禁止使用姓名缩写命名分支**
## 三大环境
1. 生产环境
    > 用于部署成品的环境,master分支
    >
2. 测试环境
    > 用于部署测试,test分支
    >
3. 开发环境
    > 用于本地进行测试
    >
## 开发流程
1. git clone remote-url 克隆仓库
2. 拉取最新代码
    * git fetch origin master:master 不在master
    * git pull origin master 在master
3. 开发
    1. 创建新分支
        * git checkout -b feat/xxx master 开发新功能
        * git checkout -b fix/xxx master 修补bug
        * git checkout -b refactor/xxx master 重构
    2. 推送新分支
        * git push origin xxx
    3. 合并到test分支
        > 前提是在开发环境测试没有问题
        >
        1. git fetch origin test:test
        2. git checkout test
        3. git merge xxx(自己的分支)
            * 没有冲突
              1. git push 推送分支
            * 产生冲突
              1. git checkout -b merge/xxx test
              2. 解决冲突
              3. git merge xxx
              4. git push origin xxx
              5. 继续向test合并
    4. 提出master的merge request(在gitlab中)
        > 前提是在测试环境没有问题
        >
        * 产生冲突和test解决方式类似
        * review没有问题,合并分支到master,结束开发
        * review出问题
          1. 继续修改代码,解决问题再次请求合并
4. 开发完毕,删除分支
    1. git push origin :xxx(远程分支名字)
    2. git branch -d xxx(本地分支名字)
## 注意事项
1. 提交merge request前**必须经过测试环境检验**
2. test分支代码**不能**合并到master分支
3. test分支可以直接合并,master分支必须经过审核
4. **不要在test分支直接进行开发!**
5. **禁止使用姓名缩写命名分支**
6. **一旦分支合并入master,请删除分支,避免分支上二次开发**
## 远程分支跟踪
1. 远程没有分支，本地也没有分支
```Shell
git checkout -b test  //创建并切换到新分支
git push --set-upstream origin test  //推送到远程分支，并且跟踪远程分支
```
2. 远程已经存在分支，本地不存在对应分支
```Shell
git checkout -b newtest origin/test
git pull
```
## 提交规范
### 格式
* `type(scope) : subject`
#### type
* feat: 新特性或功能
* fix: 缺陷修复
* docs: 文档更新
* style: 代码风格或者组件样式更新
* refactor: 代码重构，不引入新功能和缺陷修复
* perf: 性能优化
* test: 单元测试
* chore: 其他不修改 src 或测试文件的提交
#### scope(optional)
* 用于说明 commit 影响的范围，比如数据层、控制层、视图层等等，视项目不同而不同
#### subject
* 简易描述该commit做了什么
## MR规范
* 在仓库提交mr时候,应该注明修改或者添加了什么功能(相当于提交的总结,需要必commit message详细)
```Plain
# 示例
1. fix:删除了审核的部分
2. feat:完善了测试环境自动推送脚本
```