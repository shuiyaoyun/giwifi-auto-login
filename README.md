# GiWiFi Auto Login

校园网 GiWiFi 自动登录 + 断线重连脚本。**后台静默运行，断网自动连。**

## 使用教程

### 1. 下载
下载 ZIP 文件 → 解压到一个文件夹

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
右键 `install.bat` → **以管理员身份运行**，自动注册开机自启。

## macOS / Linux 使用教程

脚本核心 `auto_login.py` 跨平台，但 `.vbs` 和 `.bat` 只有 Windows 能用。

### 1. 下载并解压
```bash
git clone https://github.com/shuiyaoyun/giwifi-auto-login.git
cd giwifi-auto-login
```
或从 Releases 下载 ZIP 解压。

### 2. 安装依赖
```bash
pip3 install pycryptodome
```

### 3. 配置
```bash
cp config.ini.example config.ini
# 编辑 config.ini 填入学号和密码
nano config.ini    # 或用 vim / 记事本 / 任何编辑器
```

### 4. 运行
```bash
python3 auto_login.py
```
按 `Ctrl+C` 停止

### 5. 开机自启（macOS/Linux）
**macOS：**  
系统偏好设置 → 用户与群组 → 登录项 → 添加 `auto_login.py`（需先赋予可执行权限 `chmod +x auto_login.py`）

**Linux：**  
添加一行到 crontab：
```bash
crontab -e
# 添加：
@reboot python3 /你的路径/auto_login.py &
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `auto_login.py` | 核心脚本（不要动它） |
| `auto_login_launcher.vbs` | 双击启动（无窗口后台运行，**仅 Windows**） |
| `install.bat` | 右键→管理员运行，自动注册开机自启（**仅 Windows**） |
| `config.ini.example` | 配置模板，改成 `config.ini` 并填账号密码 |
| `config.ini` | 你的账号密码（已加入 .gitignore，不会上传到 GitHub） |

## 依赖

- Python 3
- `pip install pycryptodome`
