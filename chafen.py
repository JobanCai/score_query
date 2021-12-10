from urllib.parse import urlencode

import requests

if __name__ == '__main__':
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'search.neea.edu.cn',
        'Origin': 'http://search.neea.edu.cn',
        'Referer': 'http://search.neea.edu.cn/QueryMarkUpAction.do?act=doQueryCond&pram=results&community=Home&sid=2nasVMoohJ6cFnsQEIjGYmh',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Upgrade-Insecure-Requests': '1'

    }
    cookies = {
        'BIGipServersearch.neea.edu.cn_internal_pool': '1889585162.37407.0000',  # 此处填入浏览器cookie
        'esessionid': '03301220FEC5B0284FD138786E5CE639',
        'verify': 'f4385d11d8db8b85fa1a46eaea2c2162'
        # 'Hm_lvt_dc1d69ab90346d48ee02f18510292577': '1638850843',
        # 'Hm_lpvt_dc1d69ab90346d48ee02f18510292577': '1638859228'
    }
    data = {
        'pram': 'results',
        'ksxm': '2nasVMoohJ6cFnsQEIjGYmh',
        'nexturl': '/QueryMarkUpAction.do?act=doQueryCond&sid=2nasVMoohJ6cFnsQEIjGYmh&pram=results&zjhm=452123199404022545&xm=李燕丽',
        'xm': '李燕丽',
        'zjhm': '452123199404022545',
        'verify': '8nnc'
    }
    cookie_str = ''
    for key,value in cookies.items():
        cookie_str += ';' + key + '=' + value
    headers['cookie'] = cookie_str
    re = requests.post('http://search.neea.edu.cn/QueryMarkUpAction.do?act=doQueryNtceResultsList',
                       data, headers=headers)
    print(re.content.decode('utf-8'))