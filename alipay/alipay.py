# -*- coding: utf-8 -*-

import sys
import requests
import qrcode
from urllib.parse import quote 
import OpenSSL.crypto as ct #pip install pyOpenSSL
import base64

sys.path.append("../")
from vos.vos_misc import *

#Smile 
#privkey = "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCIX0l1A3pbAtEkFESaZ4o8VNyEwWLMWt2h1pFGvrj1MOWO5wPzwQJjjX+DRG3823R2Hy/2xYF5orCBzDg+SnEmcqdIYAszfiHIBsu2QwzQ96AibqNRYtkRrSNVejMKHfgzu7tI5UXIaN/QMbQBvD+4WO25ttsasPRGLfpW+Hhv9qxth1WjW5ap3cKTVWsrRJKakch/0QVpyvIHJGRH9fdDRGJBLFyErXIpc2OdSkTWMxIH6OEDcgr4oyUkl/DkOIA+8F14JgVHSkGwqQ0F1KMSlLZ+H2DoLVdDXm3KdbdbeF/XPyVjzEG1pV1Iru+t6OUtc42nrjSOYKoYg/HZAryNAgMBAAECggEADCZpNgq0SQ2MMqm3nwYgk9V/vDg6pDhoTLYARYxSkE3l9gBxIrOMkfAWb0yWfBPVYXzP2i2opnyvOzFFxY7+W82VR+Z+uPzA58BrP/bjWm7ljovK80JaUq/ZWRFFIN6gsYNFYW5D9GIbpsH25ryt9K+/pm87QDqJ2QLZrgv/NwJi9nRAhT0LAW3ezVVwUb5LdvqOmDFiR4/GTnr25pVpUNvJWAMrCooc8zrdpYAn+Q0/D0xhOSFxA/itTlcZIYr3BtvAupbyEUQghnhQoFYzgUuJA46qyVQWQS+bNhws0s3LW0NYc+KQVilnYuYfIGKawniv/w9BN1zwYDADlfIDxQKBgQC/ij0xYSOwVTaVtN/B2/TqnHBAXGYfML+VqOVq4bMWR9rwZ9UIwOGNkA/M677M00oW+Nm3wLHTMp8G74VGk4wZqFEjGjnx6Zdl1oY9hNeG54L8VKHaoycWbDSP5umBQ0y8ZlvfDn0Q29xRMpOWS+3T7uZ2HjKGF9JMi+JElbwAWwKBgQC2RCxqx98QF6w1A82rczxP8ZdE8BQGfmbeAEc+bag0Z1ljpxMPpTslNXqGJgttFdc4JvpxwUDCbmMdJ4H2WtdBHDi9qXpnzHAYSRwkZkCA/FSpf2SbRUsEgBjhzactgIiqoPPylTAj4pvz0+zf088sjiaQ8yJRLoPawn9mw8xLNwKBgCu9b9f07Od5ritl0Ks+haGF9ARelVuOEFIm7a0IuZLe+dpoe7eyBFAFk/Yh58JyhbrVPTK/KFyodLRqwi6pxxac31p6xLy/sTkqUiF+UpGWEM16rjN1ipmOQDqUasKAEef8IALCFkFhU+CfAiESWc9KAQr8PmFs0zNzxkoPP419AoGAY82kvLvBKyCrTURN5GnvRp81g6wqavvf/AQO/uIwzrEgw26DA3gokNFdzAMdEph5BuhhDtURTuX/I8G0al+HqsF3WHNq8VeCsemmnU/YVkjVWxLE1jj1QPubpFlmB4ZwT25e5iBHAf9eAf+zn0RuFymneIuJ6QYdcTY7aNwiC7UCgYEAsY8Ak0kVY5KMx2kw5VrCYyPEeERA3hWUcfH5rIxo+tvoSnf62P+yy/JMG1ei6Map9x+IuMNsI97sYZQykIEDod65mRii9bVBfypbgyDNZm4AtddYkDrMlBXP8vsHeN0DpgDYIzWTsDZl6thIRp/9UizmnEE5OtsgR47ZhynT110="
#app_id= "2021002118605358"

