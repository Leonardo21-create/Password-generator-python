#librery to generate unique IDs
import secrets
class credential:
    def __init__ (self, user_name, app_site, entry_id=None, password_value=None):
        self.user_name = user_name
        self.app_site = app_site
        
        #Logic to generate a new ID or use one that has already created.
        if entry_id is None:
            self.entry_id = str(secrets.randbelow(1000)) 
        else:
            self.entry_id = entry_id
            
    def to_dict (self):
           entry_dict = {
               "User name" : self.user_name,
               "app or site" : self.app_site,
               "Entry Id" : self.entry_id  ,
           }
           return entry_dict
           
    def add_password(self,password_value, entry_dict):
        password_dict = {
            "password": password_value
        }
        entry_dict.update(password_dict)
        return entry_dict
        