#Those libraries work for the encryption and diencryption.
import base64
import os
from cryptography.fernet import Fernet #symetric encryption
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC #encryptor

class encryption_Handler:
    def __init__ (self,master_password, salt=None):
        """
        If the file has salt, it uses it, otherwise, a new one is created.
        """
        if salt:
            self.salt = salt
        else:
            self.salt = os.urandom(16)
            """
            This algorithm is a congfiguration for "PBKDF2HMAC" function that
            will create a secure key from your password, kdf(Key Derivation Function).
            """
        kdf = PBKDF2HMAC(
            algorithm = hashes.SHA256(),
            length = 32, #At least the algorithm need 32 bytes of length
            salt = self.salt, # The bytes for the encryptation.
            iterations = 480000 #Iterations times
        )
        """
        .encode(), is a function that transform str in bytes
        kdf.derive, is a function that we configurated, this the salt.
        base64.urlsafe_b64encode, is a function to traduce this bytes in characters.
        All is saved into de variable "Key"
        """
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        self.fernet = Fernet(key)
       
    #data will be the json archive where the data (password and user information) will be saved.
    def encrypt (self, json_str):
        
        #However encrypt only works with bytes, we transform data into bytes.
        data_in_bytes = json_str.encode ('utf-8')
        
        #Encrypt data with the fernet key (Derivate of Master Password) that we created in the constructor.
        encrypted_data = self.fernet.encrypt(data_in_bytes)
        return encrypted_data
    
    def decrypt(self, encrypted_data):
        
        #We receive the data encrypted so we use the fernet_key to dencrypt data.
        decrypted_bytes = self.fernet.decrypt(encrypted_data)
        
        #transform the dencrypted bytes into the real data by using decode method.
        bytes_in_data = decrypted_bytes.decode('utf-8')
        return bytes_in_data

    def get_salt(self):
        """
        The salt has to be saved to decrypt the file, decrypt read the first 16 bytes to get
        the salt and use it.
        """
        return self.salt
        
        
        
        
        
        