---
title: Go语言基础
tags:
  - golang
update: 2025-04-05
---
## 环境配置
### Linux下go环境安装
在官网上安装源码`.tar.gz`文件
将文件解压到系统中
```shell
sudo tar -xzf go1.xx.xx.linux=amd64.tar.gz -C /usr/local/src/
```
配置环境变量
在 `~/.bashrc`中添加以下几行
```shell
export GOPATH=$HOME/go
export PATH=$PATH:/usr/local/src/go/bin:$GOPATH/bin
export GO111MODULE=on
export GOPROXY=https://goproxy.cn
```
### go语言特性
静态编译型语言
- 静态：强类型，在编译的时候就确定
- 编译型：相对于解释型少一个解释器，直接由源代码编译得到二进制程序
### 第一个go语言程序
```go
// 每一个可执行的 golang 程序必定具备一个 main 包，并在该 main 包下具有执行函数 main 的 go 文件
package main
 
// HelloGo.go
// 基于图灵 API 一个简单的聊天机器人
 
// 引入相关依赖
import (
 "bytes"
 "encoding/json"
 "fmt"
 "io/ioutil"
 "math/rand"
 "net/http"
)
 
// 请求体结构体
type requestBody struct {
 Key string  `json:"key"`
 Info string  `json:"info"`
 UserId string  `json:"userid"`
}
 
 
// 结果体结构体
type responseBody struct {
 Code int `json:"code"`
 Text string `json:"text"`
 List []string `json:"list"`
 Url string `json:"url"`
}
 
// 请求机器人
func process(inputChan <-chan string, userid string)  {
 for{
  // 从通道中接受输入
  input := <- inputChan
  if input == "EOF"{
   break
  }
  // 构建请求体
  reqData := &requestBody{
   Key: "792bcf45156d488c92e9d11da494b085",
   Info : input,
   UserId: userid,
  }
  // 转义为 json
  byteData,_ := json.Marshal(&reqData)
  // 请求聊天机器人接口
  req, err := http.NewRequest("POST",
   "http://www.tuling123.com/openapi/api",
   bytes.NewReader(byteData))
 
  req.Header.Set("Content-Type", "application/json;charset=UTF-8")
 
  client := http.Client{}
  resp, err := client.Do(req)
 
  if err != nil {
   fmt.Println("Network Error!")
  }else {
   // 将结果从 json 中解析并输出到命令行
   body, _ := ioutil.ReadAll(resp.Body)
   var respData responseBody
   json.Unmarshal(body, &respData)
   fmt.Println("AI: " + respData.Text)
  }
  resp.Body.Close()
 }
}
 
func main()  {
 
 var input string
 fmt.Println("Enter 'EOF' to shut down: ")
 // 创建通道
 channel := make(chan string)
 // main 结束时关闭通道
 defer close(channel)
 // 启动 goroutine 运行机器人回答线程
 go process(channel, string(rand.Int63()))
 
  for {
   // 从命令行中读取输入
   fmt.Scanf("%s", &input)
   // 将输入放到通道中
   channel <- input
   // 结束程序
   if input == "EOF"{
    fmt.Println("Bye!")
    break
   }
 
  }
 
}
```
### 编译工具
1. ​go run​命令直接编译执行：`go run HelloGo.go​`
2. ​go build​ 命令先编译得到可执行文件
    1. ​`go build -o HelloGo HelloGo.go`​ 或者 `go build HelloGo.go​` 会生成一个`HelloGo`可执行文件。
