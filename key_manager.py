import keyring

class KeyManager:
    def __init__(self):
        self.api_service_name = "ShodanAPI"
        self.user = "user"

    def get_api_key(self):
        return keyring.get_password(self.api_service_name, self.user)
    
    def set_api_key(self, api_key):
        keyring.set_password(self.api_service_name, self.user, api_key)
