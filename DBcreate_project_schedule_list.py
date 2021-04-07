import json, requests
import pymongo
from datetime import datetime

try:
    day = datetime.now()
    
    conn = pymongo.MongoClient("192.168.3.237", 27017)
    
    db = conn.tcs
    
    col = db.id_pw
    pw_data = col.find({})
    id_pw = {'os_username': pw_data[0]['id'], 'os_password': pw_data[0]['pw']}
    
    col = db.project_key_category
    project_key = list(col.find(
                                    {"$or": [
                                                {'key':'CD701XR'},
                                                {'key':'SD805XQ1'},
                                                {'key':'SD805XA3'},
                                                {'key':'SD805XA2'},
                                                {'key':'SD805XL1'},
                                                {'key':'SD805XL'},
                                                {'key':'BD805XC'},
                                                {'key':'HD701XC'},
                                                {'key':'HD895XC'},
                                                {'key':'SD701XR'},
                                                {'key':'SD805XL2'},
                                                {'key':'CV8050C'},
                                                {'key':'BDCA'},
    
                                            ]
                                    },
                                    {
                                            "_id":0, "key":1, "name":1
                                    }
                                )
                        )
    
    
    version_data = []
    
    for i in range(0, len(project_key)):
        url = requests.get('https://tcs.telechips.com:8443/rest/projects/1.0/project/' + str(project_key[i]['key']) + '/release/allversions', id_pw)
        version = json.loads(url.text)
        for j in range(0, len(version)):
            temp = {
                    'date': day.strftime('%Y-%m-%d'),
                    'project_key': project_key[i]['key'],
                    'project_name': project_key[i]['name'],
                    'id': version[j]['id'],
                    'name': version[j]['name'],
                    'released': version[j]['released'],
                    'startdate': version[j]['startDate']['formatted'],
                    'enddate': version[j]['releaseDate']['formatted'],
                    'todo': version[j]['status']['toDo']['count'],
                    'inprogress': version[j]['status']['inProgress']['count'],
                    'done': version[j]['status']['complete']['count'],
                    'overdue': version[j]['overdue']
                    }
            version_data.append(temp)
    
    result_version = sorted(version_data, reverse = False, key = lambda x:(x['project_name'], x['enddate']))
    
    #----------------- 출력하지 말아야 할 마일스톤 id를 입력 ------------------#
    drop_list = [
                
            ]
    #---------------------------------------------------------------------#
    
    for i in range(0, len(drop_list)):
        for j in range(0, len(result_version)):
            if drop_list[i] == result_version[j]['id']:
                del result_version[j]
                
    
    col = db.version_list_TCS
    col.delete_many({"date": day.strftime('%Y-%m-%d')})
    col.insert_many(result_version)
    
    
    conn.close()

except:
    conn = pymongo.MongoClient("192.168.3.237", 27017)
    db = conn.tcs
    col = db.bot_oauth
    headers = {
    'Content-Type': 'application/json; charset=UTF-8',
    'consumerKey': col.find({})[0]['consumerKey'],
    'Authorization': col.find({})[0]['Authorization']
    }
    conn.close()
    
    url = 'https://apis.worksmobile.com/r/kr1llsnPeSqSR/message/v1/bot/1809717/message/push' #1:1 메시지 Request URL
    body = {
        'botNo': '1809717',
        'accountId': 'bluenote212@telechips.com',
        'content': {
            'type': 'text',
            'text': 'DBcreate_project_schedule_list.py 실행 실패했습니다.'
         }
    }
    r = requests.post(url, data=json.dumps(body), headers=headers)
    