#Bob
app_id= "2021002124649069" 
privkey = "MIIEowIBAAKCAQEAmrbzgal/tguqw0CU1DL9ZSul0zaACUbk9AZ/+O1481NYdL2zWg8ztfDM4cf1ayuf0qpwRW72FoHthYS31UUNCYOvkVR1XKkm9/973sx+nl2b1zx5OBD1ptrF0T+RFVqyIKkzy1zX7sMN0zTxwJiZjozPz3qKCWq/jsqkWorTXepmAdRA0CUI0+lIhGegQbpBeJujWcIRMJU6UEvv7zoFaBVThnHuj906nk4HqEpmTqLpRz4yVirNtH5KJOwj81BOHn5J35FHECiWFfMC2PbQvEyS8qLIR/xSMgl8PZhP85k6vohf+V7Z6Jsda9hnxWw9c133X+R93sCrrPuIQvx1dQIDAQABAoIBAFcevnA9KhUw7K+WJjh3ngjiUzZkciTHLxXasyVRU9JxFFZonB4SgWPqfPSGzMPUhOLz5tSybxCtiTquSXZms7iv1qVXkd7jwXXU/8OuE37J53+EJh5ULoAOoWX7DY+gyr1piijx1wY0AAz2u0tgoteKo1qJ/kDfQ478vR/fHLa86896Dp5tB/vrgEzyxeZ2k1qAKrmVvxCC6Q4m/1maR4IXEbH+HNLuz7vKGYnbrrdGhLxNLqD3gzutl1JZhZrI4wBbCyaCx5HOIiUI+fBc2ux0n3yCOqGC2DOkrvFPHCfQwgJXf3xfCxn64Px2qBiT5i6C7JQV7IB6YuNmlpCJseECgYEA7FjuTrt76DS77wEoTnBWeeLpczLvwZE+uU9SzY0Yk0EGSaacp/p0rppBr5ERSgcfVxaCDxckWnCBhxfYftZUWkmcMBAqXb4nTijv5wL6JRHsoFO9YKbS/4zlkUENYxVRYa8ugqTQzGUZJdGczshOLdCRtp67BDDVvs3yHFGD8tcCgYEAp5RTAdaJOogRIPW2gPr677NOXwh2WcpHELq3OSHbEfLnKqoronoGIpy0A5lvNuWHQuxoJyTJ7mM5uwEx4+dxECAmALcqNnuIDT7KZk0k0469w1Sv25a+7SeTchN5y3ew8YMMYWHiTGIApHmaoSbgsRxTMji8s0tr0U4vCKsLnJMCgYBSZpsHRiRoC+Kt7GhiGJZ9vlgH+u1OPlZxAy/qTFQSGuyXRwh9JDwEF/HoxRoTBjKuCUHlAvuAsJLoR68KYa1dISbcNvaeYkqP3IPvtcECpaIrL6bqCJ+tyzDKmLSTI/6QoSQFFnNZn7HJ1q/mBD4FiR8UXXj0eBY9hM3xg5YOVwKBgHfwhwCXxhwoauoGMxtZhuSslvkZm2tkhTyKBr1TZ/IOwjkdFqHxaBa5xXWWCa1m1kql3V22zPhb+GPJ1SVi7t81wz1b21CnVZb1S/OwXx0z2snFASDPYdNnMfbBzbg88F3LB79jSY6VzhPqHSweIU9iEIGvbg99eauSo8M2eNcVAoGBAJtc7pwduQ+Od2lxYURtfvrTi+L11sbVOrKl+Np6gdPEcMkQJbZZv+ve5KCc4+7FChJzRr3D6p+8euRJa++TyNkYeT8Laiwd+R7VJ7JTvTv6wYnNclsfM8rYdMnpQ86bp6GXffLv+npp1SeJmPq1LMbG3j7BADDE/nUmM1MEaPmZ" 

gateway = "http://openapi.alipay.com/gateway.do?"
#gateway = "http://10.16.10.90/gateway.do?"

def payShowHelp():
    helpInfo = [
        "help                          show help info",
        "pay money tradeNo             make QRcode with money and tradeNo",
        "check tradeNo                 check tradeNo",
        "--------------------------------------------------------------------"]
    
    for info in helpInfo:
        print(info)
    return

def get_sig(content, privateKey):
    pkey = ct.load_privatekey(ct.FILETYPE_PEM, privateKey)
    if pkey:
        signature = ct.sign(pkey, content.encode('utf8'), 'sha256')
        ret = base64.encodebytes(signature)
        return ret.decode('utf8').replace('\n', '')
    return False

