# coding:utf-8
from flask import Flask
import requests
from bs4 import BeautifulSoup
from lxml import etree
import json
from flask import request, session, g, redirect, url_for, abort, \
    render_template, flash, current_app

app = Flask(__name__)

#db = pymysql.connect("localhost", "root", "root", "qa",charset='utf8')


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/qa/<question>")
def queryByQuestion(question):
    url = "https://iask.sina.com.cn/search"

    querystring = {"searchWord": " 如何给父母买保险", "record": "1"}

    headers = {
        'pragma': "no-cache",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/65.0.3325.146 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'cache-control': "no-cache",
        'cookie': "SINAGLOBAL=61.216.161.146_1520406637.236937; U_TRS1=00000092.401a4cf8.5a9f9925.1f3bad2e; UOR=,"
                  "blog.sina.com.cn,; ULV=1520408869623:1:1:1:61.216.161.146_1520406637.236939:; "
                  "Apache=10.71.2.95_1521018175.881433; iask_cookie=1521252428345.8599; "
                  "UM_distinctid=16231b5ea5757-062737e58c1a34-33657c04-fa000-16231b5ea5815c; "
                  "CNZZDATA5890382=cnzz_eid%3D742738111-1521251625-null%26ntime%3D1521251625; "
                  "Hm_lvt_ad29670c49e093f8aa6cbb0f672c1a81=1521252429; "
                  "CNZZDATA1254164143=660789046-1521252428-null%7C1521252428; "
                  "CNZZDATA1254639207=1559181879-1521247894-https%253A%252F%252Fiask.sina.com.cn%252F%7C1521247894; "
                  "Hm_lpvt_ad29670c49e093f8aa6cbb0f672c1a81=1521252611; "
                  "Hm_lvt_5ddee0387661b15cea4b3ca849e03784=1521252611; "
                  "Hm_lpvt_5ddee0387661b15cea4b3ca849e03784=1521252611",
        'connection': "keep-alive",
    }

    data_dict = {}
    data_list = []
    answer = {}
    querystring['searchWord'] = question
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
    except Exception as e:
        answer['code'] = 400
        answer['message'] = '请求出错，请稍后再试'
        answer['data'] = []
        return json.dumps(answer)
    try:
        soup = BeautifulSoup(response.text, "lxml")
        datas = soup.find_all('p', class_="title")
        domain_url = "https://iask.sina.com.cn/"
        for data in datas[:3]:
            detail_url = data.find('a')['href']
            response = requests.get(domain_url + detail_url, headers=headers)
            html = etree.HTML(response.text)
            result = html.xpath('//*[@id="other_answer"]/ul/li/div/div[1]/div[2]/span/pre/text()')
            if not result:
                result = html.xpath('//*[@id="other_answer"]/ul/li/div/div[1]/div/span/pre/text()')
            if len(''.join(result).strip()) < 30:
                continue
            key = (data.find('a').get_text()).strip().replace('\r', '').replace('\n', '')
            value = ''.join(result).strip().replace('\r', '').replace('\n', '')
            data_dict[key] = value
        data_list.append(data_dict)
        answer['code'] = 200
        answer['message'] = "请求成功"
        answer['data'] = data_list
        return json.dumps(answer)
    except Exception as e:
        answer['code'] = 400
        answer['message'] = '解析出错，请稍后再试'
        answer['data'] = []
        return json.dumps(answer)


