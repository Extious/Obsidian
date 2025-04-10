---
title: MySQL常见问题
tags:
  - mysql
update: 2025-04-06
---
## Access denied for user 'root'@'localhost'
在运行 MySQL 5.7（及更高版本）的 Ubuntu 系统中，MySQL root 用户默认设置为使用 auth_socket 插件进行身份验证，而不是使用密码。在许多情况下，这可以提供更高的安全性和可用性，但当您需要允许外部程序（例如，vscode mysql插件）访问用户时，它也会使事情变得复杂。为了使用密码以 root 身份连接到 MySQL，您需要将其身份验证方法从 auth_socket 切换为mysql_native_password。
```bash
sudo mysql    #进入mysql终端
```

```bash
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_new_password';    #修改密码的同时将验证方式改为密码验证
FLUSH PRIVILEGES    #刷新特权
```