import json
from EncryptionHandler import encryption_Handler 
class vault_handler:
    def __init__(self,archive):
        self.archive = archive
    
    def create_json(self,list_of_entrys):
        #Create a list with every credential
         data_to_save = list_of_entrys
         #Transform that list into a json_str which is a txt archive.
         json_str = json.dumps(data_to_save)
         return json_str
     
    def save_encrypted_data(self,salt_used,encrypted_data):
        
        """
        Save the encrypted bytes in the disc of the computer,
        use "with" to make sure that once the operation has been
        performed, finish every process
        """
        with open(self.archive,"wb") as f:
            f.write(salt_used)#First save the salt at the begining of the file
            f.write (encrypted_data)#Then save encrypted data
    

    def load_json(self,master_password):
        try:
            """
            Using "with" for caution, open the encrypted file.
            recovered the salt in the first 16 bytes and then read the file
            """
            with open(self.archive, "rb") as f:
                salt_from_file = f.read(16)
                load_json_encrypted_bytes = f.read()
            #Use de object to decrypt the file
            temp_encryptor = encryption_Handler(master_password, salt=salt_from_file)
            decrypted_str = temp_encryptor.decrypt(load_json_encrypted_bytes)
            return json.loads(decrypted_str)
        except FileNotFoundError:
            # Si no hay archivo, devolvemos lista vacía
            return []
        except Exception as e:
            print(f"Error al desencriptar: {e}")
            return []
         