@app.route("/qademo", methods=['POST', 'GET'])
def queryBydemo():
    if request.method == 'GET':
        return render_template('index-demo.html', error={})
    question = request.form['question']
    url = "https://iask.sina.com.cn/search"

    querystring = {"searchWord": " 如何给父母买保险", "record": "1"}

    headers = {
        'pragma': "no-cache",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/65.0.3325.146 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'cache-control': "no-cache",
        'cookie': "SINAGLOBAL=61.216.161.146_1520406637.236937; U_TRS1=00000092.401a4cf8.5a9f9925.1f3bad2e; UOR=,"
                  "blog.sina.com.cn,; ULV=1520408869623:1:1:1:61.216.161.146_1520406637.236939:; "
                  "Apache=10.71.2.95_1521018175.881433; iask_cookie=1521252428345.8599; "
                  "UM_distinctid=16231b5ea5757-062737e58c1a34-33657c04-fa000-16231b5ea5815c; "
                  "CNZZDATA5890382=cnzz_eid%3D742738111-1521251625-null%26ntime%3D1521251625; "
                  "Hm_lvt_ad29670c49e093f8aa6cbb0f672c1a81=1521252429; "
                  "CNZZDATA1254164143=660789046-1521252428-null%7C1521252428; "
                  "CNZZDATA1254639207=1559181879-1521247894-https%253A%252F%252Fiask.sina.com.cn%252F%7C1521247894; "
                  "Hm_lpvt_ad29670c49e093f8aa6cbb0f672c1a81=1521252611; "
                  "Hm_lvt_5ddee0387661b15cea4b3ca849e03784=1521252611; "
                  "Hm_lpvt_5ddee0387661b15cea4b3ca849e03784=1521252611",
        'connection': "keep-alive",
    }

    data_dict = {}
    data_list = []
    answer = {}
    querystring['searchWord'] = question
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
    except Exception as e:
        answer['code'] = 400
        answer['message'] = '请求出错，请稍后再试'
        answer['data'] = []
        return json.dumps(answer)
    try:
        soup = BeautifulSoup(response.text, "lxml")
        datas = soup.find_all('p', class_="title")
        domain_url = "https://iask.sina.com.cn/"
        for data in datas[:3]:
            data_dict = {}
            detail_url = data.find('a')['href']
            response = requests.get(domain_url + detail_url, headers=headers)
            html = etree.HTML(response.text)
            result = html.xpath('//*[@id="other_answer"]/ul/li/div/div[1]/div[2]/span/pre/text()')
            if not result:
                result = html.xpath('//*[@id="other_answer"]/ul/li/div/div[1]/div/span/pre/text()')
            if len(''.join(result).strip()) < 30:
                continue
            key = (data.find('a').get_text()).strip().replace('\r', '').replace('\n', '')
            value = ''.join(result).strip().replace('\r', '').replace('\n', '')
            data_dict[key] = value
            data_list.append(data_dict)
        print(data_list)
        answer['code'] = 200
        answer['message'] = "请求成功"
        answer['data'] = data_list
        return json.dumps(answer)
    except Exception as e:
        answer['code'] = 400
        answer['message'] = '解析出错，请稍后再试'
        answer['data'] = []
        return json.dumps(answer)


