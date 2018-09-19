__author__ = 'wontoniii'

"""Loading of configuration files and parameters.

@type version: L{twisted.python.versions.Version}
@var version: the version of this program
@type DEFAULT_CONFIG_FILES: C{list} of C{string}
@var DEFAULT_CONFIG_FILES: the default config files to load (in order)
@var DEFAULTS: the default config parameter values for the main program
@var DHT_DEFAULTS: the default config parameter values for the default DHT

"""

import os
import sys
from ConfigParser import SafeConfigParser

class ConfigError(Exception):
    """Errors that occur in the loading of configuration variables."""
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class ExtendedConfigParser(SafeConfigParser):
    """Adds 'gettime' and 'getstringlist' to ConfigParser objects.

    @ivar time_multipliers: the 'gettime' suffixes and the multipliers needed
        to convert them to seconds
    """

    time_multipliers={
        's': 1,    #seconds
        'm': 60,   #minutes
        'h': 3600, #hours
        'd': 86400,#days
        }

    def gettime(self, section, option):
        """Read the config parameter as a time value."""
        mult = 1
        value = self.get(section, option)
        if len(value) == 0:
            raise ConfigError("Configuration parse error: [%s] %s" % (section, option))
        suffix = value[-1].lower()
        if suffix in self.time_multipliers.keys():
            mult = self.time_multipliers[suffix]
            value = value[:-1]
        return int(float(value)*mult)

    def getstring(self, section, option):
        """Read the config parameter as a string."""
        return self.get(section,option)

    def getstringlist(self, section, option):
        """Read the multi-line config parameter as a list of strings."""
        return self.get(section,option).split()

    def optionxform(self, option):
        """Use all uppercase in the config parameters names."""
        return option.upper()

