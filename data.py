import json
import os

class Data:
    fname= "data/data.txt"

    @classmethod
    def _load(cls):
        if(not os.path.exists(cls.fname)):
            with open(cls.fname, "w+") as data_file:
                json.dump({}, data_file) #create data file if none exists

        with open(cls.fname) as data_file:
            cls._data: dict = json.load(data_file)
             
    @classmethod
    def _save(cls):
        with open(cls.fname, "w") as data_file:
            json.dump(cls._data, data_file)
    
    @classmethod
    def get(cls, key, default = None):
        return cls._data.get(key, default)
    
    @classmethod
    def set(cls, key, value):
        cls._data[key]= value
        cls._save()

Data._load()