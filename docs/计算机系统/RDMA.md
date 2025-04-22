---
title: RDMA
tags:
  - rdma
update: 2025-04-06
---
## 传统通信过程
1. 数据发送方需要讲数据从用户应用空间Buffer复制到内核空间的Socket Buffer中。
2. 然后Kernel空间中添加数据包头，进行数据封装。通过一系列多层网络协议的数据包处理工作
3. 数据被Push到NIC网卡中的Buffer进行网络传输
4. 消息接受方接受从远程机器发送的数据包后，要将数据包从NIC buffer中复制数据到Socket Buffer
5. 然后经过一些列的多层网络协议进行数据包的解析工作
6. 解析后的数据被复制到相应位置的用户应用空间Buffer
7. 这个时候再进行系统上下文切换，用户应用程序才被调用
## 基本原理
RDMA是一种新的直接内存访问技术，RDMA让计算机可以直接存取其他计算机的内存，而不需要经过处理器的处理。RDMA将数据从一个系统快速移动到远程系统的内存中，而不对操作系统造成任何影响。
目前支持RDMA的网络协议主要有三种
* InfiniBand(IB)
* iWARP(RDMA over TCP/IP)
* RoCE(RDMA over Converged Ethernet)
  * RoCEv1和RoCEv2
## 操作
### Memory Verbs
### Messaging Verbs