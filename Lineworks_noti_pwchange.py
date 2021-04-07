import json, requests
import pymongo

try:
    #user_data를 DB에서 가져와서 리스트로 변환
    conn = pymongo.MongoClient("192.168.3.237", 27017)
    db = conn.tcs
    col = db.user_data
    user_data = col.find()
    user_data_len = col.count_documents({})
    
    col = db.bot_oauth
    headers = {
    'Content-Type': 'application/json; charset=UTF-8',
    'consumerKey': col.find({})[0]['consumerKey'],
    'Authorization': col.find({})[0]['Authorization']
    }
    
    file = open('/home/B180093/PW_EXPIRE_LOG/pw_expiration.txt', 'r')
    x = file.read()
    file.close()
    
    temp = x.split('/')
    pw_list = []
    
    for i in range(0, len(temp)):
        pw_list.append([temp[i][1:-1].split(',')[0][1:-1], temp[i][1:-1].split(',')[1][1:-1], temp[i][1:-1].split(',')[2][1:-1]])
    
    
    for i in range(0, user_data_len):
        for j in range(0, len(pw_list)):
            if pw_list[j][0].lower() == user_data[i]['employee_No']:
                pw_list[j].append(user_data[i]['name'])
    
    
    url = 'https://apis.worksmobile.com/r/kr1llsnPeSqSR/message/v1/bot/1809717/message/push' #1:1 메시지 Request URL        
    for i in range(0, len(pw_list)):
        if len(pw_list[i]) == 4:
            body = {
                'botNo': '1809717',
                #'accountId': 'bluenote212@telechips.com',
                'accountId': pw_list[i][1],
                'content': {
                    'type': 'text',
                    'text': '안녕하세요 ' + pw_list[i][3] + '님\n연구소 개발서버 접속 패스워드가 '+ pw_list[i][2] + '에 만료되오니 갱신부탁드립니다.\nSSP 접속 주소 - https://openldap.telechips.com'
                    }
                }
            r = requests.post(url, data=json.dumps(body), headers=headers)

        else:
            continue
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
            'text': 'Lineworks_noti_pwchange.py 실행 실패했습니다.'
         }
    }
    r = requests.post(url, data=json.dumps(body), headers=headers)


