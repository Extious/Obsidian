---
title: Docker
tags:
  - docker
update: 2025-04-06
---
## Ubuntu安装
### ubuntu配置代理
#### 参考文章
[yangchnet.github.io/Dessert/posts/env/安装与配置clash/](https://yangchnet.github.io/Dessert/posts/env/%E5%AE%89%E8%A3%85%E4%B8%8E%E9%85%8D%E7%BD%AEclash/)
[www.noseeflower.icu/](https://www.noseeflower.icu/)
[zhuanlan.zhihu.com/p/15657792425](https://zhuanlan.zhihu.com/p/15657792425)
#### 修改后文件
```plaintext
# /etc/systemd/system/clash.service
[Unit]
Description=Clash Proxy Service
After=network.target
[Service]
Type=simple
ExecStart=/usr/local/bin/clash -f /home/zhaozhan/.config/clash/config.yaml
Restart=always
RestartSec=3
[Install]
WantedBy=multi-user.target
```
#### 测试效果
`curl -I https://www.google.com`
![image](https://picture.zhaozhan.site/docker-proxy.png)
### Docker配置
#### 安装docker
[docs.docker.com/engine/install/ubuntu/](https://docs.docker.com/engine/install/ubuntu/)
#### 配置代理
```bash
sudo vim /etc/systemd/system/docker.service.d/http-proxy.conf
```
文件中输入以下内容：
```conf
[Service]
Environment="HTTP_PROXY=127.0.0.1:7890"
Environment="HTTPS_PROXY=127.0.0.1:7890"
Environment="NO_PROXY=localhost,127.0.0.1,docker-registry.example.com,.corp"
```
终端输入：
```bash
sudo systemctl daemon-reload
sudo systemctl restart docker
```