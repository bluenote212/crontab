import requests
import simplejson as json
import pymongo


conn = pymongo.MongoClient("192.168.3.237", 27017)
db = conn.tcs
col = db.id_pw
pw_data = col.find({})
id_pw = {'os_username': pw_data[1]['id'], 'os_password': pw_data[1]['pw']}


#모든 프로젝트의 카테고리 data 생성
url = requests.get('https://tims.telechips.com:8443/rest/api/2/search?jql=createdDate%20>%3D%20-1d&maxResults=1000&validateQuery=false&fields=issuetype', id_pw)
data = json.loads(url.text)

