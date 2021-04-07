import requests
import simplejson as json
import pymongo

try:
    conn = pymongo.MongoClient("192.168.3.237", 27017)
    db = conn.tcs
    col = db.id_pw
    pw_data = col.find({})
    id_pw = {'os_username': pw_data[0]['id'], 'os_password': pw_data[0]['pw']}
    
    #모든 프로젝트의 카테고리 data 생성
    url = requests.get('https://tcs.telechips.com:8443/rest/api/2/project', id_pw)
    data = json.loads(url.text)
    
    projectCategory_list = []
    for i in range(0, len(data)):
        key = data[i]['key']
        name = data[i]['name']
        if 'projectCategory' in data[i]:
            projectCategory = data[i]['projectCategory']['name']
        else:
            projectCategory = 'None'
        data1 = {'key': key, 'projectcategory' :projectCategory, 'name': name}
        projectCategory_list.append(data1)
    
    col = db.project_key_category
    col.delete_many({})
    col.insert_many(projectCategory_list)
    
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
    
    url = 'https://apis.worksmobile.com/r/kr1llsnPeSqSR/message/v1/bot/1809717/message/push' #1:1 메시지 Request URL
    body = {
        'botNo': '1809717',
        'accountId': 'bluenote212@telechips.com',
        'content': {
            'type': 'text',
            'text': 'project_key_category_dbcreate.py 실패 성공했습니다.'
         }
    }
    r = requests.post(url, data=json.dumps(body), headers=headers)
    
    conn.close()