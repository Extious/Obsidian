---
title: Python基础
tags:
  - python
update: 2025-04-05
---
# 基础语法
## print
python代码一行行执行，字符串过长需要使用三引号
三引号可以直接换行
```python
print('''
ni
hao‍‍```)
```
## 命名规范
1. 字母全部小写
2. 不同单词使用下划线分割
## 数据类型
### str
### int
### float
### bool
True
False
### NoneType
None
## 交互
input函数
（等同于C语言中的scanf）
## 条件语句
```python
if 20>3:
	print(True)
else:
	print(False)
```
多层及使用elif关键字
## 列表
动态链表
## 字典
通过[]取得key对应value
### 元组
不可变列表
## for循环
可迭代对象：
* str
* 列表
* 字典
```python
# range快速迭代数字
for i in range(1,1,101):
	total = total + i
```
## 函数
```python
def func1(x):
	print(x)
	return x+1
```
## Class
```python
class CuteCat:
	def __init__(self,cat_name,cat_age):
		self.name = cat_name
		self.age = cat_age
	def speak(self):
		print("瞄" * self.age)
# 继承
class Cat(Mammal):
	# def ...
```
## 文件操作
```python
# 使用with省略close
with open("./data.txt") as f:
	# print ...
```
打开模式：
* w
* r
* a
* r+
## 异常处理
```python
try:
	# ...
except ValueError:
	# ...
except:
	# ...
else:
	# ...
finally:
	# ...
```
## 测试
# 虚拟环境配置
# Pyenv
使用pyenv可以进行多版本管理
安装（下述三条命令等效）：
```bash
# Github源
curl https://pyenv.run | bash
# 上面的调用等效于
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
# 推荐：替换国内镜像源
curl -L https://gitee.com/xinghuipeng/pyenv-installer/raw/master/bin/pyenv-installer | bash
```
配置环境变量，将安装路径写入~/.bashrc文件：
```bash
# 将以下三条语句写入 ~/.bashrc文件结尾
export PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```
在使用pyenv安装相应python库版本的时候需要安装额外的包：
```bash
sudo apt update; sudo apt install build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev gcc
```
安装python
```bash
# 查看可安装版本
pyenv install --list
#方式一：因为pyenv会自动到github上下载，速度超慢，因此推荐第二种方式
$ pyenv install 3.12.2 -v  #-v 以日志模式显示安装过程
#方式二：使用curl或者wget下载到~/.pyenv/cache下，然后再用pyenv安装。软件源可以用自己熟悉的镜像源
$ cd ~/.pyenv
$ sudo mkdir cache
$ sudo wget -c https://mirrors.huaweicloud.com/python/3.12.2/Python-3.12.2.tar.xz -P  ~/.pyenv/cache/
$ pyenv install 3.12.2 -v
```
pyenv使用：
```bash
# 当前shell
$ pyenv shell 3.12.2
# 当前目录
$ pyenv local 3.12.2
# 全局
$ pyenv global 3.12.2
# 查看当前Python版本
$ python --version
```
## 创建、激活、停用及删除 virtualenv
创建名为 `venv` 的 virtualenv 环境：
```bash
pyenv virtualenv 3.5.2 venv
```
激活 `venv` 环境：
```bash
pyenv activate venv
```
停用当前 `venv` 环境：
```bash
pyenv deactivate
```
删除 `venv` 环境：
```bash
pyenv virtualenv-delete venv
```
[官方地址](https://github.com/pyenv/pyenv)
[安装参考文章](https://blog.csdn.net/xhp312098226/article/details/137106947)
[虚拟环境参考文章](https://fugangqiang.github.io/posts/python/pyenv%E6%90%AD%E5%BB%BApython%E8%99%9A%E6%8B%9F%E7%8E%AF%E5%A2%83.html)