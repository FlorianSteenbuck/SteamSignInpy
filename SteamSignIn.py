#!/usr/bin/env python
from urllib import parse
import requests
import socket

class SteamSignIn(object):
	__steamlogin = "https://steamcommunity.com/openid/login"
	@property
	def steamlogin(self):
		return self.__steamlogin
	__clientip = None
	__ipv6 = False
	__host_addr = ''
	__port_addr = 0
	__socket = None
	__res_args = None
	def __init__(self,clientip=None):
		if self.is_valid_ipv4_address(clientip):
			self.__clientip = clientip
		else:
			if self.is_valid_ipv6_address(clientip):
				self.__clientip = clientip
				self.__ipv6 = True
			else:
				raise Exception("No valid ipv6 or ipv4 address")
	def create_socket(self):
		self.__host_addr = '0.0.0.0'
		if self.__ipv6:
			self.__host_addr = '::'
		self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if self.__ipv6:
			self.__socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
		self.__socket.bind((self.__host_addr,self.__port_addr))
		return (self.__host_addr,self.__socket.getsockname()[1],self.__ipv6)
	def startserver(self):
		data = ''
		header = 'HTTP/1.1 200 OK\r\nServer: Fl0XeN Log1n\r\nContent-Type: text/html\r\nEncoding: utf-8\r\n'
		self.__socket.listen(1)
		while 1:
			conn, addr = self.__socket.accept()
			if addr[0] == self.__clientip:
				data = self.fgets(conn).split(" ")[1]
				back = open("conf/SteamSignIn/ok.html").read()
				conn.send(bytes(header+'Content-Length: '+str(len(back))+'\r\n\r\n'+back,'utf-8'))
				conn.close()
				break
			else:
				back = open("conf/SteamSignIn/wrongip.html").read()
				conn.send(bytes(header+'Content-Length: '+str(len(back))+'\r\n\r\n'+back,'utf-8'))
				conn.close()
		self.__socket.close()
		data = data.split("?")[len(data.split("?"))-1]
		return self.urlparamtodic(data)
	def urlparamtodic(self,data):
		dic = {}
		args = data.split('&')
		for arg in args:
			keyval = arg.split('=')
			dic[parse.unquote_plus(keyval[0])] = parse.unquote_plus(keyval[1])
		return dic
	def validate(self,dic):
		params = {}

		openid_endpoint = dic["openid.op_endpoint"]
		signed = dic["openid.signed"].split(",")
		for item in signed:
			params["openid."+item] = parse.quote_plus(dic["openid."+item])
		params['openid.mode'] = 'check_authentication'

		params["openid.assoc_handle"] = dic['openid.assoc_handle'] 
		params["openid.signed"] = dic['openid.signed']
		params["openid.sig"] = parse.quote_plus(dic['openid.sig'])
		params["openid.ns"] = 'http://specs.openid.net/auth/2.0'

		data = "?"
		for key, value in params.items():
			data += key+"="+value+"&"
		data = data[:-1]
		print("https://steamcommunity.com/openid/login"+data)
		check = requests.get("https://steamcommunity.com/openid/login"+data)
		check = str(check.content)
		if check.split("\\n")[1] == "is_valid:true":
			return dic["openid.claimed_id"]
		else:
			return False
	def is_valid_ipv4_address(self,address):
		try:
			socket.inet_pton(socket.AF_INET, address)
		except AttributeError:
			try:
				socket.inet_aton(address)
			except socket.error:
				return False
			return address.count('.') == 3
		except socket.error:
			return False

		return True
	def is_valid_ipv6_address(self,address):
		try:
			socket.inet_pton(socket.AF_INET6, address)
		except socket.error:
			return False
		return True
	def fgets(self,socket,recv_bytes=1,deml='\n'):
		data = ''
		while 1:
			data += socket.recv(recv_bytes).decode('utf-8')
			if deml in data:
				lines = data.split(deml)
				data = lines[0]
				break
		return data