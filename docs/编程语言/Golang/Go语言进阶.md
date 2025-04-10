---
title: Go语言进阶
tags:
  - golang
update: 2025-04-05
---
# 依赖管理
## 包管理
> 注意：一个包对应一个目录，一个目录下不同文件之间可以相互公开，只有不同的包之间需要大写使其公开。
使用import之后编译运行一个文件就会连带着编译其import的包
## GOPATH
一个目录包括三个子目录
- `src`，不同的包的源代码
- `pkg`，编译后的类库
- `bin`，编译后的可执行程序
​`go install​` 命令将编译之后的结果文件：.a应用包或可执行文件导入到pkg或bin中
​`go get​` 命令将源码直接导入`src`中然后执行 `go install​`
## Go Modules
`gopath`改进之后通过go.mod文件进行包的管理
通过命令 `go mod init [module name]​` 生成`go.mod`文件
go.mod文件样例：
```go
module name
go 1.20
require github.com/longjoy/micro-go-book v0.0.1
```
可以通过 `go mod tidy​`命令进行依赖的更新
最终下载的第三方库保存在`GOMODCACHE`中，即`GOPATH/pkg/mod`中
​![image](https://picture.zhaozhan.site/go-mod.png)​
# 反射基础
一般不会自己写反射代码，理解原理即可
提供运行时对代码的访问和修改的能力
两个概念:
- Type：主要表示被反射变量的类型信息。
- Value：表示被反射变量的类型信息
go语言反射的实现主要位于reflect包中
## reflect.Type类型对象
通过 `ypeofname := reflect.Typeof(type name)​`方法获取一个变量的类型信息，存到一个`reflect.Type`的类型的变量中。
通过`typeofname.kind()`获得`type name`的种类（struct 等等）而`typeofname`是指哪个包里定义的类型`packagename.typename`
```go
// Kind表示类型所表示的特定类型。
// 零类型不是有效类型。
type Kind uintconst (
    Invalid Kind = iota
    Bool
    Int
    Int8
    Int16
    Int32
    Int64
    Uint
    Uint8
    Uint16
    Uint32
    Uint64
    Uintptr
    Float32
    Float64
    Complex64
    Complex128
    Array
    Chan
    Func
    Interface
    Map
    Ptr
    Slice
    String
    Struct
    UnsafePointer
)
```
### 类型对象`reflect.StructField`和`reflect.Method`
#### `StructField`
reflect中存在`structfield`类型用于存储：结构体内字段的类型信息
以上述通过`typeof(type name)`方法获得的一个结构体类型对象为接收器可以使用以下三个方法获得该结构体对象下属的字段的`structfield`类型信息：
```go
//获取一个结构体内的字段数量
NumField() int
//根据index获取结构体内的成员字段类型对象
Field(i int) StructField
//根据字段名获取结构体内的成员字段类型对象
FieldByName(name string) (StructField, bool)
```
`StructField`中的内容
```go
type StructField struct{
    //成员字段名称
    Name string
    //成员字段Type,reflect.Type类型
    Type Type
    //Tag,主要描述字段的额外信息，如json序列化和对象映射的时候使用
    Tag StructTag
    //字段偏移
    Offset uintptr
    //成员字段的Index
    Index []int
    //成员字段是否公开
    Anonymous bool
}  
```
#### Method
reflect中还存在Method类型用于存储：接口下方法的方法类型对象
go语言中可以声明一个接口变量，并赋值以接收器：var person Person = &Hero{}​,其中Person是一个接口，Hero是一个结构体。
通过相同的方法 `typeOfPerson := reflect.Typeof(person)​`可以获得一个接口Person的类型对象。
而以接口类型对象为接收器存在以下方法来获取Method类型对象
```go
//根据index查找方法
Method(int) Method
//根据方法名查找方法
MethodByName(string) (Method, bool)
//获取类型中的公开的方法数量
NumMethod() int
```
Method内的基本信息
```go
type Method struct{
    //方法名
    Name string
    //方法类型
    Type Type
    //反射对象，可用于调用方法
    Func Value
    //方法的index
    Index int
}  
```
`Method.Type`为`func`(接收器,剩余的原方法参数)
## reflect.Value反射值对象
使用上述的`Type`类型对象，我们只能查看类型信息，不能对变量的值进行查看和修改，所以有了`reflect.Value`反射值对象。
可以通过`reflect.ValueOf`获取反射变量的信息Value，通过Value对变量的值进行查看和修改。
### 获取变量值
通过`Value.Interface()`方法获取变量的值
可以使用`reflect.New(类型对象)`创建一个相同类型的新变量，值以`Value`对象的形式返回。
### 改变变量值
对变量的修改可以通过方法`Value.Set方`法实现
例子如下：
```go
name := "小明"
valueOfName := reflect.ValueOf(&name)
valueOfName.Elem().Set(reflect.ValueOf("小红"))
fmt.Println(name)
```

> 注意：由于Value的值是原变量值的拷贝，即使`ValueOf(&name)`，也只是指向name指针的拷贝，要寻址到原变量要使用#Elem方法。

可以通过方法`#CanAddr`判断是否可以寻址
### 结构体value
对于结构体的反射值对象，可以通过`Value.CanSet`判断某字段是否公开可以改变，结构体的value同时也有类似type的一些方法：`#NumField`，`#FieldByIndex`，`#FieldByName`来获取字段的`value`
### 反射接口方法调用

使用函数 `func (v value) Call(in []value) []Value​`

```go
//声明接口以及确定其接收器
var person Person = &Hero{
    Name:"小红",
    Speed:"100",
}
valueOfPerson := reflect.ValueOf(person)
//获取sayHello函数
sayHelloMethod := valueOfPerson.MethodByName("sayHello")
//使用#Call方法调用
sayHelloMethod.Call([]reflect.Value{reflect.ValueOf("小张")})
```
也可以使用上边`type`中的`Method.func`调用，但要将接收器作为第一个参数传入
# 并发模型
## 并发与并行
- 并发：同一时间段内，多条指令在CPU上同时执行
- 并行：同一时刻上，多条指令在CPU上同时执行
## CSP并发模型
go语言实现两种并发模型
- 线程与锁并发模型：依赖于共享内存，程序出错不易排查
- CSP（通信顺序进程模型）：有两个关键概念
    - 并发实体：即执行线程，他们之间相互独立并发执行
    - 通道：并发实体之间使用通道发送信息
极易导致死锁
## 常见线程模型
线程是操作系统能够调度的最小单位分为用户线程和内核线程
- 用户线程：由用户空间的代码创建、管理和销毁，调度由用户空间的线程库完成
- 内核线程：由操作系统管理和调度，线程切换需要cpu切换为内核态
用户线程无法被操作系统感知，用户线程所属的进程或者内核线程才能被操作系统直接调度。
### 用户级线程模型
一个进程包含多个用户线程，对应一个内核线程
缺点：一个用户线程阻塞导致整个进程失去时间片
### 内核级线程模型
每个用户线程对应一个内核线程
缺点：线程切换从用户态到内核态资源消耗大
### 两级线程模型
上述两个模型相结合：一个进程对应多个内核线程，由进程中的调度器决定进程内的线程如何与申请的内核线程相对应。
## GMP线程模型
go语言中的MPG线程模型对两级线程模型进行改进：
- M：Machine，一个Machine对应一个内核线程，相当于内核线程在go语言进程中的映射
- P：Processor，go代码片段执行所需的上下文环境，用户代码逻辑处理器
- G：Goroutine，go代码片段的封装，是一种轻量级的用户线程
M，P共同构成了一个基本的运行环境，此时G0中的代码处于运行的状态，右边G队列处于待执行的状态。
当没有足够的M来和P组合为G提供运行环境时，Go语言会创建新的M，在很多时候M的数量可能比P多。在单个Go语言进程中，P的最大数量决定了程序的并发规模，且P的最大数量由程序决定，可以通过修改环境变量GOMAXPROCS和调用函数runtime.GOMAXPROCS来设定P的最大值。
# 并发实践
## 协程goroutine
**goroutine是go语言中的轻量级进程，在运行的时候由runtine管理，我们编写main函数也是运行在goroutine之上，可以通过 **go 表达式语句​ 来启动一个新的goroutine
表达式语句可以是内建函数，也可以是自定义的方法和函数（命名或匿名都可）
> 注意：go语言不同的goroutine间的代码次序并不代表真正的执行顺序（不清楚真正的调度顺序），主goroutine结束，其创建的goroutine如果还没有执行那么会被销毁。
### 对比OS线程
- os线程：固定栈内存：2MB
- goroutine：栈内存不固定，从2KB到1GB
### 示例
```go
package main

import (
        "fmt"
        "time"
)

func main() {
        arr := []int{1, 2, 3, 4}
        for _, v := range arr {
                go func() {
                        fmt.Printf("%d\t", v) //用的是协程外面的全局变量v。输出4 4 4 4
                }()
        }
        time.Sleep(time.Duration(1) * time.Second)
        fmt.Println()
        for _, v := range arr {
                go func(value int) {
                        fmt.Printf("%d\t", value) //输出1 4 2 3
                }(v) //把v的副本传到协程内部
        }
        time.Sleep(time.Duration(1) * time.Second)
        fmt.Println()
}
```
[goroutine协程关闭](https://zhuanlan.zhihu.com/p/597424646?utm_id=0)
## 通道channel
channel声明：
```go
var channelName chan T    //T为可传输数据类型
channelName <- val    //将val的值传到channelName中
val,ok := channel    //ok检查channel是否关闭
ch := make(chan T,sizeOfChan)    //使用make对channel进行初始化
```

> 注意：创建channel时如果指定channel的长度，那么有缓冲区，缓冲区未满时不阻塞，如果没有指定长度，那么只会往里边写入一次之后就会阻塞

【实例】不断从终端中获取数据
```go
package main
import(
    "bufio"
    "fmt"
    "os"
)
func printInput(ch chan string){
    for val := range ch {
        if val == "EOF"{
            break
        }
        fmt.Printf("Input is %s\n",val)
    }
}
func main(){
    ch := make(chan string)
    go printInput(ch)
    scanner := bufio.NewScanner(os.Stdin)
    for scanner.Scan(){
        val := scanner.Text()
        ch <- val
        if val == "EOF"{
            fmt.Println("End the game!")
            break
        }
    }
    defer close(ch)
}
```
### select
使用select可以从多个channel中读取数据：
```go
select {
case val := <- ch1:
    ...
case val := <- ch2:
    ...
case <- time.After(2 * time.Second):    //超时处理
    ...
}
```
## sync同步包

### 互斥锁：Mutex
```go
var lock sync.Mutex
lock.Lock()
lock.Unlock()
```
### 读写锁：RWMutex
接口：（允许多读单写，读写互斥）

```go
//写加锁
func (rw *RWMutex) Lock()
//写解锁
func (rw *RWMutex) Unlock()
//读加锁
func (rw *RWMutex) RLock()
//读解锁
func (rw *RWMutex) RUnlock()
```
### WaitGroup（并发等待组）
接口：
```go
//添加等待数量，传递负数表示任务减1
func (wg *WaitGroup) Add（delta int）
//等待数量减1
func (wg *WaitGroup) Done()
//使goroutine等待于此
func (wg *WaitGroup) Wait()
```
### map（并发安全字典）
原生的字典map多个`goroutine`同时添加`key-value`的时候可能会发生数据的丢失
go语言中有`sync.Map`提供以下接口：
```go
//根据key获取存储值
func (m *Map) Load(key interface{}) (value interface{},ok bool)
//设置key-value对
func (m *Map) Store(key, value interface{})
//如果key存在则返回key对应的value，否则设置key-value对
func (m *Map) LoadOrStore(key, value interface{}) (actual interface{},loaded bool)
//删除一个key以及对应值
func (m *Map) Delete(key interface{})
//无序遍历map
func (m *Map) Range(f func(key,value interface{}) bool)
```
# 标准库
参考：[go标准库中文文档](https://studygolang.com/pkgdoc)
## OS
读文件：
```go
//打开文件
fileObj,err := os.Open("./main.go")
//关闭文件
defer fileObj.Close()
//简单读文件
var tmp = make{[]byte,128}
n,err := fileObj.Read(tmp)
if err == io.EOF{
    return
}
//bufio读取文件(一行)
reader := bufio.NewReader(fileObj)
line,err := reader.ReadString('\n')
//Ioutil读文件（整个文件）
ret,err := ioutil.ReadFile("./main.go")
```
写文件：
```go
//打开文件
fileObj,err := os.OpenFile("./log.txt",os.O_APPEND|os.O_CREATE,0644)
//关闭文件
defer fileObj.Close()
//普通写入
fileObj.Write([]byte("xxx"))
fileObj.WriteString("xxx")
//bufio写文件
writer := bufio.NewWriter(fileObj)
writer.WriteString("xxx")//写入缓存
writer.Flush()//写入文件
//ioutil写文件
err := ioutil.WriteFile("./log.txt",[]byte(str),0666)
```
## Time
```go
now := time.Now()//时间对象
now.Year()
now.Unix()//时间戳格式
nowTime := time.Unix(now,0)//将时间戳转化为时间对象
now.Add(24 * time.Hour)//加时间
timer := time.Tick(time.Second)//定时器，一直在变，一秒一算
now.Format("2006-01-02")//时间对象格式化输出
now.Format("2006/01/02 15:04:05")
timeObj := time.Parse("2006-01-02","2004-01-01")//将字符串解析为时间对象
time.Duration(100)//将100转化为100ns的时间间隔类型
/*
Sub 时间相减
Before 判断时间前后
Equal 判断时间是否相等
...
*/
```
## Strconv
```go
//将字符串解析为10进制，64位数
strconv.ParseInt(str,10,64)
strconv.Atoi(str)
//将数字转换为字符串
strconv.Itoa(i)
//将字符串转化为bool
strconv.ParseBool("true")
...
```
## Context
Context 包提供上下文机制在 `goroutine` 之间传递 deadline、取消信号（cancellation signals）或者其他请求相关的信息。
```go
type Context interface {
    //返回值为管道，正常情况下阻塞，直到cancelfunc，chan关闭
    Done() <-chan struct{}
    //查看deadline,通过withdeadline设置，若没设置则返回ok=false
    Deadline() (deadline time.Time, ok bool)
    //chan关闭时会返回error，说明cancel原因
    Err() error
    //返回由WithValue关联到context的值。
    Value(key interface{}) interface{}
}
```
### 创建根context
根 context 不会被 cancel。这两个方法只能用在最外层代码中，比如 main 函数里。
```go
//一般使用 Background() 方法创建根 context。
context.Background()
//TODO() 用于当前不确定使用何种 context，留待以后调整。
context.TODO()
```
### 派生context
```go
func WithCancel(parent Context) (ctx Context, cancel CancelFunc)
func WithDeadline(parent Context, d time.Time) (Context, CancelFunc)
func WithTimeout(parent Context, timeout time.Duration) (Context, CancelFunc)
func WithValue(parent Context, key, val interface{}) Context
```
### 示例
```go
package main
import (
    "context""fmt""time"
)
func sleepRandom_1(stopChan chan struct{}) {
    i := 0
    for {
        time.Sleep(1 * time.Second)
        fmt.Printf("This is sleep Random 1: %d\n", i)
        i++
        if i == 5 {
            fmt.Println("cancel sleep random 1")
            stopChan <- struct{}{}
            break
        }
    }
}
func sleepRandom_2(ctx context.Context) {
    i := 0
    for {
        time.Sleep(1 * time.Second)
        fmt.Printf("This is sleep Random 2: %d\n", i)
        i++
        select {
        case <-ctx.Done():
            fmt.Printf("Why? %s\n", ctx.Err())
            fmt.Println("cancel sleep random 2")
            return
        default:
        }
    }
}
func main() {
    ctxParent, cancelParent := context.WithCancel(context.Background())
    ctxChild, _ := context.WithCancel(ctxParent)
    stopChan := make(chan struct{})
    go sleepRandom_1(stopChan)
    go sleepRandom_2(ctxChild)
    select {
    case <- stopChan:
        fmt.Println("stopChan received")
    }
    cancelParent()
    for {
        time.Sleep(1 * time.Second)
        fmt.Println("Continue...")
    }
}
```
## Flag
定义flag​命令行参数，用来接收命令行输入的参数值，一般有以下两种方法
- flag.TypeVar()：先定义参数（实际上是指针），再定义flag.TypeVar​将命令行参数存储(绑定)到前面参数的值的指针(地址)
```go
var name string
var age int
var height float64
var graduated bool
// &name 就是接收用户命令行中输入的-n后面的参数值
// 返回值是一个用来存储name参数的值的指针/地址
// 定义string类型命令行参数name，括号中依次是变量名、flag参数名、默认值、参数说明
flag.StringVar(&name, "n", "", "name参数,默认为空")
// 定义整型命令行参数age
flag.IntVar(&age,"a", 0, "age参数,默认为0")
// 定义浮点型命令行参数height
flag.Float64Var(&height,"h", 0, "height参数,默认为0")
// 定义布尔型命令行参数graduated
flag.BoolVar(&graduated,"g", false, "graduated参数,默认为false")
```
- flag.Type()：用短变量声明的方式定义参数类型及变量名
```go
// 定义string类型命令行参数name，括号中依次是flag参数名、默认值、参数说明
namePtr := flag.String("n", "", "name参数,默认为空")
// 定义整型命令行参数age
age := flag.Int("a", 0, "age参数,默认为0")
// 定义浮点型命令行参数height
height := flag.Float64("h", 0, "height参数,默认为0")
// 定义布尔型命令行参数graduated
graduated:= flag.Bool("g", false, "graduated参数,默认为false")
```
​flag​包支持的命令行参数的类型有`bool​、int​、int64​、uint​、uint64​、floatfloat64​、string​、duration​`
解析参数方式：

| -flag xxx  | 空格和一个-​符号 |
| ---------- | --------- |
| --flag xxx | 空格和两个-​符号 |
| -flag=xxx  | 等号和一个-​符号 |
| --flag=xxx | 等号和两个-​符号 |

​flag​的详细用法可参考[flag包文档](https://pkg.go.dev/flag)
## Log
```go
func (l *Logger) Print(v ...interface{}) //直接打印输出
func (l *Logger) Fatal(v ...interface{}) //输出日志后立即结束程序
func (l *Logger) Panic(v ...interface{}) //输出日志后抛出异常
```