import json
import websocket
from win11toast import toast

# 从文件中读取 _uid 和 __client_id
with open('cookie.txt', 'r') as file:
    _uid, __client_id = file.read().strip().split()

# 设置 WebSocket 的 headers，包含 cookie
headers = {
    "Cookie": f"_uid={_uid}; __client_id={__client_id}"
}


def on_open(ws):
    data = json.dumps({
        "channel": "chat",
        "channel_param": _uid,
        "type": "join_channel"
    })
    ws.send(data)


def on_error(ws, error):
    print(f"WebSocket error: {error}")


def on_close(ws, close_status_code, close_msg):
    print(f"WebSocket closed with status code: {close_status_code}, close message: {close_msg}")


def on_message(ws, message):
    data = json.loads(message)
    if data.get('_ws_type') == 'server_broadcast':
        msg = data['message']
        # 打印消息内容
        print(f"{msg['sender']['name']} → {msg['receiver']['name']}: {msg['content']}")
        button = {
            'activationType': 'protocol',
            'arguments': f"https://www.luogu.com.cn/chat?uid={msg['sender']['uid']}",
            'content': '查看私信'
        }
        image = {
            'src': f"https://cdn.luogu.com.cn/upload/usericon/{msg['sender']['uid']}.png",
            'placement': 'hero'
        }
        # 发送桌面通知
        toast('收到新的私信', f"{msg['sender']['name']}: {msg['content']}",
              duration='short',
              # image=image,
              button=button,
              audio={'silent': 'true'})


if __name__ == "__main__":
    ws_url = "wss://ws.luogu.com.cn/ws"
    ws = websocket.WebSocketApp(ws_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                header=headers)  # 添加 header 参数

    print("Started")
    ws.run_forever()