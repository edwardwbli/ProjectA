#encoding=utf-8

from xml.dom import minidom

XML = '''<xml>
 <ToUserName><![CDATA[toUser]]></ToUserName>
 <FromUserName><![CDATA[fromUser]]></FromUserName> 
 <CreateTime>1348831860</CreateTime>
 <MsgType><![CDATA[text]]></MsgType>
 <Content><![CDATA[this is a test]]></Content>
 <MsgId>1234567890123456</MsgId>
 </xml>
'''
class WxRequest(object):

    def __init__(self, xml=None):
        if not xml:
            return
        doc = minidom.parseString(xml)
        params = [ele for ele in doc.childNodes[0].childNodes if isinstance(ele, minidom.Element)]
       
        for param in params:
            if param.childNodes:
                text = param.childNodes[0]
                self.__dict__.update({param.tagName: text.data})
            else:
                self.__dict__.update({param.tagName: ''})

if __name__ == '__main__':

    wxr = WxRequest(XML)
    
    print wxr.__dict__
