import json, requests
import pymongo
from atlassian import Confluence
from datetime import datetime

try:
    #id_pw를 가져와서 리스트로 변환
    conn = pymongo.MongoClient("192.168.3.237", 27017)
    db = conn.tcs
    col = db.id_pw
    pw_data = col.find({})
    id_pw = {'os_username': pw_data[0]['id'], 'os_password': pw_data[0]['pw']}
    
    
    col = db.project_key_category
    project_key = col.find({"$or": [{'projectcategory':'1.SOC 개발'},
                                   {'projectcategory':'2.SOC 검증'},
                                   {'projectcategory':'3.SDK 개발'},
                                   {'projectcategory':'4.요소/기반 기술'},
                                   {'projectcategory':'5.사업자/선행/국책'},
                                   {'projectcategory':'6.HW개발'}
                                   ]})
    project_key_len = col.count_documents({"$or": [{'projectcategory':'1.SOC 개발'},
                                                   {'projectcategory':'2.SOC 검증'},
                                                   {'projectcategory':'3.SDK 개발'},
                                                   {'projectcategory':'4.요소/기반 기술'},
                                                   {'projectcategory':'5.사업자/선행/국책'},
                                                   {'projectcategory':'6.HW개발'}
                                                   ]})
    
    conn.close()
    
    #현재 년도, 월을 출력
    day = datetime.now()
    year = day.year
    month = day.month
    
    status_release = '<ac:structured-macro ac:name="status" ac:schema-version="1" ac:macro-id="ef71acd3-1ae0-4eda-99b2-11e0aee72d0e"><ac:parameter ac:name="colour">Blue</ac:parameter><ac:parameter ac:name="title">release</ac:parameter><ac:parameter ac:name="" /></ac:structured-macro>'
    status_unrelease = '<ac:structured-macro ac:name="status" ac:schema-version="1" ac:macro-id="7570780e-a96c-465c-8f7e-acf4245eb381"><ac:parameter ac:name="colour">Yellow</ac:parameter><ac:parameter ac:name="title">unrelease</ac:parameter><ac:parameter ac:name="" /></ac:structured-macro>'
    status_archived = '<ac:structured-macro ac:name="status" ac:schema-version="1" ac:macro-id="6242d969-7110-49d8-9898-cf5e37aa02e4"><ac:parameter ac:name="colour">Grey</ac:parameter><ac:parameter ac:name="title">archived</ac:parameter><ac:parameter ac:name="" /></ac:structured-macro>'
    
    version_data = []
    for i in range(0, project_key_len):
        url = requests.get('https://tcs.telechips.com:8443/rest/projects/1.0/project/' + project_key[i]['key'] + '/release/allversions', id_pw)
        print(project_key[i]['key'])
        version = json.loads(url.text)
        if len(version) != 0:
            for j in range(0, len(version)):
                temp = []
                if version[j]['released'] == True:
                    status = status_release
                elif version[j]['archived'] == True:
                    status = status_archived
                else:
                    status = status_unrelease
                #duedate가 지난 지연중인 이슈 개수를 구하는 request
                url2 = requests.get('https://tcs.telechips.com:8443/rest/api/2/search?jql=duedate%3Cnow()%20and%20fixVersion%3D'+ version[j]['id'] +'&maxResults=1&fields=1', id_pw)
                duedate = json.loads(url2.text)
                #해당 fixversion의 worklog를 구하는 request
                url3 = requests.get('https://tcs.telechips.com:8443/rest/com.deniz.jira.worklog.email/1.0/timesheet/jql?startDate=' + str(year-1) + '-' + str(month) + '-' + str(day.day) + '&endDate=' + str(year) + '-' + str(month) + '-' + str(day.day) + '&jql=fixVersion%3D' + version[j]['id'] + '&targetKey=72', id_pw)
                resource = json.loads(url3.text)
                timespent = 0
                if 'projects' in resource.keys():
                    for k in range(0, len(resource['projects'])):
                        for l in range(0, len(resource['projects'][k]['issues'])):
                            for m in range(0, len(resource['projects'][k]['issues'][l]['workLogs'])):
                                timespent += resource['projects'][k]['issues'][l]['workLogs'][m]['timeSpent']
                    member = ''
                    for o in range(0, len(resource['worklogAuthors'])):
                        if o == len(resource['worklogAuthors'])-1:
                            member += resource['worklogAuthors'][o]['fullName'].replace('(', ' ').split()[0]
                        else:
                            member += resource['worklogAuthors'][o]['fullName'].replace('(', ' ').split()[0] + ','
                else:
                    member = '' #due date가 over된 이슈 개수를 구하는 request
                url4 = requests.get('https://tcs.telechips.com:8443/rest/api/2/search?jql=duedate<now()%20and%20status%20not%20in(Resolved%2CClosed)%20and%20fixVersion%3D'+ version[j]['id'] +'&maxResults=1&fields=1', id_pw)
                duedate_over = json.loads(url4.text)
                
                temp = {
                        'project_name' : project_key[i]['name'],
                        'project_key' : project_key[i]['key'],
                        'id' : version[j]['id'],
                        'name' : version[j]['name'],
                        'description' : version[j]['description'],
                        'start_date' : version[j]['startDate']['formatted'],
                        'release_date' : version[j]['releaseDate']['formatted'],
                        'status' : status,
                        'duedate_over_issue' : duedate['total'],
                        'resolved_issue' : version[j]['status']['complete']['count'],
                        'total_issue' : version[j]['status']['unmapped']['count'] + version[j]['status']['toDo']['count'] + version[j]['status']['inProgress']['count'] + version[j]['status']['complete']['count'],
                        'duedate_over' : duedate_over['total'],
                        'timespent' : round(timespent/60/60, 2),
                        'member' : member
                        }
                version_data.append(temp)
    
    
    #Wiki 페이지에 version Data page 생성
    wiki_data_top = '<p class="auto-cursor-target"><br /></p><ac:structured-macro ac:name="table-excerpt" ac:schema-version="1" ac:macro-id="70b8954e-f54e-46e7-8b34-a176d7c406ee">\
    <ac:parameter ac:name="name">version_data</ac:parameter><ac:rich-text-body><p class="auto-cursor-target"><br /></p><table><colgroup><col /><col /><col /><col /><col /><col /><col /><col /><col /><col />\
    <col /><col /><col /><col /><col /></colgroup><tbody><tr><th>Project_name</th><th>Key</th><th>Milestone_id</th><th>Milestone_name</th><th>Description</th><th>Milestone_start</th><th>Milestone_close</th><th>Release</th>\
    <th>Plan_issue</th><th>Resolved_issue</th><th>Total_issue</th><th>Duedate_over</th><th>timespent</th><th>Member</th></tr>'
    wiki_data_middle = ''
    wiki_data_bottom = '</tbody></table><p class="auto-cursor-target"><br /></p></ac:rich-text-body></ac:structured-macro><p><br /></p>'
    
    #version data 돌면서 table 생성
    for i in range(0, len(version_data)):
        data_row = '<tr>'
        for j in range(0, len(version_data[i])):
            if j == 3: #version name에 link
                data_row += '<td><a href="https://tcs.telechips.com:8443/projects/' + str(version_data[i]['project_key']) + '/versions/' + str(version_data[i]['id']) + '">' + str(list(version_data[i].values())[j]) + '(' + str(version_data[i]['id']) + ')' + '</a></td>'
            else: #나머지 항목은 값만 입력
                data_row += '<td>' + str(list(version_data[i].values())[j]) + '</td>'
        data_row += '</tr>'
        wiki_data_middle += data_row
    
    wiki = wiki_data_top + wiki_data_middle + wiki_data_bottom
    wiki = wiki.replace("&","<p>&amp;</p>") #특수문자 & 치환
    
    confluence = Confluence(
        url='https://wiki.telechips.com:8443',
        username = pw_data[0]['id'],
        password = pw_data[0]['pw']
        )
    
    confluence.update_page(
            parent_id = 95455710,
            page_id = 121733850,
            title = 'version_data',
            body = wiki,
            type='page',
            representation='storage'
            )


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
            'text': 'version_data_wikicreate.py 실패했습니다.'
         }
    }
    r = requests.post(url, data=json.dumps(body), headers=headers)
