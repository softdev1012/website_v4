import requests, time, os
from pymongo import MongoClient
from multiprocessing.pool import ThreadPool
from collections import Counter

mongodb = MongoClient('mongodb://localhost:27017')
db = mongodb['mfc_ctb_4']

db_global_settings = db.global_connections
db_global_settings_live = db.global_connections_live
db_running = db.running
db_ping = db.pings
db_running_ctb = db.ctb_running

'MFC PART'
def add_running_session(model_username,proxy,website_bot):
    add = False
    wp = []

    def add_model_proxx(ele):
        try:
            if website_bot == 'mfc':
                proxylove = ele.split(':')
                if len(proxylove) == 4:
                    url = requests.get('https://www.myfreecams.com/', proxies={
                        'http': 'http://{}'.format(proxylove[0]+':'+proxylove[1]+'@'+proxylove[2]+':'+proxylove[3]),
                        'https': 'https://{}'.format(proxylove[0]+':'+proxylove[1]+'@'+proxylove[2]+':'+proxylove[3])
                    }, verify=True, allow_redirects=True)

                    if url.status_code == 200:
                        wp.append(ele)
                        modelquery = [x for x in db_running.find({'model': model_username})]
                        if len(modelquery) == 0:
                            db_running.insert_one({'model': model_username,
                                                   'status': 'active',
                                                   'current_viewers': 0,
                                                   'proxy': [ele]})
                            print('Added new, model > {}'.format(model_username))
                            # return True
                        else:
                            modelinfo = modelquery[-1]
                            if ele not in modelinfo['proxy']:
                                db_running.update_one({'_id': modelinfo['_id']}, {'$push': {
                                    'proxy': ele,
                                }})
                                print('Success adding new proxie. Total proxies > {}'.format(
                                    str(len(modelinfo['proxy']) + 1)))
                                # return True
                elif len(proxylove) == 2:
                    url = requests.get('https://www.myfreecams.com/', proxies={
                        'http': 'http://{}'.format(ele),
                        'https': 'https://{}'.format(ele)
                    }, verify=False, allow_redirects=True)
                    if url.status_code == 200:
                        wp.append(ele)
                        modelquery = [x for x in db_running.find({'model': model_username})]
                        if len(modelquery) == 0:
                            db_running.insert_one({'model': model_username,
                                                   'status': 'active',
                                                   'current_viewers': 0,
                                                   'proxy': [ele]})
                            print('Added new, model > {}'.format(model_username))
                            # return True
                        else:
                            modelinfo = modelquery[-1]
                            if ele not in modelinfo['proxy']:
                                db_running.update_one({'_id': modelinfo['_id']}, {'$push': {
                                    'proxy': ele,
                                }})
                                print('Success adding new proxie. Total proxies > {}'.format(
                                    str(len(modelinfo['proxy']) + 1)))
                                # return True

            elif website_bot == 'ctb':
                proxylove = ele.split(':')
                print(len(proxylove))
                if len(proxylove) == 4:
                    url = requests.get('https://es.chaturbate.com/female-cams/', proxies={
                        'http': 'http://{}'.format(proxylove[0]+':'+proxylove[1]+'@'+proxylove[2]+':'+proxylove[3]),
                        'https': 'https://{}'.format(proxylove[0]+':'+proxylove[1]+'@'+proxylove[2]+':'+proxylove[3])
                    }, verify=False, allow_redirects=True)
                    if url.status_code == 200:
                        wp.append(ele)
                        modelquery = [x for x in db_running_ctb.find({'model': model_username})]
                        if len(modelquery) == 0:
                            db_running_ctb.insert_one({'model': model_username,
                                                   'status': 'active',
                                                   'current_viewers': 0,
                                                   'proxy': [ele]})
                            print('Added new, model > {}'.format(model_username))
                            # return True
                        else:
                            modelinfo = modelquery[-1]
                            if ele not in modelinfo['proxy']:
                                db_running_ctb.update_one({'_id': modelinfo['_id']}, {'$push': {
                                    'proxy': ele,
                                }})
                                print('Success adding new proxie. Total proxies > {}'.format(
                                    str(len(modelinfo['proxy']) + 1)))
                                # return True
                elif len(proxylove) == 2:
                    url = requests.get('https://es.chaturbate.com/female-cams/', proxies={
                        'http': 'http://{}'.format(
                            proxylove[0] + ':' + proxylove[1]),
                        'https': 'https://{}'.format(
                            proxylove[0] + ':' + proxylove[1])
                    }, verify=False, allow_redirects=True)
                    if url.status_code == 200:
                        wp.append(ele)
                        modelquery = [x for x in db_running_ctb.find({'model': model_username})]
                        if len(modelquery) == 0:
                            db_running_ctb.insert_one({'model': model_username,
                                                       'status': 'active',
                                                       'current_viewers': 0,
                                                       'proxy': [ele]})
                            print('Added new, model > {}'.format(model_username))
                            # return True
                        else:
                            modelinfo = modelquery[-1]
                            if ele not in modelinfo['proxy']:
                                db_running_ctb.update_one({'_id': modelinfo['_id']}, {'$push': {
                                    'proxy': ele,
                                }})
                                print('Success adding new proxie. Total proxies > {}'.format(
                                    str(len(modelinfo['proxy']) + 1)))
                                # return True

        except Exception as e:
            print('Proxie > {} - Not working...'.format(str(e)))
    with ThreadPool(processes=3) as pool:
        pool.map(add_model_proxx, proxy.split(','))

    if len(wp) != 0:
        return True
    else:
        print('Proxie not working')
        return False

