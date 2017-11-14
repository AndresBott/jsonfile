import json,os
class jsonFile:
    _filePath = ""
    _vaulesKey = "_values"
    _exists = False
    _data = {}
    _indexPrefix = "_i"

    def __init__(self, s):
        """
        Constructor
        :param s: absolute path to configuration file
        """
        self.setfilePath(s)

    def setfilePath(self, s):
        """
        Set the absolute path to configuration file
        :param s: path
        """
        self._filePath = s
        if os.path.isfile(s):
            self._exists = True
        else:
            self._exists = False

    def fileExists(self):
        """
        check if the json file exists
        :return: True | False
        """
        return self._exists

    def write(self):
        """
        write the json object to file
        :return:
        """
        with open(self._filePath, "w") as outfile:
            json.dump(self._data, outfile, indent=4)

    def safe(self):
        """
        Alias to write
        :return:
        """
        self.write()

    def load(self):
        """
        load a json file into the object
        :return:
        """
        if self.fileExists():
            with open(self._filePath) as data_file:
                self._data = json.load(data_file)

    def set(self,key=False,value=None,base=False,indexed=False,id=False):
        """
        Store data in the tree json object, where the data is stored will depend on some factors

        :param key: string | bool, the key string for the dictionary, if not defined or False passed an auto index will be created
        :param value: value to be stored, if not defined an empty object will be created
        :param section: bool | string | list pass a string or a list to define the section (sub section) to store the data
         i.e ["level1","level2"] will create { "level1": {"level2":{"key:"value" } } }
         if no section is defined or passed as False, key-value will go to root level i.e: {"key":"value"}
        :param base:  used in the recusrive function
        :return:
        """
        if key is False:
            return False

        if base is False:
            base = self._data

        if isinstance(key, basestring):
            if key not in base:
                base[key] = {}

            if value is None:
                base[key] = {}
            else:
                base[key] = value
        elif isinstance(key, list):

            if len(key) == 1:
                if value is None:
                    base[key[0]] = {}
                else:
                    base[key[0]] = value
            elif len(key) > 1:
                sectionID = key[0]
                secttionCopy = list(key)
                secttionCopy.pop(0)

                if sectionID not in base:
                    base[sectionID] = {}

                self.set(key=secttionCopy, value=value, base=base[sectionID])


    def remove(self,key=False,base=False):
        """
        Remove a key or section from the tree
        :param key:
        :param base:
        :return:
        """
        if key is False:
            return False
        else:
            if isinstance(key, basestring):
                if key in self._data:
                    self._data.pop(key)
                    return True
                else:
                    return False

            elif isinstance(key, list):
                if base is False:
                    base = self._data

                if key[0] not in base:
                    return False

                if len(key)== 1:
                    base.pop(key[0])
                    return True

                elif len(key) > 1:
                    sectionID = key[0]
                    secttionCopy = list(key)
                    secttionCopy.pop(0)
                    return self.remove(key=secttionCopy, base=base[sectionID])




    def get(self, key=False,defaultReturn=False, base=False):
        # type: (object, object) -> object
        """
        Get the value or part of the json tree of a section in the json
        :param key: (bool)False | string | list
         if False return the whole json
         if a string return the level 1 value of that key
         if a list go down the tree and return the last element in the list
        :param base:
        :return:
        """

        if key is not False:
            if isinstance(key, basestring):
                if key in self._data:
                    return self._data[key]
                else:
                    return defaultReturn

            elif isinstance(key, list):
                if base is False:
                    base = self._data

                if key[0] not in base:
                    return defaultReturn

                if len(key) > 1:
                    sectionID = key[0]
                    secttionCopy = list(key)
                    secttionCopy.pop(0)
                    return self.get(key=secttionCopy, base=base[sectionID])
                else:
                    return base[key[0]]

        else:
            return self._data


