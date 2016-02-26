# -*- coding: UTF-8 –*-
# Create your views here.
from django.http import HttpResponse
from wechat.official import WxApplication, WxTextResponse
from django.views.decorators.csrf import csrf_exempt

#Append "Echo: " text before every echo
class WxTextResponseLocal(WxTextResponse):
    def __init__(self, text, request):
        super(WxTextResponseLocal, self).__init__(text, request)
        self.text = 'Echo: ' + self.text 

class EchoApp(WxApplication):
    """把用户输入的文本原样返回。
    """
    WELCOME_TXT = u'欢迎来到回声公众号！Everything you said is matter!'
    SECRET_TOKEN = '123456789'
    APP_ID = 'wx6d8b8d87d7cc4662'
    ENCODING_AES_KEY = 'Egw2nZfAWc7surm80mHL6lOcLDHLAOKWysR2H4vJjMv'

    def on_text(self, req):
        #Original response
        #return WxTextResponse(req.Content, req)
        
        #Overrided Response
        return WxTextResponseLocal(req.Content, req)

@csrf_exempt
def wechat(request):
    # 微信配置验证代码
    #result = request.GET
    #echo_str =  result['echostr']
    #app = EchoApp()
    # 返回echo_str给微信即可

    #return HttpResponse(echo_str)
    #微信配置验证代码结束

    #Echo testing 
    app = EchoApp()
    result = app.process(request.GET, request.body)
    
    return HttpResponse(result)
