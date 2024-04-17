import requests, json, time, bs4, re,random,string,websocket, threading
from backend import check_pings, log_message
s = requests.session()
s.verify = False

def generaterandomstring(num):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=num))
def parser(step,text):
    if step == 0:
        allres = re.findall(re.compile('initialRoomDossier = "(.*?)"'),text[0])
        parsed_res = json.loads(json.loads(json.dumps(allres[0].replace('\\u0022','"').replace('\\u005C', '\\'))))
        #input(parsed_res['wschat_host'])
        urlwss = parsed_res['wschat_host'] + '/{}/{}'.format(parsed_res['server_name'], generaterandomstring(8))
        #input(parsed_res)
        connect_ws = json.dumps({"method": "connect", "data":
            {"user": parsed_res['chat_username'],
             "password": parsed_res['edge_auth'],
             "room": text[1],
             "room_password": parsed_res['room_pass']
             }})
        joinroom_ws = json.dumps({'method': 'joinRoom',
                                  "data": {'room': text[1]}})

        #input(connect_ws)
        return allres[0],[connect_ws,joinroom_ws,urlwss]
    elif step == 1:
        password = re.findall(re.compile('"chat_password": "{(.*?)}"'),text[0])[0].replace('\\u005C','\\'+'\'')
        room_pass = re.findall(re.compile('"room_pass": "(.*?)"'),text[0])
        return password,room_pass
def connect_room_cb(username_room,proxy):
    bid = 'botctb_{}'.format(str(generaterandomstring(8)))
    url = s.get('https://es.chaturbate.com/{}/'.format(username_room), headers={
        'Host': 'es.chaturbate.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://es.chaturbate.com/female-cams/',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1'
    })
    res2 = parser(0, [url.text,username_room])
    def on_message(ws, message):
        log_message('MESSAGE')
        log_message(message)
        ces = getcurrent_status()
        if ces == False:
           log_message('Finishing....')
           ws.close()
    def on_error(ws, error):
        log_message('ERROR')
        log_message(error)
        ws.close()
    def on_close(ws):
        log_message('CLOSED')
        log_message("### closed ###")
        # ws.close()
    def on_open(ws):
        def apisend():
            url = requests.get(
                'http://localhost/api?action=newbot&model_username={}&ping={}&botid={}'.format(username_room, str(
                    int(time.time())), bid))
            while True:
                'check by server'
                allinfo = json.loads(requests.get('http://localhost/api?action=get_models&web=ctb').text)
                for ele in allinfo['success']:
                    if ele[0] == username_room:
                        if ele[1] == 'stop':
                            ws.close()
                            exit()

                'check by server max live time'
                res2 = check_pings(direct_result=bid)
                if res2 == False:
                    ws.close()
                    exit()
                time.sleep(5)

        def joinroom():
            login = json.dumps([json.loads(json.dumps(res2[1][0]))])
            joinroom = json.dumps([json.loads(json.dumps(res2[1][1]))])
            ws.send(login)
            time.sleep(2)
            ws.send(joinroom)
            apisend()
            # time.sleep(15)
            # ws.close()
            # log_message("thread terminating...")



        def keep_connected():
            updateroom_count = json.dumps({'method': 'updateRoomCount',
                                           'data': {
                                               'model_name': 'naughtyelle',
                                               'private_room': False
                                           }})
            updatecount = json.dumps(updateroom_count)
            # input(updatecount)
            ws.send(updatecount)

        threading.Thread(target=joinroom).start()
        # joinroom()
        # time.sleep(2)
        # while True:
        #    keep_connected()
        #    time.sleep(2)
        #    threading.Thread(target=keep_connected).start()
        # time.sleep(2)

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(res2[1][2].replace('https', 'wss') + '/websocket',
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open

    if proxy == '1':
        ws.run_forever()
    else:
        total_info = proxy.split(':')
        if len(total_info) == 4:
            ws.run_forever(http_proxy_host=total_info[2],http_proxy_port=int(total_info[3]),http_proxy_auth=(total_info[0],total_info[1]))
        elif len(total_info) == 2:
            ws.run_forever(http_proxy_host=total_info[0], http_proxy_port=int(total_info[1]))


    #:80::
def start_bot_ctb(username_model):
    allinfo = json.loads(requests.get('http://localhost/api?action=get_models&web=ctb').text)
    max_connections = allinfo['cgc']
    for ele in allinfo['success']:
        #input([ele[0],username_model])
        if ele[0] == username_model:
            for proxy in ele[2].split(','):
                for i in range(int(max_connections)):
                    nth = threading.Thread(target=connect_room_cb,args=([username_model,proxy]))
                    nth.start()