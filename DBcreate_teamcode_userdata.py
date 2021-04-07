import requests
import simplejson as json
import pymongo

try:
    conn = pymongo.MongoClient("192.168.3.237", 27017)
    db = conn.tcs
    col = db.id_pw
    pw_data = col.find({})
    id_pw = {'os_username': pw_data[0]['id'], 'os_password': pw_data[0]['pw']}
    
    #Team code
    team_code = [
            {'team':'SOC Advanced Team', 'team_code':'4', 'project_key':'TMSAT', 'group_code':'DEPT173'},
            {'team':'SOC IP Design Team', 'team_code':'95', 'project_key':'TMIDT', 'group_code':'DEPT188'},
            {'team':'SOC Design Team', 'team_code':'5', 'project_key':'TMSDT', 'group_code':'TCW01600'},
            {'team':'SOC Verification Team', 'team_code':'6', 'project_key':'TMSVT', 'group_code':'DEPT81'},
            {'team':'SOC Implementation Team', 'team_code':'8', 'project_key':'TMSIT', 'group_code':'TCW01420'},
            {'team':'HW Platform Team', 'team_code':'87', 'project_key':'TMHWT', 'group_code':'TCW03300'},
            {'team':'HW Verification Team', 'team_code':'88', 'project_key':'TMHVT', 'group_code':'DEPT180'},
            {'team':'System BSP Team', 'team_code':'10', 'project_key':'TMBSP', 'group_code':'TCW02900'},
            {'team':'Application BSP Team', 'team_code':'11', 'project_key':'TMABT', 'group_code':'TCW02203'},
            {'team':'Security Solution Team', 'team_code':'9', 'project_key':'TMSEC', 'group_code':'TCW02700'},
            {'team':'Automotive MCU Team', 'team_code':'22', 'project_key':'TMST', 'group_code':'TCW03100'},
            {'team':'Audio Technology Team', 'team_code':'100', 'project_key':'TMAT', 'group_code':'DEPT196'},
            {'team':'Media Android Team', 'team_code':'89', 'project_key':'TMMT', 'group_code':'DEPT182'},
            {'team':'Media Linux Team', 'team_code':'90', 'project_key':'TMMLT', 'group_code':'TCW01230'},
            {'team':'Media HAL Team', 'team_code':'91', 'project_key':'TMMHT', 'group_code':'DEPT183'},
            {'team':'SW Architecture Team', 'team_code':'14', 'project_key':'TMSAT2', 'group_code':'DEPT175'},
            {'team':'Automotive Platform Team', 'team_code':'15', 'project_key':'TMAPT', 'group_code':'TCW02500'},
            {'team':'Driver Assistance Platform Team', 'team_code':'18', 'project_key':'TMAPT2', 'group_code':'TCW02400'},
            {'team':'Core Technology Team', 'team_code':'101', 'project_key':'TMCT', 'group_code':'DEPT75'},
            {'team':'Project Management Team', 'team_code':'92', 'project_key':'TMPMT', 'group_code':'DEPT184'},
            {'team':'RND Innovation Team', 'team_code':'2', 'project_key':'TMTPD', 'group_code':'TCW04300'},
            {'team':'Technical Writing Team', 'team_code':'94', 'project_key':'TMTWT', 'group_code':'DEPT186'}
            ]
    
    col = db.team_code
    col.delete_many({})
    col.insert_many(team_code)
    
    user_data = []
    for i in range(0, len(team_code)):
        resource = requests.get('https://tcs.telechips.com:8443/rest/api/2/group/member?includeInactiveUsers=false&groupname=' + team_code[i]['group_code'], id_pw)
        data = json.loads(resource.text)
        for j in range(0, len(data['values'])):
            if data['values'][j]['displayName'] == '최종상 (Jong-Sang Choi)' or data['values'][j]['displayName'] == '이완규 (Wan Gyu Lee)' or data['values'][j]['displayName'] == '성정훈 (Jaffrey Seong)' or data['values'][j]['displayName'] == '박우근 (Orion Park)' or\
            data['values'][j]['displayName'] == '김범주 (Arthur Kim)' or data['values'][j]['displayName'] == '김민우A (Thomas Kim)' or data['values'][j]['displayName'] == '장희준 (Raymond Jang)' or data['values'][j]['displayName'] == '이근 (Storm Lee)' or\
            data['values'][j]['displayName'] == '최용희 (Yong Hee Choi)' or data['values'][j]['displayName'] == '김윤형 (Yun Hyung Kim)' or data['values'][j]['displayName'] == '윤영호 (Kreis Youn)' or data['values'][j]['displayName'] == '차우종 (WJ Cha)' or\
            data['values'][j]['displayName'] == '김우식 (WS Kim)' or data['values'][j]['displayName'] == '박길성 (Roy Park)' or data['values'][j]['displayName'] == '한연호 (YH Han)' or data['values'][j]['displayName'] == '이진욱 (Jim Lee)' or\
            data['values'][j]['displayName'] == '김태현 (TH Kim)' or data['values'][j]['displayName'] == '권순홍 (SH Kwon)' or data['values'][j]['displayName'] == '이창일 (Joey Lee)' or data['values'][j]['displayName'] == '최영조 (YoungJo Choi)' or data['values'][j]['displayName'] == '김지은 (Jinny Kim)':
                user_data.append({'name':data['values'][j]['displayName'], 'employee_No':data['values'][j]['key'], 'team':team_code[i]['team'], 'email':data['values'][j]['emailAddress'], 'leader':'T-Leader'})
            else:
                user_data.append({'name':data['values'][j]['displayName'], 'employee_No':data['values'][j]['key'], 'team':team_code[i]['team'], 'email':data['values'][j]['emailAddress'], 'leader':''})
    
    user_data.append({'name':'송봉기 (BongGee Song)','employee_No':'b150137','team':'','email':'bgsong@telechips.com', 'leader':'CTO'})
    user_data.append({'name':'김문수 (Moonsoo Kim)','employee_No':'b020069','team':'SOC IP Design Team','email':'mskim@telechips.com', 'leader':'G-Leader'})
    user_data.append({'name':'최재순 (JS Choi)','employee_No':'b030187','team':'','email':'arm7@telechips.com', 'leader':'G-Leader'})
    user_data.append({'name':'노호식 (Hosi Roh)','employee_No':'b050120','team':'','email':'rohhosik@telechips.com', 'leader':'G-Leader'})
    user_data.append({'name':'이재호 (Justin Lee)','employee_No':'b030240','team':'','email':'jhlee17@telechips.com', 'leader':'G-Leader'})
    user_data.append({'name':'장지연 (Patrick Jang)','employee_No':'a990059','team':'','email':'zerocool@telechips.com', 'leader':'G-Leader'})
    user_data.append({'name':'이영종 (Daxter Lee)','employee_No':'b050109','team':'','email':'yjrobot@telechips.com', 'leader':'G-Leader'})
    
    
    #user_data의 값을 DB에 저장
    col = db.user_data
    col.delete_many({})
    col.insert_many(user_data)


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
            'text': 'teamcode_userDB_create.py 실행 실패했습니다.'
         }
    }
    r = requests.post(url, data=json.dumps(body), headers=headers) 