@app.route("/qaByBd/<question>")
def queryByBD(question):
    url = "https://wapiknow.baidu.com" \
          "/index"

    querystring = {"rn": "10", "word": "什么是共保", "lm": "0", "ssid": "0", "from": "0", "bd_page_type": "1",
                   "uid": "B9BFFD2DB0932FDC17AF1039038A5AE7", "pu": "sz@224_240,os@", "init": "middle", "step": "1",
                   "cifr": "p_idx"}

    headers = {
        'pragma': "no-cache",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/65.0.3325.181 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'referer': "http://wapiknow.baidu.com/",
        'cookie': "BAIDUID=B9BFFD2DB0932FDC17AF1039038A5AE7:FG=1; BIDUPSID=B9BFFD2DB0932FDC17AF1039038A5AE7; "
                  "PSTM=1520574165; "
                  "BDUSS=dhOXYxMFNkeXloVEhUeWR6Z1JNbGJ"
                  "-Wk9jLWhiV1pwflltZ1FKZmNOTFJLOUJhQVFBQUFBJCQAAAAAAAAAAAEAAAA6pGNEuMrV4WhlYXZlbgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANGeqFrRnqhaej; BDRCVFR[S4-dAuiWMmn]=I67x6TjHwwYf0; PSINO=7; H_PS_PSSID=1465_21119_20883_22074; Hm_lvt_16bc67e4f6394c05d03992ea0a0e9123=1522461790; Hm_lpvt_16bc67e4f6394c05d03992ea0a0e9123=1522463104",
        'connection': "keep-alive",
        'cache-control': "no-cache",
    }

    base_url = 'https://wapiknow.baidu.com'
    querystring['word'] = question
    response = requests.request("GET", url=url, headers=headers, params=querystring)
    html = etree.HTML(response.text.encode('utf-8'))
    detail_urls = html.xpath('//div[@class="slist"]/p/a/@href')[:3]
    titles = html.xpath('//div[@class="slist"]/p/a/text()')[:3]
    answer = {}
    data_list = []

    for data in zip(titles, detail_urls):
        data_dict = {}
        if data[0].__contains__('百度百科'):
            kw = data[0].split('_')[0]

            if kw == '' or len(kw) == 0:
                kw=question


            url = "https://wapbaike.baidu.com/item/{0}?tj=fr_ik_search".format(kw)
            # querystring = {"scope": "103", "format": "json", "appid": "379020", "bk_key": kw, "bk_length": "600"}
            response = requests.request("GET", url, headers=headers)
            response.encoding = response.apparent_encoding


            html = etree.HTML(response.text)
            try:
                # answer['data'] = json.loads(response.text)['abstract']
                answer['code'] = 200
                answer['message']='解析成功'

                json_data=''.join(html.xpath('//html/head/meta[2]/@content'))

                if json_data.replace('\n','').strip()  == '':
                    json_data=''.join(html.xpath('//div[@class="summary-content"]/p/text()'))

                answer['data'] = json_data
            except Exception as e:
                continue
            return json.dumps(answer)
        else:
            question = data[0]
            next_url = base_url + data[1]
            baike_response = requests.get(url=next_url, headers=headers)
            baike_response.encoding = 'utf-8'
            result = etree.HTML(baike_response.text)
            content = result.xpath('//div[@class="full-content"]/text()')
            if len(content) == 0  or ''.join(content).replace('\n','').strip() == '':
                continue
            data_dict[question] = ''.join(content)
            data_list.append(data_dict)

    answer['code'] = 200
    answer['message'] = '解析成功'
    answer['data'] = data_list
    print(json.dumps(answer))
    return json.dumps(answer)


