from abc import ABC, abstractmethod
import secrets
import string

class password_generator(ABC):
    def __init__(self, length):
        self.length = length
                   
    @abstractmethod
    def generate(self):
        pass
    
    
    def validate_security(self, length):
        if length < 8:
            print("Error: the password is too short (at leats 8 characters).")
            return False
            
        elif 8 <= length < 12:
            print("Perfect password")
            return True # Aceptamos, pero avisamos
            
        else: # Mayor o igual a 12
            return True
        
 
class password_generator_simple (password_generator):
    def generate(self):
        characters = string.ascii_letters + string.digits
        password_value_simple = "".join(secrets.choice(characters) for _ in range (self.length))
        return password_value_simple

class password_generator_complex (password_generator):
    def generate(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        password_value_complex = "".join(secrets.choice(characters) for _ in range (self.length))
        return password_value_complex