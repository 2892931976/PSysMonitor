#!/usr/bin/env python
#encoding=utf-8
"""
 tonggao sdk
 User: liurongcheng
 Date: 14-8-14
 Time: 下午5:55
 email:liurongcheng@baidu.com
"""
import urllib2
import json

class TonggaoIncident(object):
    """baidu tonggao incident interface sdk class;
    you will be provide with the service id and token,
    and when you send the request to tonggao web,you must provide with them"""
    __hostname = "http://tonggao.baidu.com"
    __url = "/event/create"
    __event_type =  "trigger"
    __incident_id = None

    def __init__(self, service_id, service_key):
        """constructor of TonggaoIncident"""
        if service_id is None or service_key is None:
            raise Exception("service id and service key must be provider")
        self.__service_id = service_id
        self.__service_key = service_key

    def __post(self, uri, headers, params):
        """send post request with the uri,headers and params """
        params_json = json.dumps(params)
        req = urllib2.Request(uri, data=params_json, headers=headers)
        resp = urllib2.urlopen(req, timeout=1)
        return resp.read()

    def __send_request(self, uri, request_headers, params):
        """send  post  request  and return the answer of  dispose_response function"""
        response = self.__post(uri, request_headers, params)
        return self.__dispose_response(response)

    def __dispose_response(self, response):
        """dispose the response from the http request to bellringer web"""
        data = json.loads(response)
        if data['status'] is False:
            raise Exception(data['message'])
        else:
            return True

    def triggerIncident(self, description):
        """ trigger one incident without  incident id"""
        return self.__trigger_incident_with_id(description, None)

    def __trigger_incident_with_id(self, description, incident_id):
        """ trigger one incident with  incident id"""
        if description is None or description is "":
            raise Exception("description of incident can not  be null")
        if incident_id is not None:
            if type(incident_id) is not int:
                raise Exception("incident_id  must be  interge");
            self.__incident_id = incident_id

        params = {
            "service_id": self.__service_id,
            "event_type": self.__event_type,
            "description": description
        }
        if self.__incident_id is not None:
            params["incident_id"] = self.__incident_id

        headers = {
            "servicekey": self.__service_key
        }
        return self.__send_request(self.__hostname + self.__url, headers, params)


class TonggaoNotice(object):
    """baidu tonggao notice interface sdk class;
    you will be provide with the app id and token,
    and when you send the request to tonggao notice web,you must provide with them"""
    __hostname = "http://tonggao.baidu.com"
    __TONGGAO_NOTICE_URL = "/AlertList/push"
    __TONGGAO_SEND_PHONE = "phone"
    __TONGGAO_SEND_EMAIL = "email"
    __TONGGAO_SEND_SMS = "sms"
    __NOT_SET_TONGGEO_TRIGGER_INCIDENT_MESSAGE = "send_type and  receiver_list  must be provider"
    __NOT_SET_APP_NAME_OR_APP_TOKEN = "both app_name and app_token must be provider"
    __RECEIVER_FORMAT_NOT_RIGHT = "receiver format is error"
    __NOT_SET_RECEIVER = "receiver must not be None or ''"
    __NOT_DESCRIPTION_ON_SMS = "description must be provider on sms"
    __NOT_DESCRIPTION_ON_EMAIL = "description must be provider on email"
    __url = __TONGGAO_NOTICE_URL
    __username = None
    def __init__(self, app_id, app_token):
        """constructor of TonggaoNotice"""
        if app_id is None or app_token is None:
            raise Exception(self.__NOT_SET_APP_NAME_OR_APP_TOKEN)
        self.__app_id = app_id
        self.__app_token = app_token

    def __md5_string(self,to_be_md5):
        """use hashlib md5 the given string"""
        import hashlib
        my_md5 = hashlib.md5()
        my_md5.update(to_be_md5)
        my_md5_digest = my_md5.hexdigest()
        return my_md5_digest

    def __dispose_notice_response(self, response):
        """dispose the response from the http request to sendman web"""
        data = json.loads(response)
        if data['return'] is False:
            raise Exception(data['message'])
        else:
            return response

    def __post(self, uri, headers, params):
        """send  post  request  with the uri 、headers and params """
        params_json = json.dumps(params)
        req = urllib2.Request(uri, data=params_json, headers=headers)
        resp = urllib2.urlopen(req)
        return resp.read()

    def sendMessage(self, send_type, receiver_list, description=None, title=None):
        """send notice to receiver_list"""
        if not self.__validation_params(send_type, receiver_list, description):
            return
        notice_list = []
        if type(receiver_list) is list:
            for receiver in receiver_list:
                notice = {}
                notice['channel'] = send_type
                notice['receiver'] = receiver
                notice['description'] = description
                if title is not None:
                    notice['title'] = title
                notice_list.append(notice)
        elif type(receiver_list) is str:
            if receiver_list == "":
                raise Exception(self.__NOT_SET_RECEIVER)
            list1 = receiver_list.split(';')
            for receiver in list1:
                notice = {}
                notice['channel'] = send_type
                notice['receiver'] = receiver
                notice['description'] = description
                if title is not None:
                    notice['title'] = title
                notice_list.append(notice)
        else:
            raise Exception(self.__RECEIVER_FORMAT_NOT_RIGHT)
        headers = {
            'token': self.__app_token,
            'appid': self.__app_id,
            'signature': self.__md5_string(self.__app_token + self.__app_id + json.dumps(notice_list))
        }
        if self.__username is not None:
            headers['userid'] = self.__username
        response = self.__post(self.__hostname + self.__url, headers, notice_list)
        return self.__dispose_notice_response(response)

    def __validation_params(self, send_type, receivers, description):
        """ validation thr given params"""
        if send_type is None or receivers is None:
            raise Exception(self.__NOT_SET_TONGGEO_TRIGGER_INCIDENT_MESSAGE)
        send_type1 = send_type.lower()
        if cmp(send_type1, self.__TONGGAO_SEND_PHONE) == 0:
            return True
        if cmp(send_type1, self.__TONGGAO_SEND_SMS) == 0:
            if description is None or description == "":
                raise Exception(self.__NOT_DESCRIPTION_ON_SMS)
            return True
        if cmp(send_type1, self.__TONGGAO_SEND_EMAIL) == 0:
            if description is None or description == "":
                raise Exception(self.__NOT_DESCRIPTION_ON_EMAIL)
            return True
        raise Exception("send type " + send_type + " is illegal")