## 基本语法
### 变量声明和初始化
#### 基本样式
1. ​var name TYPE​
2. ​var name TYPE = 表达式​
3. ​var a = 100​ 或 b:= "hello"​
> 注意：:=​ 不能用于全局变量的声明和初始化,同时其左值中的变量最少有一个变量必须是未定义过的变量
#### 多重赋值
交换a,b的值可以使用 a,b = b,a​
#### 匿名变量
函数使用多返回值时，使用 a, _ :=getName()​ _ 为匿名变量，不占用命名空间和内存
### 数据类型
#### 整型
- 按长度：int8,int16,int32,int64
- 按有无符号：uint8,uint16,uint32,uint64
#### 浮点型
两种：float32和float64
#### 布尔型
true和fasle
> 注意：bool与整型不能转换，bool型不能参与数值运算
#### 字符串型
String
>注意遍历字符串的时候可以以byte和rune两种方式，具体参考[字符类型：byte和rune](http://c.biancheng.net/view/18.html#:~:text=Go%E8%AF%AD%E8%A8%80%E5%AD%97%E7%AC%A6%E7%B1%BB%E5%9E%8B%EF%BC%88byte%E5%92%8Crune%EF%BC%89%201%20%E4%B8%80%E7%A7%8D%E6%98%AF%20uint8%20%E7%B1%BB%E5%9E%8B%EF%BC%8C%E6%88%96%E8%80%85%E5%8F%AB%20byte%20%E5%9E%8B%EF%BC%8C%E4%BB%A3%E8%A1%A8%E4%BA%86%20ASCII,UTF-8%20%E5%AD%97%E7%AC%A6%EF%BC%8C%E5%BD%93%E9%9C%80%E8%A6%81%E5%A4%84%E7%90%86%E4%B8%AD%E6%96%87%E3%80%81%E6%97%A5%E6%96%87%E6%88%96%E8%80%85%E5%85%B6%E4%BB%96%E5%A4%8D%E5%90%88%E5%AD%97%E7%AC%A6%E6%97%B6%EF%BC%8C%E5%88%99%E9%9C%80%E8%A6%81%E7%94%A8%E5%88%B0%20rune%20%E7%B1%BB%E5%9E%8B%E3%80%82%20rune%20%E7%B1%BB%E5%9E%8B%E7%AD%89%E4%BB%B7%E4%BA%8E%20int32%20%E7%B1%BB%E5%9E%8B%E3%80%82) 默认for range遍历使用rune方式
#### 类型断言
```go
x.(T)
```
- 断言x不为nil且x为T类型
- 如果T不是接口类型，则该断言x为T类型
- 如果T类接口类型，则该断言x实现了T接口
> 直接赋值的方式，如果断言为true则返回该类型的值，如果断言为false则产生runtime panic；j这里赋值直接panic 不过一般为了避免panic，通过使用ok的方式
```go
func main() {
    var x interface{} = 7
    j, ok := x.(int32)
    if ok {
        fmt.Println(reflect.TypeOf(j))
    } else {
        fmt.Println("x not type of int32")
    }
}
```
另外一种就是variable.(type)配合switch进行类型判断
```go
func main() {
    switch v := x.(type) {
    case int:
        fmt.Println("x is type of int", v)
    default:
        fmt.Printf("Unknown type %T!\n", v)
    }
}
```
#### 泛型
[泛型参考链接](https://juejin.cn/post/7080938405449695268)
### 指针
具体内容和C语言差不多，只不过限制了指针类型的偏移和运算能力，增加了自动垃圾回收机制
【实例】使用flag从命令行中读取参数
```go
package main
import (
"flag"
"fmt"
)
func main(){
//参数以此是命令行参数的名称，默认值，提示
surname := flag.String("surname","王","您的姓")
var personalName string
flag.StringVar(personalName,"personalName","小二","您的名")
id := flag.Int("id",0,"您的id")
flag.Parse()
fmt.Printf("I am %v %v,and my id is %v\n",*surname,personalName,*id)
}
```
在命令行中输入 go run Flag.go -surname="苍" -personalName="小屋" -id=100​ 得到输出：I am 苍 小屋，and my id is 100​
Flag支持
```shell
-id=100
--id=100
-id 100
--id 100
```
### 常量与类型别名
#### 常量
使用const关键字
#### 类型别名
- 定义类型别名：`type name = TYPE`
- 定义新类型：`type name TYPE`
### 分支循环
#### 条件语句
- `If else`条件语句注意与if匹配的`"{"`和`if`在同一行；`else`必须与上一个分支的`"}"`位于同一行
- `switch`语句不需要用`break`，可以用`fallthrough`关键字连接两个`case`；可以对字符串和复杂表达式进行判断；可以写成`if-else`类型：`switch`后没有变量，`case`后接条件判断表达式。
#### 循环
只有一种`for`循环
```go
for init;condition;end{
循环体
}
```
## 常见容器
### 数组
声明初始化的几种方式
​`var name [size]TYPE​`
`​name := [...]string{"xiaoming","xiaohong","xiaoli"}​`
​`name := new([size]TYPE)​`
使用指针操作数组时不支持偏移和运算。
### 切片
#### 从原生数组中生成切片
​`slice := source[begin:end]​`包括`begin`不包括`end`；修改切片相当于修改数组
#### 动态创建切片
​`make([]TYPE,size,cap)​`得到的切片会被初始化为其类型的初始值
#### 声明新的切片
​`var name []TYPE​`相当于声明数组时没有设置大小
#### 向切片中添加元素
使用append函数
`size<=cap`时：更新原数组
`size>cap`时：申请新空间
> 可以使用 `copy(destSli,srcSli []TYPE)​` 复制切片
### 列表与字典
#### 列表
双向有序链表，每个节点可以是不同的数据类型
引入`container/list`包
初始化：`var name list.List​ or name := list.New()​`
对应函数：
- `PushBack(element)`
- `PushFront(element)`
- `Remove(element)`
- 头元素：`Front()`
- 下一个元素：`Next()`
#### 字典
初始化
```go
//声明
classMates1 := make(map[int]string)
//添加映射关系
classMates1[0] = "小明"
//在声明的时候初始化
classMates2 := map[int]string{
    0:"小明"，
    1:"小红"，
    2:"小张"，
}
```
判断map中某个键是否存在
​`value,ok := classmate2[1]​ if 存在 then ok为true.`
### 容器遍历
使用`for-range`遍历
```golang
for k,v := range nums{
//循环体
}
```
> 注意：遍历循环体中对k，v修改不会影响到原容器的内容
## 函数与接口
### 函数的声明和参数传递
具体样式
```go
func name(params)(return params){
 function body
}
```
可返回多个参数
```go
func swap(x, y string) (string, string) {
   return y, x
}
x,y=swap(x,y)
```
> 注意：如果函数需要在包外的代码使用，则函数名要大写
### 匿名函数和闭包
匿名函数：初始化和调用一起
主要用于回调函数和闭包
#### 回调函数
函数作为参数传递，实现回调。
```go
package main
import "fmt"

// 声明一个函数类型
type cb func(int) int

func main() {
    testCallBack(1, callBack)
    testCallBack(2, func(x int) int {
        fmt.Printf("我是回调，x：%d\n", x)
        return x
    })
}

func testCallBack(x int, f cb) {
    f(x)
}

func callBack(x int) int {
    fmt.Printf("我是回调，x：%d\n", x)
    return x
}
```
#### 闭包
携带状态的函数叫做闭包，包的是函数和变量环境
```go
package main

import "fmt"

func getSequence() func() int {
   i:=0
   return func() int {
      i+=1
     return i  
   }
}

func main(){
   /* nextNumber 为一个函数，函数 i 为 0 */
   nextNumber := getSequence()  

   /* 调用 nextNumber 函数，i 变量自增 1 并返回 */
   fmt.Println(nextNumber())
   fmt.Println(nextNumber())
   fmt.Println(nextNumber())
   
   /* 创建新的函数 nextNumber1，并查看结果 */
   nextNumber1 := getSequence()  
   fmt.Println(nextNumber1())
   fmt.Println(nextNumber1())
}
```
### 接口声明和嵌套
接口：调用方和实现方约定的一种合作协议。调用者不关心接口的实现方式，实现者通过接口暴露自己的内在功能。每个接口有一个或多个方法
> 注意：只有当接口名和方法名的首字母都为大写的时候，表示公开，包外可以被访问
```go
type interfaceName interface{
    method1(params)(return params)
    method2(params)(return params)
    ...
}
```
接口是可以嵌套的
### 函数体实现接口
go语言中的所有类型都可以实现接口
首先定义一个接口：
```go
type Printer interface{
    Print(interface{})
}
```
将函数定义为类型之后实现接口：
```golang
type FuncCaller func(p interface{})
//实现方法
func (funcCaller FuncCaller) Print(p interface{}){
    //调用函数本体
    funcCaller(p)
}
```
具体使用：
```go
func main(){
    var printer Printer
    printer = FuncCaller(func(p interface{}){
        fmt.Println(p)  
    })
    printer.Print("Golang is good!")
}
```
## 结构体和方法
### 结构体定义
样式
```go
type structName struct{
    value1 valueType1
    value2 valueType2
    ...
}
```
> 注意：结构体公开则其名首字母大写；字段公开则字段名首字母大写
### 结构体的实例化和初始化
#### 实例化
声明实例化
```go
var p1 Person
p1.Name = "xiaoming"
```
函数实例化
```go
p2:= new(Person)//指针类型
p2.Name = "xiaohong"
```
取址实例化
```go
p3 := &Person{}
p3.Name = "xiaozhang"
```
#### 初始化
```go
p4 := &Person{
    Name:"xiaowang",
    Birth:"2004-01-01"
}
//如果所有字段都初始化，可以按顺序省略字段名
```
### 方法和接收器
方法定义样式
```go
func (recipient recipientType) methodName(params)(return params){
function body
}
```
> 注意：接收器最好选用指针类型
### 结构体实现接口
接口Cat,Dog定义+实现结构体CatDog定义+接口（方法）实现
具体实现：
```go
catDog := &CatDog{}
//声明一个Cat接口，将catDog指针类型赋值给cat
var car Cat
cat = catDog
cat.CatchMouse()
```
### 内嵌和组合
结构体内部可以内嵌结构体，也可有匿名字段
#### 继承
```go
type Animal struct {
    name string
}
type Dog struct {
    Feet    int    
    *Animal //通过嵌套匿名结构体实现继承
}
func main() {    
    d := &Dog{            
        Feet: 4,            
        Animal: &Animal{                     
            name: "狗蛋",            
        },    
    }
}
```
