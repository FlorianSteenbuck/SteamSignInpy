#!/usr/bin/env python
from SteamSignIn import SteamSignIn

SteamSignIn = SteamSignIn('127.0.0.1')
host = SteamSignIn.create_socket()
print("Host: "+host[0])
print("Port: "+str(host[1]))
print("IPv6: "+str(host[2]))
print(SteamSignIn.steamlogin+"?openid.ns=http://specs.openid.net/auth/2.0&openid.mode=checkid_setup&openid.return_to=http://127.0.0.1:"+str(host[1])+"&openid.realm=http://127.0.0.1:"+str(host[1])+"&openid.identity=http://specs.openid.net/auth/2.0/identifier_select&openid.claimed_id=http://specs.openid.net/auth/2.0/identifier_select")
print(SteamSignIn.validate(SteamSignIn.startserver()))