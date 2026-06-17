# GiWiFi Auto Login

校园网 GiWiFi 自动登录 + 断线重连脚本。**后台静默运行，断网自动连。**

## 小白使用教程

### 1. 下载
**下载 ZIP** → 解压到一个文件夹

### 2. 装 Python（如果没有的话）
打开 **命令提示符（cmd）**，输入：
```
python --version
```
如果提示找不到，去 https://www.python.org/downloads/ 下载安装（**安装时勾选 Add Python to PATH**）

### 3. 安装依赖
在命令提示符输入：
```
pip install pycryptodome
```
等它装完。

### 4. 填写账号密码
1. 用 **记事本** 打开 `config.ini.example`
2. 找到 `username = YOUR_STUDENT_ID`，把 `YOUR_STUDENT_ID` 改成你的**学号（账号）**
3. 找到 `password = YOUR_PASSWORD`，把 `YOUR_PASSWORD` 改成你的**密码**
4. **另存为** 改名为 `config.ini`（去掉 .example）

### 5. 运行
**双击** `auto_login_launcher.vbs`——没有任何窗口弹出来，已经在后台跑了。

### 6. 设置开机自启（可选）
1. 搜索打开 **任务计划程序**
2. 点右侧 **创建基本任务**
3. 名称填 `GiWiFi Auto Login`，触发器选 **用户登录时**
4. 操作选 **启动程序**，程序填 `wscript.exe`，参数填 `auto_login_launcher.vbs` 的完整路径

## 文件说明

| 文件 | 说明 |
|------|------|
| `auto_login.py` | 核心脚本（不要动它） |
| `auto_login_launcher.vbs` | 双击启动（无窗口后台运行） |
| `config.ini.example` | 配置模板，改成 `config.ini` 并填账号密码 |
| `config.ini` | 你的账号密码（已加入 .gitignore，不会上传到 GitHub） |

## 依赖

- Python 3
- `pip install pycryptodome`
