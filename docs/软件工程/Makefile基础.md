---
title: Makefile基础
tags:
  - makefile
update: 2025-04-06
---
## 前言
从代码到可执行文件需要预处理，编译，汇编和链接这几个步骤。
而一个项目有多个源文件，如果只修改一个，就对所有源文件重新执行编译、链接步骤，就太浪费时间了，因此十分有必要引入 Makefile 工具：Makefile 工具可以根据文件依赖，自动找出那些需要重新编译和链接的源文件，并对它们执行相应的动作。
## makefile三要素
目标，依赖，执行语句：
![image](https://picture.zhaozhan.site/makefile-steps.png)
## 基本语句
### 基本结构
```Makefile
# Makefile
main : main.c
        gcc main.c -o main
```
### 通配符和使用wildcard函数
Wildcard function使用方法
```Makefile
$(wildcard pattern…)
```
**使用举例：**
```Makefile
# Makefile
main : $(wildcard *.c)
        gcc $(wildcard *.c) -o main
```
## 变量
### 变量使用通配符
```Makefile
# Makefile
SRCS := $(wildcard *.c)
main : $(SRCS)
        gcc $(SRCS) -o main
```
### 赋值和修改
#### 递归赋值
```Makefile
foo = $(bar)
bar = $(ugh)
ugh = Huh?
all:;echo $(foo)
# 打印的结果为 Huh?，$(foo)展开得到$(bar)，$(bar)展开得到$(ugh)，$(ugh)展开得到Huh?最终$(foo)展开得到Huh?
```
#### 简单赋值
```Makefile
x := foo
y := $(x) bar
x := later
# 等效于：
# y := foo bar
# x := later
```
#### 文本添加
```Makefile
objects = main.o foo.o bar.o utils.o
objects += another.o
# objects最终为main.o foo.o bar.o utils.o another.o
```
#### 条件赋值
```Makefile
FOO ?= bar
# FOO最终为bar
foo := ugh
foo ?= Huh?
# foo最终为ugh
```
## Makefile进阶
### 应对复杂的目录结构
当前的目录结构为：
```Makefile
.
├── Makefile
├── entry.c
├── func
│   ├── bar.c
│   └── bar.h
└── main
```
使用foreach函数遍历所有的头文件和源文件
使用方法：
```Makefile
$(foreach var,list,text)
```
使用举例：
```Makefile
# Makefile
#the list
SUBDIR := .
SUBDIR += ./func
#find .h file
INCS := $(foreach dir,$(SUBDIR),-I$(dir))
#find .c file
SRCS := $(foreach dir,$(SUBDIR),$(wildcard $(dir)/*.c))
#go
main : $(SRCS)
        gcc $(INCS) $(SRCS) -o main
```
### 分析编译过程
* 预处理：预处理器将以字符 `#` 开头的命令展开、插入到原始的C程序中。比如我们在源文件中能经常看到的、用于头文件包含的 `#include` 命令，它的功能就是告诉预编译器，将指定头文件的内容插入的程序文本中，生成 `.i`文本文件。下图示解析：
![image](https://picture.zhaozhan.site/makefile-compile.png)
* 编译阶段：编译器将文本文件 `*.i` 翻译成文本文件 `*.s`，它包含一个汇编语言程序。
* 汇编阶段：汇编器将 `*.s` 翻译成机器语言指令，把这些指令打包成可重定位目标程序（relocatable object program）的格式，并保存在 `*.o` 文件中。
* 链接阶段：在 `bar.c` 中我们定义了 `Print_Progress_Bar` 函数，该函数会保存在目标文件 `bar.o` 中。直到链接阶段，链接器才以某种方式将 `Print_Progress_Bar` 函数合并到 `main` 函数中去。在链接时如果没有指定 `bar.o`，链接器就无法找到 `Print_Progress_Bar` 函数，也就会提示找不到相关函数的定义。
### 模式规则和自动变量（两个问题）
目前要解决两个问题
1. 没有保存 `.o` 文件，这导致我们每次文件变动都要重新执行预处理、编译和汇编来得到目标文件，即使新得到的文件与旧文件完全没有差别（即编译用到的源文件没有任何变化，就跟 `bar.c` 一样）。
2. 有保存 `.o` 文件，则会遇到第二个问题，即依赖中没有指定头文件，这意味着只修改头文件的情况下，源文件不会重新编译得到新的可执行文件！
#### 编译过程:
![image](https://picture.zhaozhan.site/makefile-process.png)
##### (.o文件的保存)解决第一个问题：
简单点可以：
```Makefile
SUBDIR := .
SUBDIR += ./func
INCS := $(foreach dir,$(SUBDIR),-I$(dir))
SRCS := $(foreach dir,$(SUBDIR),$(wildcard $(dir)/*.c))
main : ./entry.o ./func/bar.o
        gcc ./entry.o ./func/bar.o -o main
./entry.o : ./entry.c
        gcc -c $(INCS) ./entry.c -o ./entry.o
./func/bar.o : ./func/bar.c
        gcc -c $(INCS) ./func/bar.c -o ./func/bar.o
```
通过手动添加目标和依赖，我们实现了 `*.o` 文件的保存，同时还确保了源文件在更新后，只会在最小限度内重新编译 `*.o` 文件。现在我们可以利用符号 `%` 和自动变量，来让 `Makefile` 变得更加通用。首先聚焦于编译过程：
```Makefile
./entry.o : ./entry.c
        gcc -c $(INCS) ./entry.c -o ./entry.o
./func/bar.o : ./func/bar.c
        gcc -c $(INCS) ./func/bar.c -o ./func/bar.o
```
上下比较 `./entry.o` 和 `./func/bar.o` 的目标依赖及执行，可以发现新添加的、用于生成 `*.o` 文件的目标和依赖，有着相同的书写模式，这意味着存在通用的写法：
```Makefile
%.o : %.c
        gcc -c $(INCS) $< -o $@
```
![image](https://picture.zhaozhan.site/makefile-grammar.png)
这里我们用上了 `%` ，它的作用有些难以用语言概括，上述例子中， `%.o` 的作用是匹配所有以 `.o` 结尾的目标；而后面的 `%.c` 中 `%` 的作用，则是将 `%.o` 中 `%` 的内容原封不动的挪过来用。
更具体地例子是，`%.o` 可能匹配到目标 `./entry.o` 或 `./func/bar.o`，这样 `%` 的内容就会是 `./entry` 或 `./func/bar`，最后交给 `%.c` 时就变成了 `./entry.c` 或 `./func/bar.c`。
另外我们还使用到了自动变量 `$< $@`，其中 `$<` 指代依赖列表中的第一个依赖；而 `$@` 指代目标。注意自动变量与普通变量不同，它不使用小括号。
结合起来使用，我们就得到了通用的生成 `*.o` 文件的写法：
```Makefile
# Makefile
SUBDIR := .
SUBDIR += ./func
INCS := $(foreach dir,$(SUBDIR),-I$(dir))
SRCS := $(foreach dir,$(SUBDIR),$(wildcard $(dir)/*.c))
main : ./entry.o ./func/bar.o
        gcc ./entry.o ./func/bar.o -o main
%.o : %.c
        gcc -c $(INCS) $< -o $@
```
#### 链接过程：
```Makefile
main : ./entry.o ./func/bar.o
        gcc ./entry.o ./func/bar.o -o main
```
我们不能通过wildcard函数来实现通用的写法，因为在最开始我们是无法匹配到 `*.o` 文件的，因为起初我们只有 `*.c` 文件， `*.o` 文件是后来生成的。
##### patsubst函数
转换一下思路，我们在获取所有源文件后，直接将 `.c` 后缀替换为 `.o`，而patsubst 函数可以用于模式文本替换。
```Makefile
$(patsubst pattern,replacement,text)
```
patsubst 函数的作用是匹配 `text` 文本中与 `pattern` 模式相同的部分，并将匹配内容替换为 `replacement`。于是链接步骤可以改写为：
```Makefile
SRCS := $(foreach dir,$(SUBDIR),$(wildcard $(dir)/*.c))
OBJS := $(patsubst %.c,%.o,$(SRCS))
main : $(OBJS)
        gcc $(OBJS) -o main
```
最终的Makefile内容为：
```Makefile
SUBDIR := .
SUBDIR += ./func
INCS := $(foreach dir,$(SUBDIR),-I$(dir))
SRCS := $(foreach dir,$(SUBDIR),$(wildcard $(dir)/*.c))
OBJS := $(patsubst %.c,%.o,$(SRCS))
main : $(OBJS)
        gcc $(OBJS) -o main
%.o : %.c
        gcc -c $(INCS) $< -o $@
```
## 丰富完善Makefile的功能
### 指定*.o文件的输出路径
我们想要将 `*.o` 文件保存至指定目录，与源文件和头文件区分开：
```Makefile
SUBDIR := ./
SUBDIR += ./func
OUTPUT := ./output
INCS := $(foreach dir,$(SUBDIR),-I$(dir))
SRCS := $(foreach dir,$(SUBDIR),$(wildcard $(dir)/*.c))
OBJS := $(patsubst %.c,$(OUTPUT)/%.o,$(SRCS))
main : $(OBJS)
        gcc $(OBJS) -o main
$(OUTPUT)/%.o : %.c
        mkdir -p $(dir $@)
        gcc -c $(INCS) $< -o $@
```
上述Makefile中使用了dir函数
`mkdir -p $(dir $@)`中 `$@`相当于目标 `$(OUTPUT)/%.o`dir函数取得其路径，mkdir创建需要的目录。
### 伪目标
```Makefile
.PHONY : clean
OUTPUT := ./output
clean:
        rm -r $(OUTPUT)
```
使用 `.PHONY`声明一个伪目标 `clean`使用的时候输入 `make clean`就会执行 `clean：`之后的命令
### 简化终端输出
我们常通过 `@` 符号，来禁止 Makefile 将执行的命令输出至终端上：
比如：
```Makefile
$(OUTPUT)/%.o : %.c
        mkdir -p $(dir $@)
        @gcc -c $(INCS) $< -o $@
```
执行 `make`之后 `gcc -c $(INCS) $< -o $@`命令就不会在终端输出
同时我们也可以使用echo命令来拟定自己的输出信息
```Makefile
clean:
        @echo try to clean...
        @rm -r $(OUTPUT)
        @echo Complete!
```
### 自动生成依赖（解决第二个问题）
我们要将头文件一同加入到 `*.o` 文件的依赖中，从而解决修改头文件后，包含该头文件的源文件不会重新编译的问题。
仅需在编译时指定 `-MMD` 选项，就能得到记录有依赖关系的 `*.d` 文件。
`-MMD` 选项包含两个动作，一是生成依赖关系，二是保存依赖关系到 `*.d` 文件。与其类似的选项还有 `-MD`，其作用与 `-MMD` 相同，差别在于 `-MD` 选项会将系统头文件一同添加到依赖关系中。
另外我们还可以指定 `-MP` 选项，这会为每个依赖添加一个没有任何依赖的伪目标。`-MP` 选项生成的伪目标，可以有效避免删除头文件时，Makefile 因找不到目标来更新依赖所报的错误。
最终的Makefile文件
```Makefile
SUBDIR := ./
SUBDIR += ./func
OUTPUT := ./output
INCS := $(foreach dir,$(SUBDIR),-I$(dir))
SRCS := $(foreach dir,$(SUBDIR),$(wildcard $(dir)/*.c))
OBJS := $(patsubst %.c,$(OUTPUT)/%.o,$(SRCS))
DEPS := $(patsubst %.o,%.d,$(OBJS))
main : $(OBJS)
        @echo linking...
        @gcc $(OBJS) -o main
        @echo Complete!
$(OUTPUT)/%.o : %.c
        @echo compile $<...
        @mkdir -p $(dir $@)
        @gcc -MMD -MP -c $(INCS) $< -o $@
.PHONY : clean
clean:
        @echo try to clean...
        @rm -r $(OUTPUT)
        @echo Complete!
-include $(DEPS)
```
最后一行的 `include` 用于将指定文件的内容插入到当前文本中。初次编译，或者 make clean 后再次编译时，`*.d` 文件是不存在的，这通常会导致 include 操作报错。所以我们在 `include` 前加了 `-` 符号，其作用是指示 make 在 include 操作出错时忽略这个错误，不输出任何错误信息并继续执行接下来的操作。
## 通用模板
```Makefile
ROOT := $(shell pwd)
SUBDIR := $(ROOT)
SUBDIR += $(ROOT)/func
TARGET := main
OUTPUT := ./output
INCS := $(foreach dir,$(SUBDIR),-I$(dir))
SRCS := $(foreach dir,$(SUBDIR),$(wildcard $(dir)/*.c))
OBJS := $(patsubst $(ROOT)/%.c,$(OUTPUT)/%.o,$(SRCS))
DEPS := $(patsubst %.o,%.d,$(OBJS))
main : $(OBJS)
        @echo linking...
        @gcc $(OBJS) -o main
        @echo complete!
$(OUTPUT)/%.o : %.c
        @echo compile $<...
        @mkdir -p $(dir $@)
        @gcc -MMD -MP -c $(INCS) $< -o $@
.PHONY : clean
clean:
        @echo try to clean...
        @rm -r $(OUTPUT)
        @echo complete!
-include $(DEPS)
```
## 参考链接
[写给初学者的makefile入门指南](https://zhuanlan.zhihu.com/p/618350718)