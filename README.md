# JdLogin

使用python模拟登陆手机jd的网址，成功获取全部订单信息。
包括双图形验证码的点击识别，密码用户名的js逆向。

## 安装

### 安装Python

至少Python3.5以上

修改settings.py文件里面的账户和密码

#### 安装依赖

```
pip3 install -r requirements.txt
```
##### 文件说明

code_verify.js:验证码加密函数

sj_jd_pwd.js:密码用户名加密函数

settings.py:设置用户名密码及像素相识度阈值

md.js:用于网页源码中的md5函数

get_traceid.js：获取历史订单时生成参数，根据cookie返回值计算
