from __future__ import unicode_literals

import configparser

class CustomConfigParser(configparser.ConfigParser):

    def __init__(self):
        configparser.ConfigParser.__init__(self)
        self.optionxform = str

    def write(self, fp):
        """ Identical to the original method, but delimit keys and values with '=' instead of ' = '
            and Sections doesn't end with a newline
        """
        if self._defaults:
            fp.write("[%s]\r\n" % DEFAULTSECT)
            for (key, value) in self._defaults.items():
                fp.write("%s = %s\r\n" % (key, str(value).replace('\n', '\r\n\t')))
            fp.write("\r\n")
        for section in self._sections:
            fp.write("[%s]\r\n" % section)
            for (key, value) in self._sections[section].items():
                if key == "__name__":
                    continue
                if (value is not None) or (self._optcre == self.OPTCRE):
                    # This is the important departure from ConfigParser for what you are looking for
                    key = "=".join((key, value.replace('\n', '\r\n\t')))
                fp.write("%s\r\n" % (key))
