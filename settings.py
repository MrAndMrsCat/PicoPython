class Settings(object):
    """Persistant settins"""

    SETTINGS_PATH = "/settings.cfg"

    # singleton
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls.load(cls)
        return cls._instance


    def load(self):
        self.items = {}
        try:
            print(f"open({self.SETTINGS_PATH})")
            with open(self.SETTINGS_PATH, mode="r") as f:
                for full_line in f.readlines():
                    line = full_line.strip()
                    print(line)
                    kv = line.split(':')
                    self.items[kv[0]] = kv[1]

        except OSError as os_ex:
            print(os_ex)
        except Exception as ex:
            print(ex)        


    def save(self):
        try:
            with open(self.SETTINGS_PATH, mode="w") as f:
                for key, value in self.items.items():
                    f.write(f"{key}:{value}\n")

        except OSError as os_ex:
            print(os_ex)
        except Exception as ex:
            print(ex)
            
    def get(self, key: str):
        return self.items.get(key)
    
    
    def get_bool(self, key: str):
        return self.get(key) == "True"
    
    
    def set(self, key: str, value):
        self.items[key] = value
        self.save()
