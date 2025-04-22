---
title: SSH详解
tags:
  - ssh
  - linux
update: 2025-04-05
---
## 什么是SSH
**Secure Shell** (**SSH**) 是一个允许两台电脑之间通过安全的连接进行数据交换 的**网络协议**。
* 传统：FTP、Telnet 是再网络中明文传送数据、用户帐号和密码，很容易受到中间人攻击 。
* SSH：利用 SSH 协议 可以有效防止远程管理过程中的信息泄露问题。通过SSH可以对所有传输的数据进行加 密，也能够防止 DNS 欺骗和 IP 欺骗。
> 补充：SSH使用的是非对称加密的一种：使用公钥和私钥进行加密和解密，一般使用公钥加密，私钥解密。

SSH的身份验证阶段，SSH只支持服务端保留公钥，客户端保留私钥的方式，** 所以方式只有两种：客户端生成密钥对，将公钥分发给服务端；服务端生成密钥对，将私钥分发给客户端。只不过出于安全性和便利性，一般都是客户端生成密钥对并分发公钥。
## SSH概要
* SSH是会话层上的协议
* SSH服务的守护进程是sshd,默认监听在22端口
* SSH客户端命令读取两个配置文件,也可以在输入命令时配置。
  * 全局：/etc/ssh/ssh_config
  * 用户：~/.ssh/config
  * 优先级：命令配置&gt;用户&gt;全局
