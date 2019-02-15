import requests
import execjs
import base64
import re
import time
from settings import *
import json
from PIL import Image 
import math,random
import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 

#定义一个全局的session对象,用于保存返回的cookie值
session = requests.session()

def x(a):
    """验证码更新时需要的nonce参数"""
    c = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    t = ''
    e = 0
    while e<a:
        t += c[math.floor(35 * random.random())]
        e += 1 
    return t

def time33(e):
    t = 5381
    a = 0
    r = len(e)
    while a<r:
        t += (t << 5) + ord(e[a])
        a += 1 
    return 2147483647 & t

def _get_username_pwd(rsaString):
    """密码用户名加密
        rsaString:网页返回的rsaString字符串
    """
    file = open(r'sj_jd_pwd.js').read()
    js = execjs.compile(file)
    name_pwd = js.call('enc_pwd_name',rsaString,username,password)
    name = name_pwd['username']
    pwd = name_pwd['pwd']
    return name,pwd

def _get_args():
    """获取网页返回的参数"""
    url = 'https://home.m.jd.com/myJd/home.action'
    try:
        html = session.get(url,headers=headers).text
        token = re.findall('str_kenString = \'(.*?)\'',html)
        token = token[0] if token else None
        md5Fun = re.findall('function getDat.*?\}',html)[0]
        rsaString = re.findall('str_rsaString = \'(.*?)\'',html)[0]
        sessionId = re.findall('var jcap_sid = \'(.*?)\'',html)[0]
        return token,rsaString,md5Fun,sessionId
    except Exception as er:
        print(er)

def _compele_login_data():
    """登录需要post的data"""
    url = 'https://payrisk.jd.com/m.html'
    token,rsaString,md5Fun,sessionId = _get_args()
    data['verifytoken'] = _parse_verifyCode(sessionId)
    finger_token = re.findall('var jd_risk_token_id = \'(.*?)\'',session.get(url,headers=headers).text)[0]
    name,pwd = _get_username_pwd(rsaString)
    file = open(r'md5.js').read()
    file += md5Fun
    dat = execjs.compile(file).call('getDat',name,pwd)
    data['s_token'] = token 
    data['dat'] = dat 
    data['wlfstk_datk'] = dat 
    data['risk_jd[token]'] = finger_token
    data['username'] = name
    data['pwd'] = pwd
    return data

def _download_pic(arg,st,sessionId,Codejs):
    #验证码验证获取verify_token
    verifyurl = 'https://jcap.m.jd.com/cgi-bin/api/check'
    results = json.loads(arg)
    pic1 = results['b1'].replace('data:image/jpg;base64,','')
    pic2 = results['b2'].replace('data:image/jpg;base64,','')
    with open('fullpic.png','wb') as f:
        f.write(base64.b64decode(pic1.encode()))
    with open('target.png','wb') as f:
        f.write(base64.b64decode(pic2.encode()))
    print('step_2:Get pic successfully')
    pos = _find_position()
    pos_arg = json.dumps({"ht":171,"wt":293,"x":pos[0],"y":pos[1]},ensure_ascii=False)
    print('图片坐标：',pos_arg)
    ctData = Codejs.call('get_tk',st,sessionId,pos_arg)
    html_3 = session.post(verifyurl,data=ctData,headers=headers).json()
    return html_3

def _parse_verifyCode(sessionId):
    """验证码解析函数
        sessionId:网页中返回的参数
    """
    initurl = 'https://jcap.m.jd.com/cgi-bin/api/fp'
    verifyurl = 'https://jcap.m.jd.com/cgi-bin/api/check'
    refreshurl = 'https://jcap.m.jd.com/cgi-bin/api/refresh'
    file = open(r'code_verify.js').read()
    Codejs = execjs.compile(file)
    ctData = Codejs.call('get_ct',sessionId)
    try:
        #初始化获得一个st码用于第二步获得验证码图片
        html_1 = session.post(initurl,data=ctData,headers=headers).json()
        print('step_1:Get st/fp successfully')
        #post提交获得验证码图片，保存到本地
        ctData = Codejs.call('get_tk',html_1['st'],sessionId,'')
        html_2 = session.post(verifyurl,data=ctData,headers=headers).json()
        html_3 = _download_pic(html_2['img'],html_2['st'],sessionId,Codejs)
        while html_3['code'] != 0:
            refresh_arg = json.dumps({'nonce':x(16),'token':html_2['st'],'sid':sessionId},ensure_ascii=False)
            se = Codejs.call('get_se',refresh_arg)
            rf_data['si'] = sessionId
            rf_data['se'] = se 
            html_2 = session.post(refreshurl,data=rf_data,headers=headers).json()
            if html_2['code'] == 0:
                html_3 = _download_pic(html_2['img'],html_2['st'],sessionId,Codejs)
            print('正在重试！')
            time.sleep(0.5)
        print('step_3:Get verifyToken successfully')
        return html_3['vt']
    except Exception as er:
        print(er)

