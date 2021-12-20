import requests
import ddddocr
import time
from bs4 import BeautifulSoup

# 获取验证码和cookies


def get_yzm():
    header = {
        'referer': 'http://cjcx.neea.edu.cn/',
        'host': 'search.neea.edu.cn',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    response = requests.get(
        'http://search.neea.edu.cn/QueryMarkUpAction.do?act=doQueryCond&pram=results&community=Home&sid=2nasVMoohJ6cFnsQEIjGYmh',
        headers=header);
    # 1.获取cookie完成
    print(response.cookies.get_dict())

    header = {
        'referer': 'http://search.neea.edu.cn/QueryMarkUpAction.do?act=doQueryCond&pram=results&community=Home&sid=2nasVMoohJ6cFnsQEIjGYmh',
        'host': 'search.neea.edu.cn',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    cookie_1 = {
        'BIGipServersearch.neea.edu.cn_internal_pool': response.cookies.get_dict()[
            'BIGipServersearch.neea.edu.cn_internal_pool'],  # 此处填入浏览器cookie
        'esessionid': response.cookies.get_dict()['esessionid']
    }
    r = requests.get('http://search.neea.edu.cn/Imgs.do?act=verify&t=0.8841180045674784', headers=header,
                     cookies=cookie_1)
    cookie_1['verify'] = r.cookies.get_dict()['verify']
    image = r.content
    imgName = str(int(round(time.time() * 1000)))
    destDir = '/images/'
    print("保存图片" + destDir + imgName + '.jpg' + "\n")
    file = open(destDir + imgName + '.jpg', 'wb')
    file.write(image)
    file.close()

    # ocr 识别验证码
    ocr = ddddocr.DdddOcr()
    with open(destDir + imgName + '.jpg', 'rb') as f:
        img_bytes = f.read()
    yzm_str = ocr.classification(img_bytes)

    cookie_str = ''
    for key, value in cookie_1.items():
        cookie_str += ';' + key + '=' + value

    res = {
        'img_path': destDir + imgName + '.jpg',
        'yzm_str': yzm_str,
        'cookie_str': cookie_str
    }
    return res

# 查询成绩


def query_ntce(name: str, id_card: str, yzm: str, cookie_str: str):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'search.neea.edu.cn',
        'Origin': 'http://search.neea.edu.cn',
        'Referer': 'http://search.neea.edu.cn/QueryMarkUpAction.do?act=doQueryCond&pram=results&community=Home&sid=2nasVMoohJ6cFnsQEIjGYmh',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Upgrade-Insecure-Requests': '1'

    }
    data = {
        'pram': 'results',
        'ksxm': '2nasVMoohJ6cFnsQEIjGYmh',
        'nexturl': '/QueryMarkUpAction.do?act=doQueryCond&sid=2nasVMoohJ6cFnsQEIjGYmh&pram=results&zjhm=' + id_card + '&xm=' + name,
        'xm': name,
        'zjhm': id_card,
        'verify': yzm
    }
    headers['cookie'] = cookie_str
    re = requests.post('http://search.neea.edu.cn/QueryMarkUpAction.do?act=doQueryNtceResultsList',
                       data, headers=headers)
    html_str = re.content.decode('utf-8')
    return parse(html_str)


# 解析结果


def parse(html_str: str):
    result = {}
    data_list = []
    soup = BeautifulSoup(html_str, 'html.parser')
    if soup.select(".oder tr") is None:
        result['isOk'] = 'N'
    else:
        result['isOk'] = 'Y'
        for idx, tr in enumerate(soup.select(".oder tr")):  # 笔试成绩
            if idx != 0:
                tds = tr.find_all('td')
                data_list.append({
                    '科目': tds[0].contents[0],
                    '报告分': tds[1].contents[0],
                    '合格与否': tds[2].contents[0],
                    '准考证号': tds[3].contents[0],
                    '考试批次': tds[4].contents[0],
                    '有效期限': tds[5].contents[0],
                    '考试省份': tds[6].contents[0],
                })
        result['written_test'] = data_list
        data_list = []
        for idx, tr in enumerate(soup.select(".odere tr")):  # 笔试成绩
            if idx != 0:
                tds = tr.find_all('td')
                data_list.append({
                    '科目': tds[0].contents[0],
                    '合格与否': tds[1].contents[0],
                    '准考证号': tds[2].contents[0],
                    '考试批次': tds[3].contents[0],
                    '考试省份': tds[4].contents[0],
                })
        result['interview'] = data_list
    return result

if __name__ == '__main__':
    get_yzm()