* SSH涉及到两个验证：主机验证、用户验证
* SSH支持多种身份验证，它们的验证顺序如下：gssapi-with-mic,hostbased,publickey,keyboard-interactive,password，但常见的是密码认证机制(password)和公钥认证机制(public key)。
* SSH客户端有很多强大的功能：端口转发、代理认证、连接共享等
* SSH服务端配置文件为/etc/ssh/sshd_config（与客户端配置文件区分开）
![image](https://picture.zhaozhan.site/ssh-config.png)
* 易被忽略：SSH登陆会被分配一个伪终端，可以配置sudo这种身份验证程序被禁止使用**
## 主机验证过程
客户端输入以下命令之后，首先进行主机验证过程**
```bash
ssh ip_addr
```
* 客户端首先读取~/.ssh/known_hosts文件和/etc/ssh/known_hosts文件，看其中是否存储了服务端的主机信息（host key），如果没有，询问是否保存该服务端的主机信息；如果有，直接进入身份验证
* 服务端的host key在/etc/ssh/ssh_host_\*.pub文件中（不同加密算法不同，在sshd服务程序启动时重建）
  主机验证阶段：服务端持有的是私钥，客户端保存的是服务端的公钥，这和身份验证阶段密钥持有方相反
> 补充：实际上ssh对比的不是host key,因为太长了，对比的是host key的指纹。指纹可以通过ssh-kegen计算得出。ssh还支持host key的模糊比较（图形对比）。**

更详细的主机认证过程是：先进行密钥交换(DH算法)生成session key(rfc文档中称之为shared secret)，然后从文件中读取host key，并用host key对session key进行签名，然后对签名后的指纹进行判断.
## 身份认证过程
常见的身份认证为密码认证和公钥认证，当公钥认证机制未通过时，再进行密码认证机制。认证顺序可以通过ssh配置文件中的指令PerferredAuthentications改变。
* 公钥认证：客户端需将自己生成的公钥（~/.ssh/id_\*.pub）发送到服务端的~/.ssh/authorized_keys文件中。认证时将私钥推导或者公钥指纹（不同版本）发给服务端。服务端判断是否认证通过，如果认证不通过，则进入下一个认证机制：密码认证机制。**
* 密码认证：输入服务端用户密码。
## 配置文件分布
服务端：
*  /etc/ssh/sshd_config：ssh服务程序sshd的配置文件。
* /etc/ssh/ssh_host_\*：服务程序sshd启动时生成的服务端公钥和私钥文件。如ssh_host_rsa_key和ssh_host_rsa_key.pub。
  * 其中.pub文件是主机验证时的host key，将写入到客户端的~/.ssh/known_hosts文件中。
  * 其中私钥文件严格要求权限为600，若不是则sshd服务可能会拒绝启动。
*  ~/.ssh/authorized_keys：保存的是基于公钥认证机制时来自于客户端的公钥。在基于公钥认证机制认证时，服务端将读取该文件。
**客户端：**
*  /etc/ssh/ssh_config：客户端的全局配置文件。
*  ~/.ssh/config：客户端的用户配置文件，生效优先级高于全局配置文件。一般该文件默认不存在。该文件对权限有严格要求只对所有者有读/写权限，对其他人完全拒绝写权限。
*  ~/.ssh/known_hosts：保存主机验证时服务端主机host key的文件。文件内容来源于服务端的ssh_host_rsa_key.pub文件。
*  /etc/ssh/known_hosts：全局host key保存文件。作用等同于~/.ssh/known_hosts。
*  ~/.ssh/id_rsa：客户端生成的私钥。由ssh-keygen生成。该文件严格要求权限，当其他用户对此文件有可读权限时，ssh将直接忽略该文件。
*  ~/.ssh/id_rsa.pub    ：私钥id_rsa的配对公钥。对权限不敏感。当采用公钥认证机制时，该文件内容需要复制到服务端的~/.ssh/authorized_keys文件中。
*  ~/.ssh/rc：保存的是命令列表，这些命令在ssh连接到远程主机成功时将第一时间执行，执行完这些命令之后才开始登陆或执行ssh命令行中的命令。
*  /etc/ssh/rc：作用等同于~/.ssh/rc。
**简单介绍sshd_config指令**
```bash
#Port 22                # 服务端SSH端口，可以指定多条表示监听在多个端口上
#ListenAddress 0.0.0.0  # 监听的IP地址。0.0.0.0表示监听所有IP
Protocol 2              # 使用SSH 2版本
#####################################
#          私钥保存位置               #
#####################################
# HostKey for protocol version 1
#HostKey /etc/ssh/ssh_host_key      # SSH 1保存位置/etc/ssh/ssh_host_key
# HostKeys for protocol version 2
#HostKey /etc/ssh/ssh_host_rsa_key  # SSH 2保存RSA位置/etc/ssh/ssh_host_rsa _key
#HostKey /etc/ssh/ssh_host_dsa_key  # SSH 2保存DSA位置/etc/ssh/ssh_host_dsa _key
###################################
#           杂项配置               #
###################################
#PidFile /var/run/sshd.pid        # 服务程序sshd的PID的文件路径
#ServerKeyBits 1024               # 服务器生成的密钥长度
#SyslogFacility AUTH              # 使用哪个syslog设施记录ssh日志。日志路径默认为/var/log/secure
#LogLevel INFO                    # 记录SSH的日志级别为INFO
###################################
#   以下项影响认证速度               #
###################################
#UseDNS yes                       # 指定是否将客户端主机名解析为IP，以检查此主机名是否与其IP地址真实对应。默认yes。
                                  # 由此可知该项影响的是主机验证阶段。建议在未配置DNS解析时，将其设置为no，否则主机验证阶段会很慢
###################################
#   以下是和安全有关的配置           #
###################################
#PermitRootLogin yes              # 是否允许root用户登录
#GSSAPIAuthentication no          # 是否开启GSSAPI身份认证机制，默认为yes
#PubkeyAuthentication yes         # 是否开启基于公钥认证机制
#AuthorizedKeysFile  .ssh/authorized_keys  # 基于公钥认证机制时，来自客户端的公钥的存放位置
PasswordAuthentication yes        # 是否使用密码验证，如果使用密钥对验证可以关了它
#PermitEmptyPasswords no          # 是否允许空密码，如果上面的那项是yes，这里最好设置no
#MaxSessions 10                   # 最大客户端连接数量
#LoginGraceTime 2m                # 身份验证阶段的超时时间，若在此超时期间内未完成身份验证将自动断开
#MaxAuthTries 6                   # 指定每个连接最大允许的认证次数。默认值是6。
                                  # 如果失败认证次数超过该值一半，将被强制断开，且生成额外日志消息。
MaxStartups 10                    # 最大允许保持多少个未认证的连接。默认值10。
###################################
#   以下可以自行添加到配置文件        #
###################################
DenyGroups  hellogroup testgroup  # 表示hellogroup和testgroup组中的成员不允许使用sshd服务，即拒绝这些用户连接
DenyUsers   hello test            # 表示用户hello和test不能使用sshd服务，即拒绝这些用户连接
###################################
#   以下一项和远程端口转发有关        #
###################################
#GatewayPorts no                  # 设置为yes表示sshd允许被远程主机所设置的本地转发端口绑定在非环回地址上
                                  # 默认值为no，表示远程主机设置的本地转发端口只能绑定在环回地址上，见后文"远程端口转发"
```
关于/etc/ssh/sshd_config的更多配置选项参考[sshd_config中文文档](http://www.jinbuguo.com/openssh/sshd_config.html)
简单介绍ssh_config文件相关指令
```bash
# Host *                              # Host指令是ssh_config中最重要的指令，只有ssh连接的目标主机名能匹配此处给定模式时，
                                      # 下面一系列配置项直到出现下一个Host指令才对此次连接生效
#   ForwardAgent no
#   ForwardX11 no
#   RhostsRSAAuthentication no
#   RSAAuthentication yes
#   PasswordAuthentication yes     # 是否启用基于密码的身份认证机制
#   HostbasedAuthentication no     # 是否启用基于主机的身份认证机制
#   GSSAPIAuthentication no        # 是否启用基于GSSAPI的身份认证机制
#   GSSAPIDelegateCredentials no
#   GSSAPIKeyExchange no
#   GSSAPITrustDNS no
#   BatchMode no                   # 如果设置为"yes"，将禁止passphrase/password询问。比较适用于在那些不需要询问提供密
                                   # 码的脚本或批处理任务任务中。默认为"no"。
#   CheckHostIP yes
#   AddressFamily any
#   ConnectTimeout 0
#   StrictHostKeyChecking ask        # 设置为"yes"，ssh将从不自动添加host key到~/.ssh/known_hosts文件，
                                     # 且拒绝连接那些未知的主机(即未保存host key的主机或host key已改变的主机)。
                                     # 它将强制用户手动添加host key到~/.ssh/known_hosts中。
                                     # 设置为ask将询问是否保存到~/.ssh/known_hosts文件。
                                     # 设置为no将自动添加到~/.ssh/known_hosts文件。
#   IdentityFile ~/.ssh/identity     # ssh v1版使用的私钥文件
#   IdentityFile ~/.ssh/id_rsa       # ssh v2使用的rsa算法的私钥文件
#   IdentityFile ~/.ssh/id_dsa       # ssh v2使用的dsa算法的私钥文件
#   Port 22                          # 当命令行中不指定端口时，默认连接的远程主机上的端口
#   Protocol 2,1
#   Cipher 3des                      # 指定ssh v1版本中加密会话时使用的加密协议
#   Ciphers aes128-ctr,aes192-ctr,aes256-ctr,arcfour256,arcfour128,aes128-cbc,3des-cbc  # 指定ssh v1版本中加密会话时使用的加密协议
#   MACs hmac-md5,hmac-sha1,umac-64@openssh.com,hmac-ripemd160
#   EscapeChar ~
#   Tunnel no
#   TunnelDevice any:any
#   PermitLocalCommand no    # 功能等价于~/.ssh/rc，表示是否允许ssh连接成功后在本地执行LocalCommand指令指定的命令。
#   LocalCommand             # 指定连接成功后要在本地执行的命令列表，当PermitLocalCommand设置为no时将自动忽略该配置
                             # %d表本地用户家目录，%h表示远程主机名，%l表示本地主机名，%n表示命令行上提供的主机名，
                             # p%表示远程ssh端口，r%表示远程用户名，u%表示本地用户名。
#   VisualHostKey no         # 是否开启主机验证阶段时host key的图形化指纹
Host *
        GSSAPIAuthentication yes
```
关于上述配置文件的相关内容参考[相关链接](https://www.cnblogs.com/f-ck-need-u/p/7129122.html)
## ssh命令
```bash
ssh [options] [user@]hostname [command]
参数说明：
-b bind_address ：在本地主机上绑定用于ssh连接的地址，当系统有多个ip时才生效。
-E log_file     ：将debug日志写入到log_file中，而不是默认的标准错误输出stderr。
-F configfile   ：指定用户配置文件，默认为~/.ssh/config。
-f              ：请求ssh在工作在后台模式。该选项隐含了"-n"选项，所以标准输入将变为/dev/null。
-i identity_file：指定公钥认证时要读取的私钥文件。默认为~/.ssh/id_rsa。
-l login_name   ：指定登录在远程机器上的用户名。也可以在全局配置文件中设置。
-N              ：显式指明ssh不执行远程命令。一般用于端口转发，见后文端口转发的示例分析。
-n              ：将/dev/null作为标准输入stdin，可以防止从标准输入中读取内容。ssh在后台运行时默认该项。
-p port         ：指定要连接远程主机上哪个端口，也可在全局配置文件中指定默认的连接端口。
-q              ：静默模式。大多数警告信息将不输出。
-T              ：禁止为ssh分配伪终端。
-t              ：强制分配伪终端，重复使用该选项"-tt"将进一步强制。
-v              ：详细模式，将输出debug消息，可用于调试。"-vvv"可更详细。
-V              ：显示版本号并退出。
-o              ：指定额外选项，选项非常多。
user@hostname   ：指定ssh以远程主机hostname上的用户user连接到的远程主机上，若省略user部分，则表示使用本地当前用户。
                ：如果在hostname上不存在user用户，则连接将失败(将不断进行身份验证)。
command         ：要在远程主机上执行的命令。指定该参数时，ssh的行为将不再是登录，而是执行命令，命令执行完毕时ssh连接就关闭。
```
如果要ssh免密登陆可以使用以下命令：
```bash
#id_ed25519.pub改为自己的算法对应的文件名，ip_addr改为自己的服务端ip
cat ~/.ssh/id_ed25519.pub | ssh ip_addr "umask 077; test -d ~/.ssh || mkdir ~/.ssh ; cat >> ~/.ssh/authorized_keys" 
```
或者直接使用提供好的命令：
```bash
#该命令可以直接将公钥分发给服务端，具体实现逻辑和上述命令相同
ssh-copy-id ip_addr 
```
## scp命令
scp是基于ssh的远程拷贝命令，也支持本地拷贝，甚至支持远程到远程的拷贝。scp拷贝是使用的22端口，其实质是使用ssh连接到远程，并使用该连接来传输数据。
具体使用方式如下：
```bash
scp [-12BCpqrv] [-l limit] [-o ssh_option] [-P port] [[user@]host1:]src_file ... [[user@]host2:]dest_file
选项说明：
-1：使用ssh v1版本，这是默认使用协议版本
-2：使用ssh v2版本
-C：拷贝时先压缩，节省带宽
-l limit：限制拷贝速度，Kbit/s，1Byte=8bit，所以"-l 800"表示的速率是100K/S
-o ssh_option：指定ssh连接时的特殊选项，一般用不上。
-P port：指定目标主机上ssh端口，大写的字母P，默认是22端口
-p：拷贝时保持源文件的mtime,atime,owner,group,privileges
-r：递归拷贝，用于拷贝目录。注意，scp拷贝遇到链接文件时，会拷贝链接的源文件内容填充到目标文件中(scp的本质就是填充而非拷贝)
-v：输出详细信息，可以用来调试或查看scp的详细过程，分析scp的机制
```
 (1).本地拷贝到本地：/etc/fstab--&gt;/tmp/a.txt。
```bash
scp /etc/fstab /tmp/a.txt
```
 (2).本地到远程：/etc/fstab--&gt;ip_addr:/tmp/a.txt。
```bash
scp /etc/fstab ip_addr:/tmp
```
 (3).远程到本地：ip_addr:/etc/fstab--&gt;/tmp/a.txt。
```bash
scp ip_addr:/etc/fstab /tmp/a.txt
```
 (4).远程ip_addr1到远程ip_addr2：ip_addr1:/etc/fstab--&gt;/ip_addr2:/tmp/a.txt。
```bash
scp ip_addr1:/etc/fstab ip_addr2:/tmp/a.txt
```
## 生成密钥对
ssh-keygen 命令用于为 ssh 生成、管理和转换认证密钥，它支持 RSA 和 DSA 两种认 证密钥。
该命令的选项：
```bash
# 常用的选项
-b：指定密钥长度； 
-C：添加注释；用于为指定注释，可以是任何内容，通常使用自己的邮件名作为注释。 
-f：指定用来保存密钥的文件名； 
-t：指定要创建的密钥类型（加密方式）; 
-e：读取openssh的私钥或者公钥文件； 
-i：读取未加密的ssh-v2兼容的私钥/公钥文件，然后在标准输出设备上显示openssh兼容的私钥/公钥； 
-l：显示公钥文件的指纹数据； 
-N：提供一个新密语； 
-P：提供（旧）密语； 
-q：静默模式； 
```
生成密钥对时，有一个选项要求你设置密码（passphrase），该密码是用来保护你的私钥的 密码。如果设置了则在使用私钥时会要求你输入这个密码；一般不设置，记不住**【之后 还可更改此密码，使用`ssh-keygen -p`】。
生成后最好将私钥进行备份。
常用的两种加密方式：
* 为了安全考虑如果使用 rsa 加密方式则指定密钥长度为 `-b 4096`（1024 的密钥长度能够被破解，建议指定为 4096）。
* 但现在有了更安全的加密方式 ed25519 ，这是目前最受推荐的公钥算法。当使用 ed25519 加密方式时，它会忽略 `-b` 选项，因为它的长度是固定的。生成的密钥更紧凑 、更短（仅包含 68 个字符）、在签名验证时也更快并且还更安全。它还将使用新的 OpenSSH 格式（OpenSSH 6.5+）而不是 PEM 格式保存私钥，Windows10 中的 OpenSSH 最先支持的也是 ed25519 类型的密钥。
使用 rsa 加密方式的示例：
```bash
$ ssh-keygen -t rsa -C "注释" -b 4096 
Generating public/private rsa key pair. 
# 指定密钥文件名称；直接回车则使用默认名称 id_rsa 
Enter file in which to save the key (/home/xxx/.ssh/id_rsa):
# 输入密码(一般不输入密码，直接回车) 
Enter passphrase (empty for no passphrase): 
# 再次输入密码 
Enter same passphrase again: 
Your identification has been saved in /home/fan/.ssh/FDGitHub_rsa. 
Your public key has been saved in /home/xxx/.ssh/id_rsa.pub. The key fingerprint is: 
***********************
# 注意在其他地方导入公钥时一定要将公钥文件中的 *全部内容* 都导入，包括末尾你的邮箱。 
```
使用 ed25519 加密方式生成密钥的示例：
```bash
ssh-keygen -t ed25519 -C "注释" # 默认的密钥文件中将带有ed25519，比如： ~/.ssh/id_ed25519 ~/.ssh/id_ed25519.pub 
```
**公钥**是一串很长的字符；为了便于肉眼比对和识别，所以有了指纹这东西；指纹位数短 ，更便于识别且与公钥一一对应。
公钥加密指纹 fingerprint 有两种形式：
* 之前的十六进制形式：`16:27:ac:a5:76:28:2d:36:63:1b:56:4d:eb:df:a6:48`
* 现在使用 sha256 哈希值并且使用 base64 进行格式 ：`SHA256:nThbg6kXUpJWGl7E1IGOCspRomTxdCARLviKw6E5SY8`
## 参考文章
[ssh和ssh服务](https://junmajinlong.com/linux/ssh/)