def mk_ali_qrcode(money, sn):
    json_dict = '{}'
    privkey2 = '-----BEGIN RSA PRIVATE KEY-----\n' + privkey + '\n-----END RSA PRIVATE KEY-----'
    parmeter1 = "app_id=" + app_id
    #biz_content = "{\"out_trade_no\":\"tradeprecreatedf8\",\"total_amount\":0.01,\"subject\":\"Pmxtst\"}"
    tradeSn = "\"trade" + sn + "\""
    biz_content = "{\"out_trade_no\":" + tradeSn + ",\"total_amount\":" + money + ",\"subject\":\"PmxBob\"}"
    #parmeter2 = "charset=utf-8&method=alipay.trade.precreate&sign_type=RSA2&timestamp=2021-01-12 14:30:00&version=1.0"
    parmeter20 = "charset=utf-8&method=alipay.trade.precreate&sign_type=RSA2&timestamp="
    timeStr = vos_getTimeStr()
    parmeter2 = parmeter20 + timeStr + "&version=1.0"
    #parmeter2 = parmeter20 + "2021-01-25 13:13:13" + "&version=1.0"

    sign_in = parmeter1 + '&biz_content=' + biz_content + '&' + parmeter2
    #sign_in = "app_id=2021002118605358&biz_content={\"out_trade_no\":\"tradeprecreatedf7\",\"total_amount\":0.01,\"subject\":\"Pmxtst\"}&charset=utf-8&method=alipay.trade.precreate&sign_type=RSA2&timestamp=2021-01-12 14:30:00&version=1.0"
    #sign_out = "QEuOXPpQH2uqsoThdBlzkiGWPlOH4gdgpeDDAmSSNJM2Wkb7BmgGzihJIaFPRjvm9/n8P2L/lMH6u6qwI6+Mwj9OA/sQTEbp7TG6QTwz5s2FoIFLmCjz8Qd3pvoq7/GfH+8zq+lZrWpTyQ+0vDEPtYf7M64X5+D/XhlkZi7U8Y3okRzqEBDR2s8SCmG1Wqn9UAA1ifUmLjNtFK50d7kZsCPWRrBc4M1EmyNFe3c9PufCcAdxcZ7jxiwVK/b9xFOvrT3lgm+hI0TPRPQBBgTfRLBw84iGUX0hXjRgwqsAOinhVOj409Wrkl9Q3QCiv1TYhE55Qitrw6y0PUhMI6ivvw=="
    sign_out = get_sig(sign_in, privkey2)

    biz_content2 = quote(biz_content) #quote(biz_content, 'utf-8')
    sign_out2 = quote(sign_out)

    url = gateway + parmeter1 + '&biz_content=' + biz_content2 + '&' + parmeter2 + '&sign=' + sign_out2    
    print(url)
    #requests.post(_url, data=_json_dict, headers=_headers, verify=False)/_resp = requests.get(_url, _json) _resp.content
    _resp = requests.post(url, json_dict, verify=False) 
    result = _resp.text
    result2 = eval(result) ##onvert str to dict
    result3 = result2["alipay_trade_precreate_response"]
    qrcode_str = result3["qr_code"]
    qrcode_str2 = qrcode_str.replace('\\', '')
    print(qrcode_str2)

    fileName = sn + ".png"
    img = qrcode.make(qrcode_str2)
    img.save(fileName)
    return

def ckeck_ali_trade(sn):
    json_dict = '{}'
    privkey2 = '-----BEGIN RSA PRIVATE KEY-----\n' + privkey + '\n-----END RSA PRIVATE KEY-----'
    parmeter1 = "app_id=" + app_id
    #biz_content = "{\"out_trade_no\":\"tradeprecreatedf8\",\"total_amount\":0.01,\"subject\":\"Pmxtst\"}"
    tradeSn = "\"trade" + sn + "\""
    biz_content = "{\"out_trade_no\":" + tradeSn + "}"
    parmeter20 = "charset=utf-8&method=alipay.trade.query&sign_type=RSA2&timestamp="
    timeStr = vos_getTimeStr()
    parmeter2 = parmeter20 + timeStr + "&version=1.0"

    sign_in = parmeter1 + '&biz_content=' + biz_content + '&' + parmeter2
    sign_out = get_sig(sign_in, privkey2)

    biz_content2 = quote(biz_content) #quote(biz_content, 'utf-8')
    sign_out2 = quote(sign_out)

    url = gateway + parmeter1 + '&biz_content=' + biz_content2 + '&' + parmeter2 + '&sign=' + sign_out2    
    #print(url)
    _resp = requests.post(url, json_dict, verify=False) 
    result = _resp.text
    result2 = eval(result) ##onvert str to dict
    query_response = result2["alipay_trade_query_response"]    

    tradeResult = {'trade_status':'no trade', 'phone number':'12345678', 'buyer_pay_amount':'0.00', }
    if(query_response["msg"] == 'Success'):
        tradeResult['trade_status'] = query_response["trade_status"]
        tradeResult['phone number'] = query_response["buyer_logon_id"]
        tradeResult['buyer_pay_amount'] = query_response["buyer_pay_amount"]
    return tradeResult

if __name__ == "__main__":
    print("Welcome to PMX alipay\r\n->")
    while True:
        inputCmd = input('->')
        inList = inputCmd.split(' ')
        
        if(inList[0] == 'help'):
            payShowHelp()
            print('->')
        elif(inList[0] == 'pay'):
            money = inList[1]
            name = "test"
            if(len(inList) > 2):
                name  = inList[2]
            mk_ali_qrcode(money, name)
            print("Qrcode file:",name, ".png")
            print('->')      
        elif(inList[0] == 'check'):
            name = "test"
            if(len(inList) > 1):
                name  = inList[1]
            ckeck_ali_trade(name)    
            print('->')
        elif(inList[0] == 'exit'):
            break
        else:
            print('->')





