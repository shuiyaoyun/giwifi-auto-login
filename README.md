# GiWiFi Auto Login

校园网 GiWiFi 自动登录与断线重连脚本。

## 功能

- 每 30 秒检测网络连通性
- 断网后自动尝试登录 GiWiFi 校园网
- 连续 3 次失败后加倍等待间隔
- 日志记录到 `~/auto_login.log`
- 后台静默运行（无窗口）

## 文件说明

| 文件 | 说明 |
|------|------|
| `auto_login.py` | 核心脚本，包含网络检测、AES 加密、自动登录 |
| `auto_login_launcher.vbs` | 静默启动器，用 pythonw.exe 无窗口运行 |

## 使用方法

1. 编辑 `auto_login.py` 顶部的 `ACCOUNT` 和 `PASSWORD`
2. 安装依赖：`pip install pycryptodome`
3. 双击 `auto_login_launcher.vbs` 运行
4. 或设置计划任务开机自启

## 依赖

- Python 3
- pycryptodome（推荐）或 cryptography（可选）