def get_all_active(webs):
    if webs == 'mfc':
        res_query = [x for x  in db_running.find()]
        return res_query
    elif webs == 'ctb':
        res_query = [x for x  in db_running_ctb.find()]
        return res_query
def desactive_session_model(model_username):
    model_status = [x for x in db_running.find({'model':model_username})]
    session_info = model_status[-1]
    if session_info['status'] == 'active':
        db_running.update_one({'_id':session_info['_id']},{'$set':{
            'status':'stop'
        }})
        print('Model > {} - Stoped.'.format(model_username))
    else:
        print('Model > {} - Already stopped.'.format(model_username))
def add_bot(model_username,proxie_to_use,mfc_ctb):
    try:
        res = add_running_session(model_username, proxie_to_use, mfc_ctb)  # 'ctb or mfc'
        if res == False:
            return False
        elif res == True:
            return True
    except Exception as e:
        if 'ProxyError' in str(e):
            print('proxie not working.')
            return False
def remove_all_proxies_of_model(model_username,websi):
    if websi == 'mfc':
        modelquery = [x for x in db_running.find({'model': model_username})]
        modelinfo = modelquery[-1]
        db_running.update_one({'_id':modelinfo['_id']},{'$set':{
        'proxy':[]
    }})
    elif websi == 'ctb':
        modelquery = [x for x in db_running_ctb.find({'model': model_username})]
        modelinfo = modelquery[-1]
        db_running_ctb.update_one({'_id': modelinfo['_id']}, {'$set': {
            'proxy': []
        }})
def change_status_model(model_username,status,websi):
    if websi == 'mfc':
        res1 = [x for x in db_running.find({'model': model_username})]
        modelinfo = res1[-1]
        if status == 'run':
            db_running.update_one({'_id': modelinfo['_id']}, {'$set': {
                'status': 'run'
            }})
        elif status == 'stop':
            db_running.update_one({'_id': modelinfo['_id']}, {'$set': {
                'status': 'stop'
            }})
    elif websi == 'ctb':
        res1 = [x for x in db_running_ctb.find({'model': model_username})]
        modelinfo = res1[-1]
        if status == 'run':
            db_running_ctb.update_one({'_id': modelinfo['_id']}, {'$set': {
                'status': 'run'
            }})
        elif status == 'stop':
            db_running_ctb.update_one({'_id': modelinfo['_id']}, {'$set': {
                'status': 'stop'
            }})
def changegc(change):
    res = [x for x in db_global_settings.find()]
    #input(res)
    if len(res) == 0:
        db_global_settings.insert_one({'global_max_commections':1,})
        return 1
    else:
        try:
            if res[-1]['global_max_commections'] != int(change):
                print('QLQ1')
                db_global_settings.update_one({
                    '_id':res[-1]['_id']
                },{'$set':{
                    'global_max_commections':int(change)
                }}
                )
                return int(change)
            else:
                print('QLQ2')
                return int(res[-1]['global_max_commections'])
        except:
            print('QLQ3')
            return False
def check_cd():
    return int([x for x in db_global_settings.find()][-1]['global_max_commections'])

def addgs_livetime(change):
    res = [x for x in db_global_settings_live.find()]
    # input(res)
    if len(res) == 0:
        db_global_settings_live.insert_one({'max_live': 3600})
        return 3600
    else:
        try:
            if res[-1]['max_live'] != int(change):
                print('QLQ1')
                db_global_settings_live.update_one({
                    '_id': res[-1]['_id']
                }, {'$set': {
                    'max_live': int(change)
                }}
                )
                return int(change)
            else:
                return int(res[-1]['max_live'])
        except:
            print('QLQ3')
            return False
def check_lt():
    return int([x for x in db_global_settings_live.find()][-1]['max_live'])



def addpingtodb(botid,lping,modeluser):
    db_ping.insert_one({'botid': botid,
                        'last_ping': lping,
                        'model_username': modeluser})
def check_pings(direct_result=False):
    appworking_good = []
    for ele in [x for x in db_ping.find()]:
        clpt = check_lt()
        #print([ele['last_ping'],int(time.time())+30])
        if int(ele['last_ping'])+int(clpt) >int(time.time()):
            appworking_good.append(ele)
        else:
            pass
    if direct_result != False:
        for ele in appworking_good:
            if direct_result == ele['botid']:
                return True
        return False
    return appworking_good
def get_model_lives():
    cpings = check_pings()
    res3 = Counter(x['model_username'] for x in cpings)
    return res3
def delete_model(model_username, webs):
    if webs == 'mfc':
        res4 = get_all_active('mfc')
        for ele in res4:
            if ele['model'] == model_username:
                db_running.delete_one({'_id':ele['_id']})
                print('success delete')
    elif webs == 'ctb':
        res4 = get_all_active('ctb')
        for ele in res4:
            if ele['model'] == model_username:
                db_running_ctb.delete_one({'_id':ele['_id']})
                print('success delete')

'CHATURBATE_PART'