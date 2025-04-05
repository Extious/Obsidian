---
title: RPC
tags:
  - rpc
update: 2025-04-05
---
# 概念
1. RPC（Remote Procedure Call Protocol） 远程过程调用协议。
2. RPC是一种通过网络从远程计算机程序上请求服务，不需要了解底层网络技术的协议。
3. RPC主要作用就是不同的服务间方法调用就像本地调用一样便捷。
# 常用RPC技术或框架
1. 应用级的服务框架：阿里的 Dubbo/Dubbox、Google gRPC、Spring Boot/Spring Cloud。
2. 远程通信协议：RMI、Socket、SOAP(HTTP XML)、REST(HTTP JSON)。
3. 通信框架：MINA 和 Netty
# 具体流程
![image](https://picture.zhaozhan.site/rpc-process.png)
# grpc
# 参考文章
[参考链接](https://juejin.cn/post/7243263236622155834)
[grpc文档](https://grpc.io/docs/languages/go/quickstart/)