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
                self._setValue(base,key,value,indexed,id)
                # base[key] = value
        elif isinstance(key, list):

            if len(key) == 1:
                if value is None:
                    base[key[0]] = {}
                else:
                    self._setValue(base, key[0], value, indexed,id)
            elif len(key) > 1:
                sectionID = key[0]
                secttionCopy = list(key)
                secttionCopy.pop(0)

                if sectionID not in base:
                    base[sectionID] = {}

                self.set(key=secttionCopy, value=value, base=base[sectionID])


    def _setValue(self, base, key, value,indexed=False,id=False):
        """
        private method to save the value, will do different if indexed = True
        :param base:
        :param key:
        :param value:
        :param indexed:
        :return:
        """
        if indexed is False:
            base[key]=value
        else:
            topIndex = self._getTopIndex(base[key])
            index = self._indexPrefix + str(topIndex + 1)
            if id is False:
                id = index
            item = {
                "index":index,
                "id":id,
                "value": value
            }

            base[key][index] = item




    def _getTopIndex(self,data):
        index = 0
        n = len(self._indexPrefix)

        for key, val in data.items():
            indexString = key[:n]
            if indexString == self._indexPrefix:
                tindex = int(key[n:])
                if tindex > index:
                    index = tindex
        return index



    def setMulti(self,key=False,value=None,id=False,base=False,indexed=False):
        """
        Call the set method with indexed = true
        :param key:
        :param value:
        :param base:
        :param indexed:
        :return:
        """
        self.set(key=key,value=value,indexed=True,id=id)



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

                if len(key) > 1:
                    sectionID = key[0]
                    secttionCopy = list(key)
                    secttionCopy.pop(0)
                    return self.remove(key=secttionCopy, base=base[sectionID])
                else:
                    base.pop(key[0])
                    return True


    def get(self, key=False, base=False):
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
                    return False

            elif isinstance(key, list):
                if base is False:
                    base = self._data

                if key[0] not in base:
                    return False

                if len(key) > 1:
                    sectionID = key[0]
                    secttionCopy = list(key)
                    secttionCopy.pop(0)
                    return self.get(key=secttionCopy, base=base[sectionID])
                else:
                    return base[key[0]]

        else:
            return self._data


    def getValueIn(self, key, value):
        """
         This function will search for a value in an key:value object and return the object on the first mach,
         or False if not found
         obj = [ {key:val, otherkey:val2 },{ key:val4, otherkey:val3 } ]
        """
        found = False
        obj = self.get(key = key)
        print obj
        return
        for x in obj:
            if x[key] == value:
                found = x
                break
        return found
