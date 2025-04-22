---
title: WebSocket
tags:
  - websocket
update: 2025-04-05
---
## 概述
WebSocket 协议提供了一种全双工的通信机制, 服务端可以主动向客户端推送数据, WebSocket 协议采用了 HTTP 协议来握手, 与 HTTP 使用相同的默认端口, 这一切都是为了兼容现有的 HTTP 组件或代理, 但 WebSocket 与 HTTP 是相互独立的协议, 二者并不存在上下的层级关系, WebSocket 的正式协议文档为 [RFC 6455](https://link.zhihu.com/?target=https%3A//tools.ietf.org/html/rfc6455), 本文全面讨论 WebSocket 协议的设计与工作原理
## 握手
### 客户端请求upgrade
WebSocket 协议的第一步是进行握手, WebSocket 握手采用 HTTP Upgrade 机制, 客户端可以发送如下所示的结构发起握手 (请注意 WebSocket 握手只允许使用 HTTP GET 方法):
```
GET /chat HTTP/1.1
Host: server.example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Origin: http://example.com
Sec-WebSocket-Protocol: chat, superchat
Sec-WebSocket-Version: 13
```
* 在 HTTP Header 中设置 Upgrade 字段, 其字段值为 websocket, 并在 Connection 字段指示 Upgrade
*  | Sec-WebSocket-Key |, 必传, 由客户端随机生成的 16 字节值, 然后做 base64 编码, 客户端需要保证该值是足够随机, 不可被预测的 (换句话说, 客户端应使用熵足够大的随机数发生器), 在 WebSocket 协议中, 该头部字段必传, 若客户端发起握手时缺失该字段, 则无法完成握手**
* | Sec-WebSocket-Version |, 必传, 指示 WebSocket 协议的版本, [RFC 6455](https://link.zhihu.com/?target=https%3A//tools.ietf.org/html/rfc6455) 的协议版本为 13, 在 [RFC 6455](https://link.zhihu.com/?target=https%3A//tools.ietf.org/html/rfc6455) 的 Draft 阶段已经有针对相应的 WebSocket 实现, 它们当时使用更低的版本号, 若客户端同时支持多个 WebSocket 协议版本, 可以在该字段中以逗号分隔传递支持的版本列表 (按期望使用的程序降序排列), 服务端可从中选取一个支持的协议版本
*  | Sec-WebSocket-Protocol |, 可选, 客户端发起握手的时候可以在头部设置该字段, 该字段的值是一系列客户端希望在于服务端交互时使用的子协议 (subprotocol), 多个子协议之间用逗号分隔, 按客户端期望的顺序降序排列, 服务端可以根据客户端提供的子协议列表选择一个或多个子协议
*  | Sec-WebSocket-Extensions |, 可选, 客户端在 WebSocket 握手阶段可以在头部设置该字段指示自己希望使用的 WebSocket 协议拓展
### 服务端响应
服务端若支持 WebSocket 协议, 并同意握手, 可以返回如下所示的结构:
```
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
Sec-WebSocket-Protocol: chat
Sec-WebSocket-Version: 13
```
*  | Sec-WebSocket-Accept |, 必传, 客户端发起握手时通过 | Sec-WebSocket-Key | 字段传递了一个将随机生成的 16 字节做 base64 编码后的字符串, 服务端若接收握手, 则应将该值与 WebSocket 魔数 (Magic Number) &quot;258EAFA5-E914-47DA- 95CA-C5AB0DC85B11&quot; 进行字符串连接, 将得到的字符串做 SHA-1 哈希, 将得到的哈希值再做 base64 编码, 最终的值便是该字段的值；当客户端收到服务端的握手响应后, 会做同样的运算来校验该值是否符合预期, 以便于判断服务端是否真的支持 WebSocket 协议
*  | Sec-WebSocket-Protocol |, 可选, 若客户端在握手时传递了希望使用的 WebSocket 子协议, 则服务端可在客户端传递的子协议列表中选择其中支持的一个, 服务端也可以不设置该字段表示不希望或不支持客户端传递的任何一个 WebSocket 子协议
*  | Sec-WebSocket-Extensions |, 可选, 与 Sec-WebSocket-Protocol 字段类似, 若客户端传递了拓展列表, 可服务端可从中选择其中一个做为该字段的值, 若服务端不支持或不希望使用这些扩展, 则不设置该字段
*  | Sec-WebSocket-Version |, 必传, 服务端从客户端传递的支持的 WebSocket 协议版本中选择其中一个, 若客户端传递的所有 WebSocket 协议版本对服务端来说都不支持, 则服务端应立即终止握手, 并返回 HTTP 426 状态码, 同时在 Header 中设置 | Sec-WebSocket-Version | 字段向客户端指示自己所支持的 WebSocket 协议版本列表
若客户端校验服务端的握手响应通过, 则 WebSocket 握手阶段完成, 接下来双方就可以进行 WebSocket 的双向数据传输了
## WebSocket 数据帧 (frame)
具体[参考文章](https://zhuanlan.zhihu.com/p/407711596)
## 总结
WebSocket 协议主要为了解决 HTTP/1.x 缺少双向通信机制的问题, 它使用 TCP 作为传输层协议, 使用 HTTP Upgrade 机制来握手, WebSocket 使用与 HTTP 相同的 80 (WebSocket over TCP) 和 443 (WebSocket over TLS) 端口, 它与 HTTP 是相互独立的协议, 二者没有上下的分层关系, 了解更详细的 WebSocket 细节可以阅读 **[RFC 6455](https://link.zhihu.com/?target=https%3A//tools.ietf.org/html/rfc6455)