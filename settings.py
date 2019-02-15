headers = {
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
		'Content-Type': 'application/x-www-form-urlencoded'
		}
#登录时post的数据
data = {
		'username':'',
		'pwd':'',
		'remember': 'true',
		's_token': '',
		'dat':'',
		'wlfstk_datk':'',
		'risk_jd[eid]': 'a78174c01e2c4e61abd157e81cbe56f2168545174',
		'risk_jd[fp]': '927e4a3562f7e3ccc7b89cfaedc93a55',
		'risk_jd[token]':'',
		'verifytoken': ''
		}

#检测像素点相似度的阈值
threshold = 6

#更新验证码时post的数据
rf_data = {
		'si':'',
		'version': 1,
		'se':'',
		'lang':''
		}
#账户信息
username = '账户'
password = '密码'