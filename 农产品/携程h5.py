import requests
from requests.packages import urllib3
import json
urllib3.disable_warnings()

def get_text(url, page):
    '''

    :param url:
    :param page:
    :return:
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36',
        'content-type': 'application/json',
        'Cookie': '_abtest_userid=b6ca4fe8-52e4-42bf-be80-915aed481056; _RSG=Tyq26c_bZQBuqCMujc5GDB; _RDG=28d9e3222c72ce2538232cf6dc61bf031f; _RGUID=b6a397f9-860b-4f1d-b350-166b7858cd38; _ga=GA1.2.412926983.1593348862; _gid=GA1.2.1828196642.1593348862; MKT_CKID_LMT=1593348862035; MKT_CKID=1593348862034.lmokg.4x40; _jzqco=%7C%7C%7C%7C1593348862448%7C1.1660698745.1593348862031.1593396431656.1593396511873.1593396431656.1593396511873.undefined.0.0.6.6; __zpspc=9.2.1593394447.1593396511.4%234%7C%7C%7C%7C%7C%23; _bfi=p1%3D102003%26p2%3D102003%26v1%3D6%26v2%3D5; appFloatCnt=6; GUID=09031176110457811441; MKT_Pagesource=H5; Union=OUID=&AllianceID=66672&SID=1693366&SourceID=&AppID=&OpenID=&createtime=1593397077&Expires=1594001877457; hoteluuid=FtSc2c85zc0FC0zO; hoteluuidkeys=084yBlEXUelDE9Gr7YDnYNbEXY30e1qEo0jHLWLYHfe89xDbWmGjPYM1YADKf4vnQjHYcHj13yZ4ISXjtYdsv79yH1yk4jOPvh6efBYF9jSoyPYlFvFqEaGYZnwLdjphebki37xGYmYoLvU9esqYlUip3YZY1YzYbZYmPi8HioMiBnjkYPBya1woZyXGwqSiOUjLXwqnyUYTnRh0J7TvshiAbiXlvGOy8XWHNyOqyZLJAmycGvXYBmydzjpPJsQwZNYL6wHpjUTJPdr5AwlSW0dyM8E4HWbUrtFRlYkHia3Eq9JQLWHTEfbR4Yt4xO5edXyfcYU9jA6wB5w3ti4TwqYfDjkQwFHvl4; _bfa=1.1593348859257.3j6i0p.1.1593348859257.1593416672159.4.11.228032; _RF1=60.176.148.245',
        'cookieOrigin': 'https://m.ctrip.com',
        'Host': 'm.ctrip.com',
        'Origin': 'https://m.ctrip.com',
        'Referer': 'https://m.ctrip.com/webapp/hotel/hoteldetail/dianping/345041.html?&fr=detail&atime=20200629&days=1'
    }
    params = {
        'basicRoomName': "",
        'groupTypeBitMap': '2',
        'cid': "09031176110457811441",
        'ctok': "",
        'cver': "1.0",
        'extension': [],
        'lang': "01",
        'sid': "8888",
        'syscode': "09",
        'xsid': "",
        'hotelId': '345041',
        'needStatisticInfo': '0',
        'order': '0',
        'pageIndex': page,  # 第几页
        'pageSize': '10',  # 每次加载10条
        'tagId': '0',
        'travelType': '-1',
        'auth': "",
    }
    response = requests.post(url, headers=headers, data=json.dumps(params), verify=False)
    html = response.text
    # print(html)
    return html


def get_parser1(html):
    '''
    解析
    :param html:
    :return:
    '''
    parser_ls = []
    data = json.loads(html).get('othersCommentList')
    for i in data:
        x_name = i['userNickName']
        x_type = i['travelType']
        x_num = i['ratingPoint']
        x_starttime = i['checkInDate']
        x_pltime = i['postDate']
        x_fangxing = i['baseRoomName']
        x_content = i['content']
        #酒店回复这一段有个问题,如果酒店不回复,那么是完全没有feedbackList这个键的,所以提前处理一下
        try:
            if i['feedbackList']:
                x_jdcontent = i['feedbackList']
                if len(x_jdcontent) > 0:
                    x_jdcontent = x_jdcontent[0]['content']
                else:
                    x_jdcontent = '没有回复'
            else:
                x_jdcontent = '没有回复'
        except Exception as e:
            x_jdcontent = '没有回复'

        print(x_name)
        print(x_type)
        print(x_num)
        print(x_starttime)
        print(x_pltime)
        print(x_fangxing)
        print(x_content)
        print(x_jdcontent)
        print('*' * 200)
        p_t = [x_name, '\r', x_type, '\r', x_num, '\r', x_starttime, '\r', x_pltime, '\r', x_fangxing, '\r', x_content,
               '\r', x_jdcontent, '\r']
        parser_ls.append(p_t)
    return parser_ls


def wride(parser_ls):
    '''
    这边传进来的是列表套列表,先循环拿到正常的列表,然后再传入单个的字段,要求存txt
    :param parser_ls:
    :return:
    '''
    try:
        with open('./xiecheng.txt', 'a+', encoding='utf-8')as f:
            for i in parser_ls:
                for j in i:
                    f.write(str(j))
            f.write('\r\n')
            f.close()
            print('写入完毕')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    '''
    原本要求是http://hotels.ctrip.com/hotel/345041.html,爬单个酒店的评论及酒店回复情况的
    但是有js加密,eleven参数不好弄,用f12改成手机界面的url,绕过js加密
    '''
    url = 'https://m.ctrip.com/restapi/soa2/16765/gethotelcomment?&_fxpcqlniredt=09031176110457811441'
    for page in range(1, 10):#翻10页
        html = get_text(url, page)
        print(len(html))
        ls = get_parser1(html)
        wride(ls)
