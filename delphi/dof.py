# encoding: utf8
from __future__ import unicode_literals

import fileinput
import re
import os.path
import codecs

from .custom_config_parser import CustomConfigParser

class DOFFile(object):
    
    def __init__(self, filename):
        self.filename = filename
        self.config = CustomConfigParser()
        with codecs.open(self.filename, 'r', encoding='latin1') as f:
           self.config.read_file(f)

    def update_version(self, version):
        version_split = version.split('.')
        if len(version_split) < 4:
            version_split.append('0')
        self.version = '.'.join(version_split)

    @property
    def version(self):
        major = self.config.get('Version Info', 'MajorVer')
        minor = self.config.get('Version Info', 'MinorVer')
        release = self.config.get('Version Info', 'Release')
        build = self.config.get('Version Info', 'Build')
        return "{}.{}.{}.{}".format(major, minor, release, build)

    @version.setter
    def version(self, value):
        major, minor, release, build = self._split_version(value)

        self.config.set('Version Info', 'MajorVer', major)
        self.config.set('Version Info', 'MinorVer', minor)
        self.config.set('Version Info', 'Release', release)
        self.config.set('Version Info', 'Build', build)

        self.config.set('Version Info Keys', 'FileVersion', value)
        self.config.set('Version Info Keys', 'ProductVersion', value)

        self.save()

    def _split_version(self, version):
        """ This allows splitting version number independently of
            its size (be it 1.2.3.4 or 1.2.3)
        """
        major = minor = release = build = '0'
        splitted_version = version.split('.')
        list_size = len(splitted_version)
        if list_size > 0:
            major = splitted_version[0]
        if list_size > 1:
            minor = splitted_version[1]
        if list_size > 2:
            release = splitted_version[2]
        if list_size > 3:
            build = splitted_version[3]
        return major, minor, release, build

    @property
    def conditionals(self):
        return self.config.get('Directories', 'Conditionals')

    @property
    def search_path(self):
        return self._change_variable_to_real_path(self.config.get('Directories', 'SearchPath'))

    def _change_variable_to_real_path(self, search_path):
        variables = set(re.findall('\$\((\w+)\)', search_path))
        for variable in variables:
            real_value = os.environ.get(variable)
            if not real_value:
                raise Exception("Environment variable {} is not defined".format(variable))
            search_path = re.sub('\$\({}\)'.format(variable), real_value, search_path)
        return search_path

    def get(self, section, option):
        return self.config.get(section, option)

    def set(self, section, option, value):
        self.config.set(section, option, value)

    def save(self):
        with codecs.open(self.filename, 'wb', encoding='latin1') as f:
            self.config.write(f)


def export_cfg_file(filename, mode, config):
    cfg_template_file = os.path.dirname(__file__) + '\\templates\\d7\\{}.config'.format(mode)
    with open(cfg_template_file) as f:
        cfg_template = f.read()
    config = {
        "directories_output_dir": config.get('Directories', 'OutputDir'),
        "directories_unit_output_dir": config.get('Directories', 'UnitOutputDir'),
        "search_path": config.search_path,
        #"conditionals": "-D" + config.conditionals
        "conditionals": ""
    }
    with open(filename, 'w') as f:
        f.write(cfg_template.format(**config))


def clear_dof_history(dof_file):
    """ Remove as seções de histórico do arquivo .dof """
    config = CustomConfigParser()
    config.read(dof_file)
    config.remove_section('HistoryLists\hlConditionals')
    config.remove_section('HistoryLists\hlUnitAliases')
    config.remove_section('HistoryLists\hlSearchPath')
    config.remove_section('HistoryLists\hlSearchPath')
    config.remove_section('HistoryLists\hlUnitOutputDirectory')
    config.remove_section('HistoryLists\hlOutputDirectorry')
    config.remove_section('HistoryLists\hlDebugSourcePath')
    config.write(open(dof_file, 'wb'))


def main():
    import sys
    dof = DOFFile('Ello.dof')
    export_cfg_file('Ello.cfg', sys.argv[1], dof)


if __name__ == "__main__":
    main()