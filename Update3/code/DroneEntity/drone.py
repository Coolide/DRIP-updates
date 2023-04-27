import rsa
from os.path import exists
import hmac
import hashlib
import requests
import psutil

URL = 'http://127.0.0.1:8000' #server address

#Drone config info
UAS_ID = 0000
serial_num = 'test'
entity_ID = 0000
registry_ID = 0000
operator_name = 'test'
emergency_num = 0000
date_of_birth = 0000

#Loads information before drone operation
def initialise():
    #Create the key pair
    if not exists('./public.pem') and not exists('./private.pem'):
        public_key, private_key = rsa.newkeys(2048)
        print('Created new public and private keys...')
        with open('public.pem', 'wb') as file:
            file.write(public_key.save_pkcs1('PEM'))

        with open('private.pem', 'wb') as file:
            file.write(private_key.save_pkcs1('PEM'))
    #Register information to the server and certificate authority
    result = requests.get('{}/register-entity/{}/{}'.format(URL,'drone',get_mac_address()))
    #Add private information
    result = requests.get('{}/add-private-info/{}/{}/{}/{}'.format(URL,UAS_ID,entity_ID,registry_ID,serial_num))
    #Add public information
    result = requests.get('{}/add-public-info/{}/{}/{}/{}'.format(URL,UAS_ID,operator_name,emergency_num,date_of_birth))
    #Add certificate to server
    with open('public.pem', 'rb') as p:
        public_key = rsa.PublicKey.load_pkcs1(p.read())
        result = requests.get('{}/add-certifcate/{}/{}'.format(URL,public_key,get_mac_address()))
        print(result)

#Encrypts the plain text into cipher text using the public key into utf-8
def encrpyt(message):
    with open('public.pem', 'rb') as p_file:
        public_key = rsa.PublicKey.load_pkcs1(p_file.read())
    encryptped_message = rsa.encrypt(message.encode(), public_key)
    return encryptped_message

#Decrypts a message using the private key into utf-8
def decrypt(message):
    with open('private.pem', 'rb') as p_file:
        private_key = rsa.PrivateKey.load_pkcs1(p_file.read())
    decrypted_message = rsa.decrypt(message, private_key)
    return decrypted_message

#Creates the hashed message using a message authentication code (MAC)
def hash(session_key, message):
    session_key = session_key.encode()
    message = message.encode()
    hashed_message = hmac.new(session_key, message, hashlib.sha256)    
    return hashed_message.hexdigest()

#Gets the WiFi mac address of the device
def get_mac_address():
    mac_address = psutil.net_if_addrs()['WiFi'][0].address
    return mac_address

def send_message():
    return

def find_observers():
    return

def get_observer_public_key():
    return

def get_flight_session():
    return

def run():
    locked = encrpyt(hash('flight-001', 'hello :)'))
    print(decrypt(locked).decode())


if __name__ == '__main__':
    initialise()
    run()