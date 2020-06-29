import requests
from lxml import etree


import json

def get_text(url,page):
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
    html = response.content.decode('utf-8')
    print(html)
    page+=1
    return html


def get_parser(html):

    parser_ls=[]
    html = etree.HTML(html)
    ls = html.xpath('//div[@class="dn hotel-t-b-border"]/div')
    for i in ls:
        x_name = i.xpath('.//p[@class="comment-title"]/span[1]/text()')[0]  # 用户名
        x_type = i.xpath('.//p[@class="dn-checkin"]/span[2]/em/text()')[0]  # 出游类型
        x_num = i.xpath('.//div[@class="g-ve"]/span/strong/text()')[0]  # 评分
        x_starttime = i.xpath('.//p[@class="dn-checkin"]/span[1]/text()')[0]  # 入住时间   两个连在一起需要拆分
        x_starttime = x_starttime.split('，')[0].split('入住')[0]
        x_pltime = i.xpath('.//p[@class="dn-checkin"]/span[1]/text()')[0]  # 评论时间
        x_pltime = x_pltime.split('，')[1].split('发表')[0]
        x_fangxing = i.xpath('.//p[@class="dn-checkin"]/span[3]/text()')[0]  # 房型
        x_content = i.xpath('.//div[@class="cbd"]/p/text()')[0]  # 评论内容
        x_jdcontent = i.xpath('.//div[@class="cm"]/ul/li[1]/text()')  # 酒店评论
        if len(x_jdcontent) > 0:
            x_jdcontent = x_jdcontent[0]
        else:
            x_jdcontent = '酒店暂未回复'
        print(x_name)
        print(x_type)
        print(x_num)
        print(x_starttime)
        print(x_pltime)
        print(x_fangxing)
        print(x_content)
        print(x_jdcontent)
        print('*' * 200)
        parser_ls.append(x_name)
        parser_ls.append(x_type)
        parser_ls.append(x_num)
        parser_ls.append(x_starttime)
        parser_ls.append(x_pltime)
        parser_ls.append(x_fangxing)
        parser_ls.append(x_content)
        parser_ls.append(x_jdcontent)
    return parser_ls


def wride(parser_ls):
    with open('./xiecheng.txt','a+',encoding='utf-8')as f:
        f.writelines(parser_ls)
        f.write('\r\n')
        f.close()
        print('写入完毕')
if __name__ == '__main__':
    url = 'https://m.ctrip.com/restapi/soa2/16765/gethotelcomment?&_fxpcqlniredt=09031176110457811441'
    for page in range(10):
        html=get_text(url,page)
        ls=get_parser(html)
        wride(ls)