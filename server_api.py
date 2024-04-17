from flask import Flask, render_template, url_for, request, jsonify, redirect, send_file, send_from_directory
import threading, json, os, requests, datetime, time, shutil, pathlib
from backend import get_all_active, add_running_session, remove_all_proxies_of_model, change_status_model, changegc, check_cd, addpingtodb, check_pings, addgs_livetime ,check_lt,get_model_lives, delete_model, log_message
from bot3 import start_bot
from chaturbate_bot import start_bot_ctb
DEBUG = True
app = Flask(__name__,
            static_url_path='',
            static_folder='static/',
            template_folder='templates/')

app.config.from_object(__name__)
app.config['SECRET_KEY'] = '712JIOJCMC1008MU11X20347MC71HGKA'

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    
@app.get('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'
@app.route('/', methods=['POST', 'GET'])
def form_post():
    if request.method == 'POST':
       UserToken = request.form.to_dict()
    elif request.method == 'GET':
        return render_template('index.html')
@app.route('/getlog', methods=['GET', 'POST'])
def downloadlog():
    cur_path = pathlib.Path(__file__).parent.resolve()
    src_path = os.path.join(cur_path, 'log.txt')
    tar_path = os.path.join(cur_path, 'logs/log.txt')
    # os.rename(src_path, tar_path)
    # os.replace(src_path, tar_path)
    shutil.move(src_path, tar_path)
    return send_from_directory(directory='./logs', path='log.txt')
@app.route('/api', methods=['GET', 'POST'])
def apiserver():
    if request.method == 'GET':
        action = request.args.get('action')
        if action == 'add_new_model':
            modelusername = request.args.get('model_username')
            proxystring = request.args.get('proxies')
            webs = request.args.get('web')
            if webs == 'mfc':
                th = threading.Thread(target=add_running_session,args=(modelusername,proxystring,webs))
                th.setDaemon(True)#demonic way
                th.start()
                return {'success':'Testing all proxies...'}
            elif webs == 'ctb':
                th = threading.Thread(target=add_running_session,args=(modelusername,proxystring,webs))
                th.setDaemon(True)#demonic way
                th.start()
                return {'success':'Testing all proxies...'}
        elif action == 'get_models':
            modweh = request.args.get('web')

            if modweh == 'mfc':
                res = [[x['model'], x['status'], ','.join(x['proxy']), str(len(x['proxy']))] for x in get_all_active(modweh)]
                current_global_con = check_cd()
                currentlifetime = check_lt()

                res3 = get_model_lives()
                res5 = []

                for mod in res:
                    found = False
                    for ele3 in res3.items():
                        if mod[0] == ele3[0]:
                            mod.append(ele3[1])
                            res5.append(mod)
                            found = True
                    if found == False:
                        mod.append(0)
                        res5.append(mod)

                return {'success': res5,
                        'cgc': current_global_con,
                        'clt': currentlifetime}, 200
            elif modweh == 'ctb':

                res = [[x['model'], x['status'], ','.join(x['proxy']), str(len(x['proxy']))] for x in get_all_active(modweh)]
                try:
                    current_global_con = check_cd()
                    currentlifetime = check_lt()
                except:
                    changegc(5)
                    addgs_livetime(3600)

                res3 = get_model_lives()
                res5 = []

                for mod in res:
                    found = False
                    for ele3 in res3.items():
                        if mod[0] == ele3[0]:
                            mod.append(ele3[1])
                            res5.append(mod)
                            found = True
                    if found == False:
                        mod.append(0)
                        res5.append(mod)

                return {'success': res5,
                        'cgc': current_global_con,
                        'clt': currentlifetime}, 200
        elif action == 'clear_proxies':
            muser = request.args.get('model_username')
            webs = request.args.get('web')
            remove_all_proxies_of_model(muser, webs)
            return {'success': 'succesfully removed all proxies...'}
        elif action == 'stop_model':
            muser = request.args.get('model_username')
            webs = request.args.get('web')
            change_status_model(muser, 'stop',webs)
            return {'success':'Success stopped model...'}
        elif action == 'start_model':
            muser = request.args.get('model_username')
            webs = request.args.get('web')
            change_status_model(muser, 'run', webs)
            time.sleep(3)
            if webs == 'mfc':
                stmo = check_cd()
                th1 = threading.Thread(target=start_bot,args=(muser, int(stmo)))
                th1.setDaemon(True)  # demonic way
                th1.start()
                return {'success': 'Success started model...'}
            elif webs == 'ctb':
                th2 = threading.Thread(target=start_bot_ctb,args=(muser,))
                th2.setDaemon(True)
                th2.start()
                return {'success':'Success started model...'}
        elif action == 'ug_tcpp':
            rargs = request.args.get('val')
            changegc(rargs)
            return {'success':'changed global settings'}
        elif action == 'newbot':
            muser = request.args.get('model_username')
            muser_ping = request.args.get('ping')
            muser_botid = request.args.get('botid')
            addpingtodb(muser_botid, muser_ping, muser)
            return {'success':'success ping'}
        elif action == 'checkpings':
            return {'success':check_pings()}
        elif action == 'ug_maxlivecon':
            nval = request.args.get('val')
            res3 = addgs_livetime(int(nval))
            return {'success':res3}
        elif action == 'delete_model':
            muser = request.args.get('model_username')
            webs = request.args.get('webs')
            delete_model(muser, webs)
            return {'success':'deleted model > {}'.format(muser)}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)