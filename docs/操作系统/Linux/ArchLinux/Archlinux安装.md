---
title: Archlinux安装
tags:
  - linux
update: 2025-04-05
---
# 启动U盘
[下载镜像](https://archlinux.org/download/)
[Ventoy烧录](https://www.ventoy.net/cn/doc_start.html)
进入BIOS中关闭Secure Boot
调整启动方式为UEFI（对应磁盘格式为GPT，之后格式化的时候会改）
使用U盘启动
进入如下archlinux的live页面
​![network-asset-图片.2ob94sb57l](https://picture.zhaozhan.site/archlinux-live.webp)​
# 基础安装
## 进入 Live 环境后关闭 reflector：
​`systemctl stop reflector​`
reflector 会根据速度自动修改镜像源，但是由于只考虑最新的20个镜像站，其结果大多数时候都不怎么好用。
## 确保使用的UEFI模式：
​`ls /sys/firmware/efi/efivars​`
若有效输出则已启动
## 连接网络
```shell
iwctl                           #执行iwctl命令，进入交互式命令行
device list                     #列出设备名，比如无线网卡看到叫 wlan0
station wlan0 scan              #扫描网络
station wlan0 get-networks      #列出网络 比如想连接YOUR-WIRELESS-NAME这个无线
station wlan0 connect YOUR-WIRELESS-NAME #进行连接 输入密码即可exit  
```
可以等待几秒等网络建立连接后再进行下面测试网络的操作。
​`ping www.gnu.org​`
如果你不能正常连接网络，首先确认系统已经启用网络接口：
```shell
ip link  #列出网络接口信息，如无线联网的设备叫wlan0
ip link set wlan0 up #比如无线网卡看到叫 wlan0
```
如果随后看到类似`Operation not possible due to RF-kill​`的报错，继续尝试 `rfkill​`命令来解锁无线网卡：`rfkill unblock wifi​`
## 更新系统时钟
```shell
timedatectl set-ntp true    #将系统时间与网络时间进行同步
timedatectl status          #检查服务状态
```
## 磁盘分区
一个通用的方案：

|挂载点|分区|分区类型|建议大小|备注|
|---|---|---|---|---|
|/mnt/boot|/dev/sda1 或/dev/nvme0n1p1|EFI System|512 MiB|ESP 分区|
|/mnt|/dev/sda2 或/dev/nvme0n1p2|Linux x86-64 root|100 GiB（至少 50 GiB）|Arch Linux 的根分区|
|/mnt/home|/dev/sda3 或/dev/nvme0n1p3|Linux home|剩余磁盘空间|Arch Linux 的 home 分区|
首先将磁盘类型转换为GPT格式，这里假设比如你想安装的磁盘名称为 sdx。如果你使用 NVME 的固态硬盘，你看到的磁盘名称可能为 `nvme0n1`。
```shell
lsblk                       #显示分区情况 找到你想安装的磁盘名称
parted /dev/sdx             #执行parted，进入交互式命令行，进行磁盘类型变更
​
(parted)mktable             #输入mktable
New disk label type? gpt    #输入gpt 将磁盘类型转换为gpt 如磁盘有数据会警告，输入yes即可
quit                        #最后quit退出parted命令行交互
```
然后进行分区操作
```shell
cfdisk /dev/sdx #来执行分区操作,分配各个分区大小，类型
fdisk -l #分区结束后， 复查磁盘情况
```
其次是格式化操作
```shell
mkfs.ext4  /dev/sdax            #格式化根目录和home目录的两个分区
mkfs.vfat  /dev/sdax            #格式化efi分区
```
最后是挂载操作
在挂载时，挂载是有顺序的，先挂载根分区，再挂载 EFI 分区。 这里的 sdax 只是例子，具体根据你自身的实际分区情况来。
```shell
mount /dev/sdax  /mnt
mkdir /mnt/efi     #创建efi目录
mount /dev/sdax /mnt/efi
mkdir /mnt/home    #创建home目录
mount /dev/sdax /mnt/home
```
## 建立交换文件（可选）
交换文件相当于 Windows 中的虚拟内存，也就是利用硬盘空间充当内存。当内存相对不足时，部分内存中的内容会交换到硬盘中，从而释放内存。关于 swap 的重要性，有两篇不错的文章，推荐读者阅读。
[https://farseerfc.me/zhs/in-defence-of-swap.html](https://farseerfc.me/zhs/in-defence-of-swap.html)
[https://farseerfc.me/zhs/followup-about-swap.html](https://farseerfc.me/zhs/followup-about-swap.html)
推荐swap大小

|内存大小|2 GiB|4 GiB|8 GiB|16 GiB|32 GiB|64 GiB|
|---|---|---|---|---|---|---|
|推荐的交换文件大小（使用休眠功能）|4096 MiB|5793 MiB|8192 MiB|11585 MiB|16384 MiB|23170 MiB|
|推荐的交换文件大小（不使用休眠功能）|4096 MiB|5793 MiB|8192 MiB|8192 MiB|4096 MiB|0 MiB|
建立交换文件的具体操作方法如下。
首先使用 dd 创建交换文件。例如，创建一块 8 GiB （=8192 MiB）大小的交换文件。
```shell
dd if=/dev/zero of=/mnt/swapfile bs=1M count=8192 status=progress
```
如果您需要创建其他大小的交换文件，请将 count= 后面的数值换成交换文件大小的 MiB 数（GiB 数 x 1024）。
然后修改权限
```shell
chmod 0600 /mnt/swapfile
```
最后格式化并启用swap
```shell
mkswap -U clear /mnt/swapfile
swapon /mnt/swapfile
```
## 选择软件仓库镜像
### reflector
推荐使用reflector，使用如下命令选择镜像。此命令将为您选出位于平均同步延迟在 3 小时以内的，位于中国的 https 镜像，并根据速度排序。指定 --completion-percent 95（默认为100）的目的是防止忽略可用的镜像。
```shell
reflector -p https -c China --delay 3 --completion-percent 95 --sort rate --save /etc/pacman.d/mirrorlist
```
也可使用得分排序
```shell
reflector -p https -c China --delay 3 --completion-percent 95 --sort score --save /etc/pacman.d/mirrorlist
```
### 手动自行修改
也可以手动修改 /etc/pacman.d/mirrorlist​配置文件，使用vim或nano在 /etc/pacman.d/mirrorlist​中添加镜像源
```shell
root@archiso ~ # nano /etc/pacman.d/mirrorlist
/etc/pacman.d/mirrorlist
------------------------
Server = https://mirrors.bfsu.edu.cn/archlinux/$repo/os/$arch
Server = https://mirrors.sjtug.sjtu.edu.cn/archlinux/$repo/os/$arch
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch
Server = https://mirrors.ustc.edu.cn/archlinux/$repo/os/$arch
```
默认先使用第一行的镜像源
完整镜像源列表可以参考[官方文档](https://archlinux.org/mirrorlist/)
## 安装系统
安装必需的基础包
```shell
pacstrap /mnt base base-devel linux linux-headers linux-firmware  #base-devel在AUR包的安装是必须的
```
可能有警告但是一定应该没有报错
如果报告“验证软件包错误”，可以尝试以下方法，然后重新安装。
```shell
pacman-key --init  # 初始化密钥环
pacman-key --populate
pacman -Sy archlinux-keyring  # 更新 archlinux-keyring
```
安装必需的功能性软件
```
pacstrap /mnt dhcpcd iwd vim bash-completion   #一个有线所需(iwd也需要dhcpcd) 一个无线所需 一个编辑器 一个补全工具
```
## 生成fstab文件
fstab是一个系统文件，决定了系统启动时如何自动挂载分区。没有 fstab，系统将找不到根分区，从而无法启动。
Arch Linux 提供了自动生成 fstab 的工具，我们利用它直接生成。
```shell
genfstab -U /mnt >> /mnt/etc/fstab
```
其中`genfstab -U /mnt​`是以 UUID 的描述方式生成 `fstab`，`“>>”` 的意思是，将输出结果附加在后面的文件之后。
生成完成后，记得使用 cat 命令打印文件内容，仔细检查一遍。
```shell
cat /mnt/etc/fstab
```
10. ## Change root
我们使用 arch-chroot 工具切换到新安装的系统，以后的操作就可以在新安装的系统中完成了。
```shell
arch-chroot /mnt
```
11. ## 时区设置
将时区设置为中国上海
```shell
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
```
然后设置硬件时间
```shell
hwclock --systohc
```
## 设置Locale进行本地化
Locale 决定了地域、货币、时区日期的格式、字符排列方式和其他本地化标准。
首先使用 vim 编辑 /etc/locale.gen​，去掉 en_US.UTF-8 所在行以及 zh_CN.UTF-8 所在行的注释符号（#）。
这里需要使用 vim 的寻找以及编辑功能，具体可自行查询
```shell
vim /etc/locale.gen
locale-gen    #编辑修改之后生成locale
echo 'LANG=en_US.UTF-8'  > /etc/locale.conf    #最后向 /etc/locale.conf 导入内容
```
## 网络配置
### 设置主机名
```shell
[root@archiso ~]# vim /etc/hostname
----------------------------------
我的主机名（myarch）
```
### 网络管理器
需要安装一个网络管理器，笔者推荐使用 NetworkManager。
```shell
pacman -S networkmanager
```
NetworkManager 附带一个守护程序。在 Arch Linux 中，守护程序由 systemd 管理。systemd 是非常重要的系统程序。现在我们使用 systemd 设置 NetworkManager 开机自动启动。
```shell
systemctl enable NetworkManager.service
```
## root密码
设置root用户密码
```shell
[root@archiso ~]# passwd
New password:  # 请输入密码，这里不会显示“*”，这是正常现象
Retype new password:
passwd: password updated successfully
```
## 引导加载程序
推荐使用GRUB，本文章只针对UEFI启动模式的电脑，对于BIOS启动模式的电脑可查看[参考文章](https://www.viseator.com/2017/05/17/arch_install/)
### 安装微码
先查看CPU型号：
```shell
cat /proc/cpuinfo | grep "model name"
```
如果是 Intel CPU，安装 intel-ucode。
```shell
pacman -S intel-ucode
```
如果是 AMD CPU，安装 amd-ucode。
```shell
pacman -S amd-ucode
```
### 安装引导程序
```shell
pacman -S grub efibootmgr   #grub是启动引导器，efibootmgr被 grub 脚本用来将启动项写入 NVRAM。
grub-install --target=x86_64-efi --efi-directory=/efi --bootloader-id=GRUB
```
可以对配置文件进行修改：编辑/etc/default/grub 文件，去掉 GRUB_CMDLINE_LINUX_DEFAULT​一行中最后的 quiet 参数，同时把 log level 的数值从 3 改成 5，这样是为了后续如果出现系统错误，方便排错。同时在同一行加入 nowatchdog 参数，这可以显著提高开关机速度。
```shell
vim /etc/default/grub
```
最后生成GRUB所需的配置文件
```shell
grub-mkconfig -o /boot/grub/grub.cfg
```
## 重启
首先退出chroot环境
```shell
exit
```
然后关闭交换文件（如果有）
```shell
swapoff /mnt/swapfile
```