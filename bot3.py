import websocket,threading,json,time,requests,random,urllib.parse,bs4,string
from backend import check_pings, check_cd, check_lt, get_active_list, log_message
s = requests.session()
s.verify = False
ids=str(int(time.time()))+str(random.randint(0,900))

def parser(step,text):
    if step == 0:

        soup = bs4.BeautifulSoup(text,'lxml')
        return soup.findAll('a')
    elif step == 1:
        'get tags'
        soup = bs4.BeautifulSoup(text,'lxml')
        alltags = soup.find('span',{'id':'tags_value'}).text
        first_tag = alltags.lstrip().rstrip().split(',')[0]
        return first_tag
    elif step == 2:
        soup = bs4.BeautifulSoup(text,'lxml')
        profile_id = soup.find('img',{'id':'profile_avatar'})['src'].split('/')[5]
        return '1'+profile_id
def get_model_idv2(username):
    url2 = s.get('https://profiles.myfreecams.com/{}'.format(username), headers={
        'Host': 'profiles.myfreecams.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://m.myfreecams.com/profiles/{}'.format(username),
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    })
    ftag = parser(2, url2.text)
    log_message(ftag)
    return ftag
def generaterandomstring(num):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=num))
def connect_room(model_username,ROOMID,proxy_to_use):

    msent = 0
    nid = 0
    userid = 0
    websocket_id_room = ''
    websocket_lentype = ''
    websocket_cxid = ''
    arg1 = ''
    arg2 = ''
    respkey = ''

    def on_message(ws, message):
        global msent, websocket_id_room, websocket_lentype, websocket_cxid, arg1, arg2, respkey
        try:
            message1 = json.loads(urllib.parse.unquote_plus(message.split(' ')[-1]))

            if '_err' in message1.keys():
                websocket_id_room = message1['ctx'][0]
                websocket_lentype = message1['ctx'][-1]
                websocket_cxid = message1['cxid']
            if 'msg' in message1.keys():
                arg1 = message1['msg']['arg1']
                if arg1 > 10000:
                    log_message('AJA HACKING')
                    arg2 = message1['msg']['arg2']
                    respkey = message1['respkey']
                    serv = message1['serv']
                    # log_message([arg1,arg2])

                    str1 = 'https://www.myfreecams.com/php/FcwExtResp.php?respkey={}&type=14&opts=256&serv={}&arg1={}&arg2={}&owner=38012424&nc={}'.format(
                        respkey, serv, str(2000), arg2, websocket_cxid)
                    str2 = 'https://www.myfreecams.com/php/FcwExtResp.php?respkey={}&type=14&opts=256&serv={}&nc=0.6544192043797341&_={}'.format(
                        respkey, serv, str(int(time.time())))

                    # input(json.loads(requests.get(str2).text))
                    all_models = json.loads(requests.get(str1).text)

                    for ele in all_models['rdata'][1:]:
                        log_message([ele[0], ele[1], ele[2]])
            if 'sid' in message1.keys():
                if message1['sid'] == websocket_id_room:
                    log_message('LOGGED IN AS > {}'.format(message1['nm']))
                    # jroom()

            log_message(message1)
            def jroom():
                if proxy_to_use == '1':
                    ws.send('51 {} 0 {} 9\n\0'.format(websocket_id_room, ROOMID))
                else:
                    allinf2 = get_active_list() #json.loads(requests.get('http://localhost/api?action=get_models&web=mfc').text)
                    for ele in allinf2:
                        if ele[0] == model_username:
                            if ele[1] == 'run':
                                ws.send('51 {} 0 {} 9\n\0'.format(websocket_id_room, ROOMID))
                            elif ele[1] == 'stop':
                                ws.close()
                                exit()
                                break
            jroom()
            #apisend()
        except:
            pass
    def on_close(ws, param1, param2):
        log_message('CLOSED')
        log_message("### closed ###")
        # ws.close()
    def on_error(ws, error):
        log_message('ERROR')
        log_message(error)
        ws.close()
    
    def on_open(ws):
        def wssend():
            while True:
                ws.send('0 0 0 0 0\n\0')
                time.sleep(30)

        def apisend():
            bid = 'botctb_{}'.format(str(generaterandomstring(8)))

            url = requests.get(
                'http://localhost/api?action=newbot&model_username={}&ping={}&botid={}'.format(model_username, str(
                    int(time.time())), bid))
            while True:
                'check by server'
                allinfo = get_active_list() # json.loads(requests.get('http://localhost/api?action=get_models&web=mfc').text)
                for ele in allinfo:
                    if ele[0] == model_username:
                        if ele[1] == 'stop':
                            ws.close()
                            exit()

                'check by server max live time'
                res2 = check_pings(direct_result=bid)
                if res2 == False:
                    ws.close()
                    exit()
                log_message(time.strftime("%H:%M:%S"), ' => ', bid)
                time.sleep(5)

        ws.send('fcsws_20180422\n\0')
        ws.send('1 0 0 20071025 0 1/guest:guest\n\0')

        log_message('fcsws_20180422\n\0')
        log_message('1 0 0 20071025 0 1/guest:guest\n\0')

        time.sleep(3)

        threading.Thread(target=wssend).start()
        threading.Thread(target=apisend).start()

    websocket.enableTrace(False)
    chat_servers = [74, 75, 67, 14, 16, 17, 18, 19, 42, 5, 7, 8, 10, 11, 12, 13, 15, 21, 22, 23, 24, 25, 26, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 39, 41, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 68, 69, 70, 71, 72, 73]
    ws = websocket.WebSocketApp('wss://wchat{}.myfreecams.com/fcsl'.format(str(random.choice(chat_servers))),
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    log_message('STARTED AS Room Number ==> {}  with proxy ==> {}'.format(ROOMID, proxy_to_use))
    if proxy_to_use == '1':
        while True:
            log_message('Set start from here.')
            ws.run_forever()
            time.sleep(60)
            ws.close()
    else:
        total_info = proxy_to_use.split(':')
        if len(total_info) == 4:
            while True:
                log_message('Set start from here.')
                ws.run_forever(http_proxy_host = total_info[2], http_proxy_port = int(total_info[3]), http_proxy_auth = (total_info[0],total_info[1]), proxy_type = "http")
                time.sleep(60)
                ws.close()
        elif len(total_info) == 2:
            while True:
                log_message('Set start from here.')
                ws.run_forever(http_proxy_host = total_info[0], http_proxy_port = int(total_info[1]), proxy_type = "http")
                time.sleep(60)
                ws.close()

def start_bot(model_username, MAX_PER_CONNECTION,direct=False):
    if direct == True:
        ROOMID = get_model_idv2(model_username)
        roomtotal = check_cd()    #json.loads(requests.get('http://localhost/api?action=get_models&web=mfc'))['cgc']
        for i in range(int(roomtotal)):
            threading.Thread(target=connect_room, args=(model_username, ROOMID, '1')).start()
            log_message('STARTED > {}'.format(str(i)))
            time.sleep(1)
    else:
        for ele in get_active_list(): #json.loads(requests.get('http://localhost/api?action=get_models&web=mfc').text)['success']:
            if ele[0] == model_username:
                if ele[1] == 'run':
                    ROOMID = get_model_idv2(model_username)
                    for proxy in ele[2].split(','):
                        for i in range(int(MAX_PER_CONNECTION)):
                            threading.Thread(target=connect_room, args=(ele[0], ROOMID, proxy)).start()
                            log_message('STARTED > {}'.format(str(i)))
                            #time.sleep(1)