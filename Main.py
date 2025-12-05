from Credentials import credential
from PasswordGenerator import password_generator_simple, password_generator_complex
from EncryptionHandler import encryption_Handler
from VaultHandler import vault_handler
import os

def main():
    
    while True:
        Menu()
        opcion = int(input ("Chose: "))
        match opcion:
            case 1:
                print("-----Create an entry-----")
                Complete_list = Create_an_entry()
            case 2:
                print("-----Save and encrypt-----")
                Save_and_encrypt(Complete_list)
                print ("El archivo se guardó en:", os.path.abspath("My_data"))
            case 3:
                print("-----Decrypt and show-----")
                decrypt_and_show()
            case 4:
                break


def Menu():
    print("Chose the operation you wish to perform")#Show the Menu
    print ("""
-------Menu-------
1.Create an entry.
2.Save and encrypt.
3.Decyrpt and load.
4.Exit
------------------""")
    
def Create_an_entry():
    list_of_entrys = []
    while True:
        print("----- Menu -----")
        print("1. Add new entry")
        print("2. Save and leave")
        opcion = input("Chose: ")
        
        if opcion == "1":
            print("-----Create a new Entry-----")
            user_name = input ("What is the user name: ")
            app_site = input ("what is the app or site: ")
            ID = input ("Press enter to create an ID: ")
            
            #Create the credential object
            entry = credential(user_name, app_site,entry_id=None)
            entry_dict = entry.to_dict()
            
            #chose simple password or complex
            print("-------------------------Create a Password-------------------------")
            print("Press 's' to create a simple password(only numbers and lyrics).")
            print("Press 'c' to create a complex password (numbers, lyrics and symbols).")    
            password_type = input("Chose: ").lower()
            
            #For simple password
            if password_type == "s":
                while True:
                    try:
                        print ("-----------Genereate a simple password----------")
                        print ("Lenght of yor password (at leats 8 characters).")
                        length = int(input("Length: "))
                        simple_password = password_generator_simple(length)
                        if simple_password.validate_security(length) == False:
                            print("Try again with a longer password.")
                            continue
                        else:
                            simple_password_value = simple_password.generate()
                            print(f"Password saved as {simple_password_value}")
                            entry.add_password(simple_password_value,entry_dict)
                            list_of_entrys.append(entry_dict)
                            break
                    except ValueError:
                        print("Error, you should write a number")
            #For complex password
            elif password_type == "c":
                while True:
                    try:
                        print ("--------Genereate a complex password--------")
                        print ("Lenght of yor password (at leats 8 characters).")
                        length = int(input("Length: "))
                        complex_password = password_generator_complex(length)
                        if complex_password.validate_security(length) == False:
                            print("Try again with a longer password.")
                            continue
                        else:
                            complex_password_value = complex_password.generate()
                            print(f"Password saved as: {complex_password_value}")
                            entry.add_password(complex_password_value,entry_dict)
                            entry.add_password(complex_password_value,entry_dict)
                            list_of_entrys.append(entry_dict)
                            break
                    except ValueError:
                        print("Error, you should write a number.")
        elif opcion == "2":
            if len (list_of_entrys) == 0:
                print("The list is empty...")
            else:  
                return list_of_entrys

def Save_and_encrypt(list_of_entrys):
    #Create a Master password
    print("Is the moment to create a master password, write and save it")
    master_password = input("Master password: ")
    """
    If the fil is empty "save encrypted data" will just write,
    but if the file has infromation then we load that information first,
    this way that information is not lost.
    """
    vault = vault_handler("My_data2.0")
    recovered_list = vault.load_json(master_password)
    if recovered_list:
        print(f"{len(recovered_list)} has been recovered.")
    else:
        print("New file or no data has found")
    combined_list = recovered_list + list_of_entrys
    
    #create The json file with the data in list  of entrys.
    file_with_data = vault_handler("My_data2.0")
    json_file = file_with_data.create_json(combined_list)
    
    #Encrypt the json file.
    encryptor = encryption_Handler(master_password)
    salt_used = encryptor.get_salt()
    encrypted_file = encryptor.encrypt(json_file)
    
    #Save the encrypted file
    file_with_data.save_encrypted_data(salt_used,encrypted_file)
    
def decrypt_and_show():
    # Ask for the master password
    master_password = input("Master password: ")
    vault = vault_handler("My_data2.0")
    # craate encryptor object to decrypt
    recovered_list = vault.load_json(master_password)
    
    if not recovered_list:
        print("The file was not found or the password is incorrect")
    else:
        print(f"¡Succes opeartion,{len(recovered_list)} entrys has found.")
        for entry in recovered_list:
            print(entry)
      
if __name__ == "__main__":
    main()
    