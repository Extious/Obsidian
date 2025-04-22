---
title: Redis基础
tags:
  - redis
update: 2025-04-06
---
## 介绍与安装
Redis是一个开源的内存中的数据结构存储系统，它可以用作：数据库、缓存和消息中间件。
Redis是用C语言开发的一个开源的高性能键值对(key-value)数据库，官方提供的数据是可以达到100000+的QPS（每秒内查询次数）。它存储的value类型比较丰富，也被称为结构化的NoSql数据库。
NoSql（Not Only SQL），不仅仅是SQL，泛指 **非关系型数据库** 。NoSql数据库并不是要取代关系型数据库，而是关系型数据库的补充。
### 下载安装
[Windows版redis下载地址](https://github.com/microsoftarchive/redis/releases)
[Linux版redis下载地址](https://download.redis.io/releases/)
windows中下载的.zip包直接解压即可
## redis配置
### 配置文件：
* Windows：redis.windows.conf
* Linux：redis.conf
### 配置参数：
* daemonize：yes将redis控制为后台运行，Windows不支持
* Requirepass foobared：配置密码，默认为注释的状态
* bind：允许远程连接的客户端ip，默认为127.0.0.1，可以注释掉允许所有远程客户端连接
启动redis服务：`./redis-server.exe ./redis.windows.conf`；也可以直接双击.exe文件启动
### 可设置参数：
1.  -h：指定连接的Redis服务的ip地址
2.  -p：指定连接的Redis服务的端口号
3.  -a：指定连接的Redis服务的密码
## redis数据类型及其命令行操作
### 类型：
redis中的数据全是key-value结构，key类型都是string
value可以是：
* 字符串string：普通常用
* 哈希hash：适合存储对象
* 列表list：按照插入顺序排序，可有重复元素
* 集合set：无序集合，没有重复元素
* 有序集合sorted set/zset：每个元素关联一个分数（score），根据分数升序排序，没有重复元素
**参考图片：**
![image](https://picture.zhaozhan.site/redis-types.png)
### 常用命令：
#### value为string
```bash
SET key value
#设置只当的key值
GET key
#获取指定key的值
SETEX key seconds value
#设置指定key的值，并把过期时间设为seconds秒
SETNX key value
#只在不存在key的时候设置key的值
```
**更多命令参考**[Redis中文网](https://www.redis.net.cn/)
#### 通用
```bash
KEYS pattern
#查找所有符合给定模式（pattern）的key
EXISTS key
#检查给定key是否存在
TYPE key
#返回key所存储的值的类型
TTL key
#返回给定key的剩余时间（TTL：time to live），以秒为单位
DEL key
#在key存在时删除key
```
## go语言操作redis
### 下载依赖包
两种redis方式支持go操作
1. `go get -u github.com/go-redis/redis`
2. `go get -u github.com/garyburd/redigo/redis`
只记录第一种
### 启动服务和监控
双击 `redis-server.exe` 和 `redis-cli.exe` 启动服务
在客户端命令行输入命令 `monitor` 开启监控
开启监控后所有操作都会在客户端命令行中打印出来
### go连接Redis
```go
import (
    "fmt"
    "github.com/go-redis/redis"
)
func ConnRedis() {
    rd := redis.NewClient(&redis.Options{
        Addr: "127.0.0.1:6379", // url
        Password: "",
        DB:0,   // 0号数据库
    })
    result, err := rd.Ping().Result()
    if err != nil {
        fmt.Println("ping err :",err)
        return
    }
    fmt.Println(result)
}
```
### 简单操作
#### Zset
* 获取zset长度
`lenth, err := client.ZCard(context.Background(), key).Result()`
* 根据score删除部分元素
`_, err = client.ZRemRangeByRank(context.Background(), key, 0, ` *`ZsetShrinkNum`* `-1).Result()`
* 添加元素
```go
_, err = client.ZAdd(context.Background(), key, &redis.Z{
    Score:  float64(messageID),
    Member: messageID,
}).Result()
```
参考资料：
go语言redis方法：[https://juejin.cn/post/7202521955366879288](https://juejin.cn/post/7202521955366879288)
go语言配置redis：[https://blog.csdn.net/lena7/article/details/120828397](https://blog.csdn.net/lena7/article/details/120828397)