---
title: Git问题汇总
tags:
  - git
update: 2025-04-06
---
## git相关问题记录
### ssl证书问题
问题描述：
在用steam++的host代理模式时，使用git clone时出现ssl证书的问题如下
```bash
Cloning into 'meta-api'...
fatal: unable to access 'https://github.com/dineshdixitgit/meta-api.git/': SSL certificate problem: unable to get local issuer certificate
```
问题解决：
```bash
//查看git相关配置
git config -l --show-origin
//将github desktop使用windows证书存储
git config --global http.sslBackend schannel
```
[参考链接](https://github.com/desktop/desktop/issues/9293)
### https代理问题
问题描述：
**使用clash梯子时，git还是没有走梯子这个代理，所以git使用https方式clone时还是超时报错，默认从443端口访问，可以配置代理到7890可代理端口上**
问题解决：
```bash
git config --global http.proxy 127.0.0.1:7890
git config --global https.proxy 127.0.0.1:7890
```
[参考链接](https://blog.csdn.net/zpf1813763637/article/details/128340109)
### ssh代理问题
问题描述：
使用clash梯子时，ssh并没有走梯子这个代理，所以还是连不到github，默认从22端口访问，可以将配置代理到443端口，走“问题2”的流程
问题解决：
```bash
//在.ssh下创建config文件，填写以下内容：（若该文件已存在可直接在后边加上以下几行）
Host github.com
Hostname ssh.github.com
Port 443
```
[参考链接](https://gist.github.com/Tamal/1cc77f88ef3e900aeae65f0e5e504794)
> 注:上述代理需要手动配置的原因猜测是因为先安装配置了clash,后又安装了git,导致git的命令并没有走代理