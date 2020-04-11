# -*- coding: utf-8 -*-
"""
   SteamReedem 0.1
   by Sinf0r0s0 07/jan/2020
   python3.6

"""
import pickle
from base64 import b64encode
from time import time
from os import urandom as random_bytes
from binascii import hexlify
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Hash import SHA1
from Crypto.PublicKey.RSA import construct as rsa_construct
import requests
from steamreedem import stmmsg as m


class Steamreedem(object):
    URL_GET_RSA = 'https://steamcommunity.com/login/getrsakey/'
    URL_LOGIN = 'https://steamcommunity.com/login/dologin/'
    URL_REG_KEY = 'https://store.steampowered.com/account/ajaxregisterkey/'

    def __init__(self, username, password, max_retry=3):
        self.username = username
        self.password = password
        self.ml = 0
        self.mr = 0
        self.is_logged = False
        self.max_retry = max_retry
        self.s = requests.Session()
        self.err_req = requests.exceptions.RequestException

    def login(self):
        try:
            resp = self.s.post(self.URL_GET_RSA, timeout=15, data={'username': self.username,
                                                                   'donotchache': int(time() * 1000)}).json()
            key_e = rsa_construct((int(resp['publickey_mod'], 16),
                                   int(resp['publickey_exp'], 16),
                                   ))
            kout = b64encode(PKCS1_v1_5.new(key_e).encrypt(self.password.encode('ascii')))
            timestamp = resp['timestamp']
            data = {
                'username': self.username,
                "password": kout,
                "rsatimestamp": timestamp,
            }
            resp = self.s.post(self.URL_LOGIN, data=data, timeout=10).json()['success']
            # print(resp)
            if resp:
                self.is_logged = True
                with open('cookie.session', 'wb') as fb:
                    pickle.dump(self.s.cookies, fb)
            return resp
        except self.err_req as e0:
            print(f'Error N0 ao obter rsa key ou ao Logar: {e0}')
            return False

    def reedem(self, key):
        if not self.has_cookie():
            print(' :( logging in...')
            self._re_login(self.max_retry)
        session_id = hexlify(SHA1.new(random_bytes(32)).digest())[:32].decode('ascii')
        try:
            ck = {
                'sessionid': session_id,
                'steamLoginSecure': self.s.cookies['steamLoginSecure'],
            }
            is_logged = self.s.get('https://store.steampowered.com/account/', cookies=ck)
            if is_logged.history:
                print('nao logado :( possibly expired cookies, logging in ... ')
                self._re_login(self.max_retry)
                self._re_reedem(key, self.max_retry)
            else:
                print('...Logged :)')
                self.is_logged = True
                blob = self.s.post(self.URL_REG_KEY, cookies=ck, data={'product_key': key, 'sessionid': session_id},
                                   timeout=10)
                if blob.history:
                    print(
                        'Error N3 redirected to login page, cookies not loaded correctly, trying to ...')
                    self._re_reedem(key, self.max_retry)
                else:
                    js = blob.json()
                    if js["success"] == 1:
                        for item in js["purchase_receipt_info"]["line_items"]:
                            print(f'[ Redeemed!!! ] {item["line_item_description"]}')
                    else:
                        error_code = js["purchase_result_details"]
                        if error_code == 14:
                            s_error_message = m.mesg14
                        elif error_code == 15:
                            s_error_message = m.msg15
                        elif error_code == 53:
                            s_error_message = m.mesg53
                        elif error_code == 13:
                            s_error_message = m.mesg13
                        elif error_code == 9:
                            s_error_message = m.mesg9
                        elif error_code == 24:
                            s_error_message = m.mesg24
                        elif error_code == 36:
                            s_error_message = m.mesg36
                        elif error_code == 50:
                            s_error_message = m.mesg50
                        else:
                            s_error_message = m.mesg00
                        print(f'[ Error ] {s_error_message}')
        except Exception as e1:
            print(f'Error when redeeming, invalid username or password: {e1}')

    def has_cookie(self):
        try:
            with open('cookie.session', 'rb') as f:
                self.s.cookies.update(pickle.load(f))
        except (FileNotFoundError, pickle.UnpicklingError):
            return False
        return True

    def _re_login(self, max_r):
        while self.ml < max_r:
            self.ml += 1
            return self.login()

    def _re_reedem(self, key_r, max_r):
        while self.mr < max_r:
            self.mr += 1
            if self.is_logged:
                return self.reedem(key_r)
            else:
                print('Erro N5: Error when trying to redeem the key using cookies')
