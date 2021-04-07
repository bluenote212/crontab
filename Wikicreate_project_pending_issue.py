import requests
import simplejson as json
from datetime import datetime, timedelta
from atlassian import Confluence
import pymongo

try:
    #mongoDB TCS Collection 과 연결하여 id, pw를 가져옴
    conn = pymongo.MongoClient("192.168.3.237", 27017)
    db = conn.tcs
    col = db.id_pw
    pw_data = col.find({})
    id_pw = {'os_username': pw_data[0]['id'], 'os_password': pw_data[0]['pw']}
    
    #연구소 과제 프로젝트의 키를 구하기 위한 find
    col = db.project_key_category
    project_key = list(col.find(
            {"$or":
                [
                        {'projectcategory':'1.SOC 개발'},
                        {'projectcategory':'2.SOC 검증'},
                        {'projectcategory':'3.SDK 개발'},
                        {'projectcategory':'4.요소/기반 기술'},
                        {'projectcategory':'5.사업자/선행/국책'},
                        {'projectcategory':'6.HW개발'}
                ]
            }
    ))
    
    #현재 년도, 월을 출력
    day = datetime.now()
    project_issue_data = []
    
    #프로젝트 별로 반복하며 이슈개수를 저장하는 부분
    for i in range(0, len(project_key)):
        print(project_key[i]['key'])
        total_issue_url = requests.get('https://tcs.telechips.com:8443/rest/api/2/search?jql=project%20%3D%20' + project_key[i]['key'] + '&maxResults=1&fields=j', id_pw)
        total_issue_text = json.loads(total_issue_url.text)
        if 'total' in total_issue_text.keys():
            total_issue = total_issue_text['total']
        else:
            total_issue = 'Error'
        
        week_issue_url = requests.get('https://tcs.telechips.com:8443/rest/api/2/search?jql=issueFunction%20not%20in%20hasSubtasks()%20AND%20issueFunction%20in%20dateCompare(%22%22%2C%20%22Start%20date%20%2B14d%20%3C%20dueDate%22)%20and%20statusCategory%20in%20(%22To%20Do%22%2C%22In%20Progress%22)And%20Issuetype%20not%20in%20(%22Epic%22)%20and%20project%20%3D%20' + project_key[i]['key'] + '&maxResults=1&fields=j', id_pw)
        week_issue_text = json.loads(week_issue_url.text)
        if 'total' in week_issue_text.keys():
            week_issue = week_issue_text['total']
        else:
            week_issue = 'Error'
        
        pending_issue_url = requests.get('https://tcs.telechips.com:8443/rest/api/2/search?jql=status%20%3D%20Pending%20and%20project%20%3D%20' + project_key[i]['key'] + '&maxResults=1&fields=j', id_pw)
        pending_issue_text = json.loads(pending_issue_url.text)
        if 'total' in pending_issue_text.keys():
            pending_issue = pending_issue_text['total']
        else:
            pending_issue = 'Error'
        
        project_issue_data.append({'key':project_key[i]['key'], 'date':str(day.strftime('%Y-%m-%d')), 'total':total_issue, '2weeks':week_issue, 'pending':pending_issue})
    
    #프로젝트 이슈 개수를 저장한 리스트(project_issue_data)를 project_pending_2weeks 콜렉션에 insert
    col = db.project_pending_2weeks
    col.insert_many(project_issue_data)
    
    #project_pending_2weeks 콜렉션에서 최근 4주 전 Data만 find
    col = db.project_pending_2weeks
    day = datetime.now()
    day_before = day - timedelta(weeks = 4)
    project_issue_data_8weeks = list(col.find({'date':{'$gte':str(day_before)}}))
    
    
    #8주 data를 Wiki 페이지에 table로 생성
    wiki_data_top = '<p class="auto-cursor-target"><br /></p><ac:structured-macro ac:name="table-excerpt" ac:schema-version="1" ac:macro-id="161913ea-7275-49ec-89af-a4e8e775825c"><ac:parameter ac:name="name">WBS</ac:parameter><ac:rich-text-body><p><br /></p><table class="wrapped"><colgroup><col /><col /><col /><col /><col /></colgroup><tbody><tr><th>Key</th><th><div class="content-wrapper"><p class="auto-cursor-target">date</p></div></th><th>total</th><th>2weeks</th><th>pending</th></tr>'
    wiki_data_middle = ''
    wiki_data_bottom = '</tbody></table><p class="auto-cursor-target"><br /></p></ac:rich-text-body></ac:structured-macro><p class="auto-cursor-target"><br /></p>'
    
    for i in range(0, len(project_issue_data_8weeks)):
        row = '<tr><td class="confluenceTd">' + str(project_issue_data_8weeks[i]['key']) + '</td><td class="confluenceTd">' + str(project_issue_data_8weeks[i]['date']) + '</td><td class="confluenceTd">' + str(project_issue_data_8weeks[i]['total']) + '</td><td class="confluenceTd">' + str(project_issue_data_8weeks[i]['2weeks']) + '</td><td class="confluenceTd">' + str(project_issue_data_8weeks[i]['pending']) + '</td></tr>'
        wiki_data_middle += row
    
    wiki = wiki_data_top + wiki_data_middle + wiki_data_bottom
    wiki = wiki.replace("&","<p>&amp;</p>") #특수문자 & 치환
    
    #confluence id, pw로 연결
    confluence = Confluence(
        url='https://wiki.telechips.com:8443',
        username = pw_data[0]['id'],
        password = pw_data[0]['pw']
        )
    
    #wiki page에 내용 업데이트
    confluence.update_page(
            parent_id = 95455710,
            page_id = 175327739,
            title = 'Project issue status',
            body = wiki,
            type='page',
            representation='storage'
        )
    conn.close()

except:
    #실패시 신호찬, 김나래에게 bot 메시지 보냄
    conn = pymongo.MongoClient("192.168.3.237", 27017)
    db = conn.tcs
    col = db.bot_oauth
    headers = {
    'Content-Type': 'application/json; charset=UTF-8',
    'consumerKey': col.find({})[0]['consumerKey'],
    'Authorization': col.find({})[0]['Authorization']
    }
    conn.close()
    
    #신호찬에게 메시지 전송
    url = 'https://apis.worksmobile.com/r/kr1llsnPeSqSR/message/v1/bot/1809717/message/push'
    body = {
        'botNo': '1809717',
        'accountId': 'bluenote212@telechips.com',
        'content': {
            'type': 'text',
            'text': 'Project Pending, 2weeks backdata wiki page 생성 실패했습니다.(Wikicreate_project_pending_issue.py)'
         }
    }
    r = requests.post(url, data=json.dumps(body), headers=headers)
    
    #김나에게 메시지 전송
    body = {
        'botNo': '1809717',
        'accountId': 'lena.kim@telechips.com',
        'content': {
            'type': 'text',
            'text': 'Project Pending, 2weeks backdata wiki page 생성 실패했습니다.(Wikicreate_project_pending_issue.py)'
         }
    }
    r = requests.post(url, data=json.dumps(body), headers=headers)

    