import json
import websocket
from win11toast import toast
import time

with open("cookie.txt", "r") as file:
    tmp = file.read()
    list = tmp.split()
    _uid = list[0]
    __client_id = list[1]
    __user_name = list[2]

headers = {
    "Cookie": f"_uid={_uid}; __client_id={__client_id}"
}

cnt_reconnect = 0
MAX_RECONNECTS = 5


def print_msg(msg):
    print(f'{int(time.time() - st)} {msg}')


def on_open(ws):
    global cnt_reconnect
    print_msg("连接成功")
    cnt_reconnect = 0
    data = json.dumps({
        "channel": "chat",
        "channel_param": _uid,
        "type": "join_channel"
    })
    ws.send(data)


def on_close(ws, close_status_code, close_msg):
    print_msg("连接已被关闭")


def on_message(ws, message):
    data = json.loads(message)
    if data.get("_ws_type") == "server_broadcast":
        msg = data["message"]
        print_msg(f'{msg["sender"]["name"]} → {msg["receiver"]["name"]}: {msg["content"]}')
        button_open = {
            "activationType": "protocol",
            "arguments": f'https://www.luogu.com.cn/chat?uid={msg["sender"]["uid"]}',
            "content": "查看私信"
        }
        if f'{msg["sender"]["name"]}' != __user_name:
            toast("收到新的洛谷私信", f'{msg["sender"]["name"]}: {msg["content"]}',
                  duration="short",
                  # icon=f'https://cdn.luogu.com.cn/upload/usericon/{msg["sender"]["uid"]}.png',
                  buttons=[button_open, "忽略"],
                  audio={"silent": "true"})


def connect():
    global cnt_reconnect
    ws_url = "wss://ws.luogu.com.cn/ws"
    ws = websocket.WebSocketApp(ws_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_close=on_close,
                                header=headers)
    while True:
        ws.run_forever()
        try:
            ws.close()
        except:
            pass
        cnt_reconnect += 1
        # print_msg("连接已被关闭")
        print_msg(f'正在尝试重连（{cnt_reconnect}/{MAX_RECONNECTS}）')
        time.sleep(5)
        if cnt_reconnect >= MAX_RECONNECTS:
            print_msg("连接超时")
            toast("连接超时")
            break


if __name__ == "__main__":
    st = time.time()
    connect()
