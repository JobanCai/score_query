import requests
import base64

if __name__ == '__main__':
    header = {
        'referer': 'http://cjcx.neea.edu.cn/',
        'host': 'search.neea.edu.cn',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    response = requests.get('http://search.neea.edu.cn/QueryMarkUpAction.do?act=doQueryCond&pram=results&community=Home&sid=2nasVMoohJ6cFnsQEIjGYmh', headers=header);
    # 1.获取cookie完成
    print(response.cookies.get_dict())

    header = {
        'referer': 'http://search.neea.edu.cn/QueryMarkUpAction.do?act=doQueryCond&pram=results&community=Home&sid=2nasVMoohJ6cFnsQEIjGYmh',
        'host': 'search.neea.edu.cn',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    cookie_1 = {
        'BIGipServersearch.neea.edu.cn_internal_pool': response.cookies.get_dict()['BIGipServersearch.neea.edu.cn_internal_pool'],  # 此处填入浏览器cookie
        'esessionid': response.cookies.get_dict()['esessionid']
    }
    r = requests.get('http://search.neea.edu.cn/Imgs.do?act=verify&t=0.8841180045674784', headers=header, cookies=cookie_1)
    cookie_1['verify'] = r.cookies.get_dict()['verify']
    image = r.content
    imgName = 'yzm'
    destDir = "D:\\"
    print("保存图片" + destDir + imgName + '.jpg' + "\n")
    # try:
    #     with open(destDir + imgName, "wb") as jpg:
    #         jpg.write(image)
    # except IOError:
    #     print("IO Error")
    # finally:
    #     jpg.close
    file = open(destDir + imgName + '.jpg', 'wb')
    file.write(image)
    file.close()

    # 2.获取验证码图片完成
    print(cookie_1)
    # 3.开始查询结果数据