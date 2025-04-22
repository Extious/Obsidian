---
title: OpenWhisk
tags:
  - openwhisk
update: 2025-04-06
---
## OpenWhisk 编程模型
![image](https://picture.zhaozhan.site/openwhisk-model.png)
#### What is an Action?
在 OpenWhisk 平台上运行的无状态函数（代码片段）。封装了为响应事件而执行的应用程序逻辑。
可以通过一下三种方式进行调用：
* OpenWhisk REST API
* OpenWhisk CLI
* 简单的用户创建的API手动调用
* 触发器调用
## 部署Openwhisk
### Running OpenWhisk locally
#### 使用 Docker 中启用的 Kubernetes（Minikube）
#### Alternative options
##### Standalone
开始使用 OpenWhisk 的最简单方法是安装“独立”OpenWhisk 堆栈。这是一个功能齐全的 OpenWhisk 堆栈，为方便起见，作为 Java 进程运行。无服务器函数在 Docker 容器中运行。您的机器上需要有 Docker、Java 和 Node.js。
首先需要安装java、nodejs [参考文章](https://zhuanlan.zhihu.com/p/141726465)
然后可以clone编译
```bash
git clone https://github.com/apache/openwhisk.git
cd openwhisk
./gradlew core:standalone:build
```
运行生成的可执行文件：
```bash
java -jar openwhisk-standalone.jar
```
服务起来后设置提示的命令:设置apihost和auth
```bash
wsk property set --apihost 'http://172.17.0.1:3233' --auth '23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP'
```
##### Docker Compose
##### Ansible
##### Vagrant
## 使用Openwhisk
### wsk
[下载地址](https://github.com/apache/openwhisk-cli/releases)
### wskdeploy
[下载地址](https://github.com/apache/openwhisk-wskdeploy/releases)
### OpenWhisk REST API
### OpenWhisk Clients
## Openwhisk架构
#### What happens on an invocation?
![image](https://picture.zhaozhan.site/openwhisk-structure.png)