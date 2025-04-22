---
title: 构建GoWeb服务器
tags:
  - golang
update: 2025-04-05
---
## http协议
HTTP协议没有状态，即同一个客户端两次请求没有对应关系，为了解决这个问题引入session和cookie的概念
### HTTP Request
http请求由请求行（Request Line）和请求头部(Header)、空行和请求数据等4个部分组成。
- 请求行：方法 `URL` 版本 `cr lf（\r\n）`
- 请求头部：字段名 字段值 `cr lf`  
    字段名 字段值 `cr lf`  
    ...
- 空行：`cr lf`
- 请求数据（请求体）：（其他数据）
### HTTP Response
服务器接收到请求之后会做出响应，也是四部分组成：状态行、响应头、空行、响应体
- 状态行：协议版本号 状态码 `cr lf`
- 响应头：（客户端可以使用的一些信息如Date（生成响应的日期）、`Content-Type`（MIME类型及编码格式）和Connection（默认是长连接）等等）字段名 字段值 `cr lf`  
    字段名 字段值 `cr lf`  
    ...
- 空行：`cr lf`
- 响应体：（响应正文）
不同状态码对应信息：
- 1XX：接收的请求正在处理
- 2XX：请求正常处理完毕
- 3XX：需要进行附加操作以完成请求
- 4XX：服务器无法处理请求
- 5XX：服务器处理请求出错
## 访问web站点的过程
1. 输入`url`之后，浏览器先访问`DNS`服务器获取需访问服务器的真实ip
2. 找到真实`ip`对应的服务器，建立`tcp`连接
3. 浏览器发送`HTTP Request`
4. 服务器接受到`HTTP Request`之后响应`HTTP Response`给浏览器
5. 浏览器接收完`HTTP Response`之后断开`tcp`连接
## 使用Go语言构建服务器
【实例】
```go
package main
import (
    "fmt"
    "strings"
    "net/http"
    "log"
    )
func main() {
    http.HandleFunc("/hello", handler)    //设置访问路由
    err := http.ListenAndServe(":8080", nil)    //设置监听窗口
    if err != nil {
        log.Fatal("ListenAndServe:",err)
    }
}
func handler(w http.ResponseWriter, r *http.Request) {
    _ = r.ParseForm()    //解析参数，默认不会解析
    fmt.Println(r.Form)    //打印表单信息
    fmt.Println("Path:",r.URL.Path)    //打印路由
    fmt.Println("Host:",r.Host)    //打印ip/端口
    for k,v := range r.Form{
        fmt.Println("key:",k)
        fmt.Println("val:",strings.Json(v,""))
    }
    _,_ = fmt.Fprintf(w, "Hello Web,%s!",r.Form.Get("name"))    //将内容写到http.ResponseWriter中，发送到客户端
}
/*
    在浏览器中访问http://localhost:8080/hello?name=Extious
    即可得到响应结果
*/
```
### 接收和处理请求
#### Web工作中的几个概念
`net/http`标准库中由客户端和服务端两个部分
- 服务端：`Server,ServerMux,Handler/HandlerFunc,Header,Request,Cookie`
- 客户端：`Client,Response,Header,Request,Cookie`
Conn:表示用户每次请求链接
`http`包服务端执行流程：
1. 创建`Listen Socket`，监听指定的端口，等待客户端的请求
2. `Listen Socke`t接收到请求，得到`Client Socket`，通过`Client Socket`与客户端通信
3. 服务端处理请求：从`Client Socket`中读取请求体，交给`Handler`处理，将响应体通过`Client Socket`写给客户端
### 处理器处理请求
流程：
1. `ListenAndServe`进行监听：`net.Listen("tcp",addr)`
2. 接收请求并创建连接`Conn：srv.Serve(l net.Listener)`：进入循环`{rw := Accept();c := srv.NewConn();go c.serve()}`
3. 处理链接`conn.serve()`：分析请求，映射`url`
### 解析请求体
具体可见"使用Go语言构建服务器"中的【实例】
### 返回响应体
主要通过接口`ResponseWriter`接口中的方法：
```go
type ResponseWriter interface{
    Header() Header    //通过set方法可以修改请求头中的某字段的内容
    Write([]byte) (int,err)    //使用json.Marshal（mapname）;w.Write(json)设置响应体
    WriteHeader(statusCode int)    //修改状态码：默认是200
}
```
## 实践案例：Golang Web 框架 Gin 实践
### Gin安装
​`go get -u github.com/gin-gonic/gin​`
### 使用方式
直接引入：
```go
import(
    "github.com/gin-gonic/gin"
    "net/http"//可选，当使用http.StatusOK（200的状态码）这类的常量的时候需引入
）
```
### 使用Gin实现HTTP服务器
```go
package main
import "github.com/gin-gonic/gin"
func main(){
    router := gin.Default()    //使用Default方法创建路由handler
    router.GET("/ping",func(c *gin.Context){    //通过http方法绑定路由规则和路由函数，这里是匿名函数
        c.JSON(200, gin.H{    //gin把request和response封装在了一起：gin.Context
            "message":"pong",
        })
    })
    router.Run(:8000)    //通过Run方法启动监听路由
}
```
### Restful API
常用`Restful`方法有：`GET,PUT,POST,DELETE`等
路由的一些使用技巧和方式：
比如：由中携带参数
```go
router.GET("/user/:name",func(c *gin.Context){
    name := c.Param("name")
    c.String(http.StatusOK,"Hello %s",name)
})
```
如上可以使用`c.Param(s)（"name"）`方法读取参数的值，但是gin不支持路由正则表达式，只有像 `/user/Extious​` 这个结构的路由才可以被匹配，而 `/user​ ,/user/​,/user/Extious/​`都不会被匹配。
gin还提供了`router`处理参数：
​`router.GET("/user/:name/action",func​`这个时候处理器可以匹配到 `/user/Extious/​,/user/Extious/Send​,/user/Extious​`
> 注意：路由参数是指API参数和URL参数不同，URL参数是路由之后 `/api?name="Extious"​` 里边`name`这种，需要用到`Query()`等方法遍历到
### gin中间件
中间件的意思是对一组接口的统一操作，常用于：记录`log`，错误`handler`，对部分接口的鉴权
```go
package main
import (
    "fmt"
    "net/http"
    "gin-http/middleware"
    "gin-http/model"
)
func main() {
    router := gin.Default()
    router.Use(AuthMiddleware())
    router.GET("/user", func(c *gin.Context) {
        user := model.User{ID: 1, Name: "test"}
        c.JSON(http.StatusOK, gin.H{"user": user})
    })
    router.Run(":8080")
}
func AuthMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        // 从请求头中获取token值
        token := c.GetHeader("Authorization")
        // 验证token是否有效，这里仅做示例，实际应用中需要调用相关接口进行验证
        if token == "valid_token" {
            c.Next() // 验证通过，继续执行后续中间件和请求处理方法
        } else {
            c.String(http.StatusUnauthorized, "Token is invalid") // 验证失败，返回错误信息
            c.Abort() // 终止请求处理，不再执行后续中间件和请求处理方法
        }
    }
}
```
## 服务端数据存储
MySQL采用gorm的一系列接口