def _find_position():
    """寻找位置参数
    使用列表添加相似点，求均值近似求出位置
    """
    prob = list()
    full_pic = Image.open('fullpic.png')
    pos_pic = Image.open('target.png')
    width_1,height_1 = pos_pic.size
    width_2,height_2 = full_pic.size
    n = (height_1//2)-3
    for i in range(width_2):
        for j in range(height_2):
            f_pix = full_pic.getpixel((i,j))
            p_pix = pos_pic.getpixel((width_1//2,n))
            if abs(f_pix[0]-p_pix[0])<threshold and abs(f_pix[1]-p_pix[1])<threshold and abs(f_pix[2]-p_pix[2])<threshold:
                prob.append((i,j))
    if prob:
        x = sum([i[0] for i in prob])//len(prob)
        y = sum([i[1] for i in prob])//len(prob)
        return x,y
    else:
        return 10,10

def main():
    """登录主函数"""
    data = _compele_login_data()
    url = 'https://plogin.m.jd.com/cgi-bin/mm/domlogin'
    main_url = 'https://home.m.jd.com/myJd/newhome.action?sid={}'.format(session.cookies['sid'])
    headers['Host'] = 'plogin.m.jd.com'
    try:
        response = session.post(url,data=data,headers=headers).json()
        if response['errcode'] == 0:
            print('登录成功！')
            headers['Host'] = 'home.m.jd.com'
            html = session.get(main_url,headers=headers)
            return True
        print('登录失败:',response['message'])
    except Exception as er:
        print(er)

def bought_info():
    """获取已购买商品的信息"""
    print('Begin login!')
    if main():
        headers.pop('Host')
        print('Begin shopping list_info !')
        car_url = 'https://p.m.jd.com/cart/cart.action'
        base_deal_list_url = 'https://wqdeal.jd.com/bases/orderlist/deallist?callersource=mainorder&order_type=3&start_page=%d&page_size=10&last_page=%d&callback=dealListCbA&isoldpin=0&utfswitch=1&traceid={}&t={}&sceneval=2&&g_ty=ls&g_tk={}'
        if 'wq_skey' in session.cookies:
            wq_skey = session.cookies['wq_skey']
        else:
            wq_skey = ''
        headers['Referer'] = 'https://wqs.jd.com/order/orderlist_merge.shtml?tab=1&ptag=7155.1.11&sceneval=2'
        now = int(time.time()*1000)
        file = open(r'get_traceid.js').read()
        traceid = execjs.compile(file).call('e')
        base_deal_list_url = base_deal_list_url.format(traceid,now,time33(wq_skey))
        deal_list_url_1 = base_deal_list_url % (1,0)
        html = session.get(deal_list_url_1,headers=headers).text
        result = eval(re.findall('dealListCbA\((.*)\)',html,re.S)[0])
        yield result
        n = 2
        while True:
            deal_list_url_2 = base_deal_list_url % (n,1)
            html = session.get(deal_list_url_2,headers=headers).text
            if not int(re.findall('total_count.*?\"(\d+)\"',html)[0]): 
                break
            n += 1
            yield eval(re.findall('dealListCbA\((.*)\)',html,re.S)[0])

def save_goods_info():
    df = pd.DataFrame()
    for i in bought_info():
        deal_list = i['deal_list']
        for each in deal_list:
            seller_info = dict()
            seller_info['date'] = pd.to_datetime(each['dateSubmit'])
            seller_info['price'] = float(each['total_price'])/100
            seller_info['state'] = each['stateName']
            seller_info['number'] = len(each['trade_list'])
            seller_info['title'] = [i['item_title'] for i in each['trade_list']]
            df = df.append(seller_info,ignore_index=True)
    df.to_excel('jd_goods.xlsx')
    print('Get jd_good successfully','The End!',sep='\n')

def visualization():
    df = pd.read_excel('jd_goods.xlsx')
    df.sort_values(by='date',inplace=True)
    a = df.resample(rule='12M',closed='left',on='date').sum() #on针对dateframe对象的参数
    a.plot(kind='bar')
    for i,j in enumerate(a['price']):
        plt.text(i+0.12,j+8,int(j),horizontalalignment='center')
    plt.xticks(rotation=270)
    plt.ylim([0,8000])
    plt.ylabel('price')
    plt.title('Date-Price-relationship')
    b = df.groupby('state').count()
    print('总消费:',df['price'].sum())
    a['percent'] = a['price'].div(df['price'].sum())
    a.sort_values(by='price',ascending=False,inplace=True)
    print(a)
    b= df[(df['date']>pd.to_datetime('2014-12-31')) & (df['date']<=pd.to_datetime('2015-12-31'))].loc[:,['price','title']]
    print(b)
    plt.tight_layout() 
    plt.show()

if __name__ == '__main__':
    # save_goods_info()
    # visualization()
    main()