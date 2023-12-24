<h1 align="center">- LuoguMsgNotifier -</h1>

<p align="center">
<img src="https://img.shields.io/github/v/release/amakerlife/LuoguMsgNotifier.svg">
<img src="https://img.shields.io/github/license/amakerlife/LuoguMsgNotifier" alt="License" />
<img src="https://img.shields.io/github/last-commit/amakerlife/LuoguMsgNotifier">
<img src="https://img.shields.io/github/downloads/amakerlife/LuoguMsgNotifier/total?label=Release%20Downloads">
<img src="https://img.shields.io/badge/support-Windows-blue?logo=Windows 10+">
</p>

在 Windows 上通知洛谷私信。

---

## 使用方法

下载 [最新版 Release](https://github.com/amakerlife/LuoguMsgNotifier/releases/latest)，解压缩后在 exe 所在目录下创建 `cookie.txt` 文件，以 `_uid __client_id` 的形式写入 cookie。完成后运行程序即可。

## 自行打包

```bash
git clone https://github.com/amakerlife/LuoguMsgNotifier
cd LuoguMsgNotifier
pip install -r requirements.txt
pyinstaller -F -i lgfavicon.ico main.py
```