@app.route("/qademo2", methods=['POST', 'GET'])
def queryBydemo2():
    if request.method == 'GET':
        return render_template('index-demo2.html', error={})
    question = request.form['question']
    url = "https://wapiknow.baidu.com" \
          "/index"

    querystring = {"rn": "10", "word": "什么是共保", "lm": "0", "ssid": "0", "from": "0", "bd_page_type": "1",
                   "uid": "B9BFFD2DB0932FDC17AF1039038A5AE7", "pu": "sz@224_240,os@", "init": "middle", "step": "1",
                   "cifr": "p_idx"}

    headers = {
        'pragma': "no-cache",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/65.0.3325.181 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'referer': "http://wapiknow.baidu.com/",
        'cookie': "BAIDUID=B9BFFD2DB0932FDC17AF1039038A5AE7:FG=1; BIDUPSID=B9BFFD2DB0932FDC17AF1039038A5AE7; "
                  "PSTM=1520574165; "
                  "BDUSS=dhOXYxMFNkeXloVEhUeWR6Z1JNbGJ"
                  "-Wk9jLWhiV1pwflltZ1FKZmNOTFJLOUJhQVFBQUFBJCQAAAAAAAAAAAEAAAA6pGNEuMrV4WhlYXZlbgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANGeqFrRnqhaej; BDRCVFR[S4-dAuiWMmn]=I67x6TjHwwYf0; PSINO=7; H_PS_PSSID=1465_21119_20883_22074; Hm_lvt_16bc67e4f6394c05d03992ea0a0e9123=1522461790; Hm_lpvt_16bc67e4f6394c05d03992ea0a0e9123=1522463104",
        'connection': "keep-alive",
        'cache-control': "no-cache",
    }

    base_url = 'https://wapiknow.baidu.com'
    querystring['word'] = question
    response = requests.request("GET", url=url, headers=headers, params=querystring)
    html = etree.HTML(response.text.encode('utf-8'))
    detail_urls = html.xpath('//div[@class="slist"]/p/a/@href')[:3]
    titles = html.xpath('//div[@class="slist"]/p/a/text()')[:3]
    answer = {}
    data_list = []

    for data in zip(titles, detail_urls):
        data_dict = {}
        if data[0].__contains__('百度百科'):
            kw = data[0].split('_')[0]

            if kw == '' or len(kw) == 0:
                kw = question

            print(kw + '----------------------------')
            url = "https://wapbaike.baidu.com/item/{0}?tj=fr_ik_search".format(kw)
            # querystring = {"scope": "103", "format": "json", "appid": "379020", "bk_key": kw, "bk_length": "600"}
            response = requests.request("GET", url, headers=headers)
            response.encoding = response.apparent_encoding

            print(response.text)

            html = etree.HTML(response.text)
            try:
                # answer['data'] = json.loads(response.text)['abstract']
                answer['code'] = 200
                answer['message'] = '解析成功'

                json_data = ''.join(html.xpath('//html/head/meta[2]/@content'))

                if json_data.replace('\n', '').strip() == '':
                    json_data = ''.join(html.xpath('//div[@class="summary-content"]/p/text()'))

                print(json_data + '*' * 20)
                answer['data'] = json_data
            except Exception as e:
                continue
            print(json.dumps(answer))
            return json.dumps(answer)
        else:
            question = data[0]
            next_url = base_url + data[1]
            print(next_url)
            baike_response = requests.get(url=next_url, headers=headers)
            baike_response.encoding = 'utf-8'
            result = etree.HTML(baike_response.text)
            content = result.xpath('//div[@class="full-content"]/text()')
            if len(content) == 0 or ''.join(content).replace('\n', '').strip() == '':
                continue
            data_dict[question] = ''.join(content)
            data_list.append(data_dict)

    answer['code'] = 200
    answer['message'] = '解析成功'
    answer['data'] = data_list
    print(json.dumps(answer))
    return json.dumps(answer)


@app.route("/qademo3", methods=['POST', 'GET'])
def queryBydemo3():

    if request.method == 'GET':
        return render_template('index-demo3.html', error={})
    url = "http://wechat.riskeys.com/ws_server/answer"
    question = request.form['question']
    payload = "{\"questionId\":2,\"answer\":\"%s\"}"%question
    headers = {
        'connection': "keep-alive",
        'accept-encoding': "gzip, deflate",
        'content-type': "application/json;charset=UTF-8",
        'unionid': "oeDaQxGWMb3iSHKSRvvC6RlMK89Y",
        'source': "anyi",
        'origin': "http://wechat.riskeys.com",
        'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E216 MicroMessenger/6.6.6 NetType/WIFI Language/zh_CN",
        'host': "wechat.riskeys.com",
        'referer': "http://wechat.riskeys.com/wxApp.html?from=groupmessage&isappinstalled=0",
        'accept-language': "zh-cn",
        'accept': "application/json, text/plain, */*",
        'content-length': "52",
        'cache-control': "no-cache",
    }
    response = requests.request("POST", url, data=payload.encode('utf-8'), headers=headers)
    response.encoding=response.apparent_encoding

    data=json.loads(response.text)
    print(data)
    answer=data['data_info']['messageList'][0]['value']
    print(question)
    print(answer)
    #cursor = db.cursor()
    #sql = "INSERT INTO qa (question, answer) VALUES (%s, %s)"
    #cursor.execute(sql,(question,answer))
    #db.commit()
    return json.dumps(json.loads(response.text))



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9009,debug=False)