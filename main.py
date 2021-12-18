from typing import Optional
import hashlib
import redis
import ntce
import proxy

from fastapi import FastAPI, Header
from pydantic import BaseModel

# debug
import uvicorn

app = FastAPI()
key = 'j2wAS(q2oj$A@CEQS'
# redis 连接池
Pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=9, password='12345', decode_responses=True)


# 传入参数
class Param(BaseModel):
    name: str
    id_card: str
    yzm: str
    sign: str


@app.get('/ntce/yzm')
def yzm():
    res = ntce.get_yzm()
    return res


@app.post("/ntce/query")
def query(param: Param, cookie_str: Optional[str] = Header('cookie_str', convert_underscores=False)):
    id_card = param.id_card
    name = param.name
    sign = param.sign
    yzm = param.yzm
    param_str = id_card + '&' + name + '&' + yzm + '&' + key
    hash = hashlib.md5(param_str.encode(encoding='UTF-8')).hexdigest()
    result = {}
    if hash != sign:
        # 校验结束
        result['isOk'] = 'N'
        return result
    else:
        data = ntce.query_ntce(name, id_card, yzm, cookie_str)
        result = {
            'isOk': 'Y',
            'data': data
        }
    return result

def can_pass_fixed_window(user, action, time_zone=60, times=30):
    """
        :param user: 用户唯一标识
        :param action: 用户访问的接口标识(即用户在客户端进行的动作)
        :param time_zone: 接口限制的时间段
        :param time_zone: 限制的时间段内允许多少请求通过
        """
    key = '{}:{}'.format(user, action)
    redis_conn = redis.Redis(connection_pool=Pool, decode_responses=True)
    # redis_conn 表示redis连接对象
    count = redis_conn.get(key)
    if not count:
        count = 1
        redis_conn.setex(key, time_zone, count)
    if count < times:
        redis_conn.incr(key)
        return True
    return False

@app.get("/")
def test():
    rdb = redis.Redis(connection_pool=Pool, decode_responses=True)
    rdb.set("name", "aaa")
    print(rdb.get("name"))

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8090)