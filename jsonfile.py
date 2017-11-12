import json,os
class jsonFile:
    _filePath = ""
    _vaulesKey = "_values"
    _exists = False
    _data = {}

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

    def set(self,key=False,value=False,section=False,base=False):
        """
        Store data in the tree json object, where the data is stored will depend on some factors

        :param key: string | bool, the key string for the dictionary, if not defined or False passed an auto index will be created
        :param value: value to be stored
        :param section: bool | string | list pass a string or a list to define the section (sub section) to store the data
         i.e ["level1","level2"] will create { "level1": {"level2":{"key:"value" } } }
         if no section is defined or passed as False, key-value will go to root level i.e: {"key":"value"}
        :param base:  used in the recusrive function
        :return:
        """
        if value is False:
            return False

        if section is False:
            if key is not False and value is not False:
                self._data[key]=value
        else:
            if key is False:
                print "keyFalse"
            elif key is not False:
                if isinstance(section, list):
                    if base is False:
                        # avoid recursively creating sections on each recurse iteration
                        self.createSection(section=section)
                        base = self._data

                    if len(section) == 1:
                        base[section[0]][key] = value
                    elif len(section) > 1:
                        sectionID = section[0]
                        secttionCopy = list(section)
                        secttionCopy.pop(0)
                        self.set(key=key,value=value,section=secttionCopy, base=base[sectionID])

                else:
                    self._data[section][key] = value
                return
            # if key is False:
            #
            #
            #
            #     if self._data.get(section) is None:
            #         self._data[section] = []
            #     # section not false but key false
            #     if value is not False:
            #
            #         for x in self._data[section]:
            #             if x["path"] == value:
            #
            #                 return
            #
            #         self._data[section].append(value)
            # # else:

    def remove(self,key=False,section=False,base=False):
        if key is False:
            return False

        if section is False:
            if key is not False and key in self._data:
                self._data.pop(key)
        else:
            if isinstance(section, list):
                if base is False:
                    base = self._data

                if len(section) == 1 and key in base[section[0]]:
                    base[section[0]].pop(key)
                elif len(section) > 1:
                    sectionID = section[0]
                    secttionCopy = list(section)
                    secttionCopy.pop(0)
                    self.remove(key=key, section=secttionCopy, base=base[sectionID])

    def createSection(self,section,base=False):

        if isinstance(section, list):

            if base is False:
                base = self._data

            if section[0] not in base:
                base[section[0]] = {}

            if len(section) > 1:
                sectionID=section[0]
                secttionCopy = list(section)
                secttionCopy.pop(0)

                self.createSection(secttionCopy,base=base[sectionID])
        else:
            self._data[section]={}


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





    def getValueIn(self, key, value, section=False):
        """
         This function will search for a value in an key:value object and return the object on the first mach,
         or False if not found
         obj = [ {key:val, otherkey:val2 },{ key:val4, otherkey:val3 } ]
        """
        found = False
        obj = self.get(section=section)
        for x in obj:
            if x[key] == value:
                found = x
                break
        return found
