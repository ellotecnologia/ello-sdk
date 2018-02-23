# encoding: utf8
import logging

from dof import DOFFile


class Project(object):

    def __init__(self, name):
        self._name = name
        self.config = DOFFile(self._name + '.dof')
        self.resources = []
        self.build_mode = 'debug'
        #self.conditionals = ''

    def get_config(self, section, option):
        return self.config.get(section, option)

    @property
    def name(self):
        return self._name

    @property
    def project_file(self):
        return self._name + '.dpr'

    @property
    def output_folder(self):
        return self.config.get("Directories", "OutputDir")

    @property
    def output_file(self):
        return self.output_folder + "\\{0}.exe".format(self._name)

    @property
    def version(self):
        return self.config.version

    @version.setter
    def version(self, value):
        self.config.version = value

    @property
    def conditionals(self):
        return self.config.get('Directories', 'Conditionals')

    @conditionals.setter
    def conditionals(self, value):
        self.config.set('Directories', 'Conditionals', value)
        self.config.save()

    def add_resource(self, resource_file):
        self.resources.append(resource_file)

    def __repr__(self):
        return self._name

    def __str__(self):
        return self._name
