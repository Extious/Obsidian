---
title: GPU通信方式
tags:
  - gpu
update: 2025-04-05
---
## 单机多卡
### GPU Direct
GPU Direct 是 NVIDIA 开发的一项技术，可实现 GPU 与其他设备（例如网络接口卡 (NIC) 和存储设备）之间的直接通信和数据传输，而不涉及 CPU。
#### GPUDirect Storge
GPUDirect Storage 允许存储设备和 GPU 之间进行直接数据传输，绕过 CPU，减少数据传输的延迟和 CPU 开销。
通过 GPUDirect Storage，GPU 可以直接从存储设备（如固态硬盘（SSD）或非易失性内存扩展（NVMe）驱动器）访问数据，而无需将数据先复制到 CPU 的内存中。这种直接访问能够实现更快的数据传输速度，并更高效地利用 GPU 资源。

> NVMe 全称 Non-Volatile Memory Express，中文译为非易失性内存主机控制器接口规范。它是一种专为闪存和下一代固态硬盘（SSD）设计的高性能存储协议。NVMe 允许 SSD 直接通过 PCIe 总线与 CPU 通信，绕过了传统 SATA 接口的瓶颈，大幅提升数据读写速度。

> 闪存（Flash Memory）是一种非易失性（Non-Volatile）的计算机存储芯片, 闪存主要分为两种类型： • **NAND Flash（与非闪存）：**  容量大、成本低、擦写速度快，但可靠性相对较低，主要用于大容量存储设备，如固态硬盘（SSD）、U盘、存储卡等。 • **NOR Flash（或非闪存）：**  容量较小、成本较高、擦写速度较慢，但可靠性高，可以直接执行代码（XIP, Execute In Place），主要用于存储启动代码、固件等，常见于嵌入式系统、手机等设备。

> SATA，全称 Serial ATA（Serial Advanced Technology Attachment），中文译为串行高级技术附件，是一种计算机总线接口，主要用于连接主机系统（如计算机主板）与存储设备（如硬盘、光驱）。

![image](https://picture.zhaozhan.site/gpu-communication-2.png)
![image](http://picture.zhaozhan.site/gpu-communication-1.png)

* GPUDirect RDMA
* GPUDirect P2P
* GPUDirect 视频
## 参考文章
[聊透 GPU 通信技术——GPU Direct、NVLink、RDMA - 又拍云 - 博客园](https://www.cnblogs.com/upyun/p/17679500.html)