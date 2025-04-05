---
title: Nginx
tags:
  - nginx
update: 2025-04-06
---
# Nginx概述
Nginx (engine x)  是一款轻量级的 Web 服务器 、反向代理服务器及电子邮件（IMAP/POP3）代理服务器。
## 反向代理
反向代理（Reverse Proxy）方式是指以代理服务器来接受 internet 上的连接请求，然后将请求转发给内部网络上的服务器，并将从服务器上得到的结果返回给 internet 上请求连接的客户端，此时代理服务器对外就表现为一个反向代理服务器。
而正向代理就是我们在客户端平时使用的代理。
![web-nginx-1.excalidraw](https://picture.zhaozhan.site/web-nginx-1.excalidraw.png)
## 负载均衡
![web-nginx-2.excalidraw](https://picture.zhaozhan.site/web-nginx-2.excalidraw.png)
## 动静分离
什么是动静分离：其实就是将一些静态的、不会变的资源通过nginx直接拿去，而不需要去请求后台，避免后端压力过大
![web-nginx-3.excalidraw](https://picture.zhaozhan.site/web-nginx-3.excalidraw.png)
# Nginx入门
## Nginx配置
Nginx的配置文件在Linux中位于/etc/nginx/nginx.conf
nginx 的使用比较简单，就是几条命令。
常用到的命令如下：
```bash
nginx -s stop       快速关闭Nginx，可能不保存相关信息，并迅速终止web服务。
nginx -s quit       平稳关闭Nginx，保存相关信息，有安排的结束web服务。
nginx -s reload     因改变了Nginx相关配置，需要重新加载配置而重载。
nginx -s reopen     重新打开日志文件。
nginx -c filename   为 Nginx 指定一个配置文件，来代替缺省的。
nginx -t            不运行，仅仅测试配置文件。nginx 将检查配置文件的语法的正确性，并尝试打开配置文件中所引用到的文件。
nginx -v            显示 nginx 的版本。
nginx -V            显示 nginx 的版本，编译器版本和配置参数。
```
# Nginx实战
![image](https://picture.zhaozhan.site/web-nginx-eg.png)c
上图，在浏览器中输入localhost：80会重定向到localhost：3000，但是会隐藏localhost：3000这一地址。
[Nginx反代理相关路由细节](https://ld246.com/article/1677207724771)
# 参考文章
[知乎：Nginx的简介和安装](https://zhuanlan.zhihu.com/p/382228615)
[CSDN：Nginx入门教程](https://blog.csdn.net/weixin_54065960/article/details/131455673)