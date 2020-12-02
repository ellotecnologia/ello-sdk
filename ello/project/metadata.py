# encoding: utf8
from __future__ import unicode_literals

import os
import os.path
import json
import collections
import configparser
import glob

from delphi.dof import DOFFile


class ProjectMetadata:

    def __init__(self, metadata_file='package.json'):
        self._metadata = {}
        self.metadata_file = metadata_file or 'package.json'
        self.metadata_type = os.path.splitext(self.metadata_file)[1]

        # If metadata is json but the metadata file doesn't exists, try to open dof metadata
        if (self.metadata_type == '.json') and (not os.path.isfile(self.metadata_file)):
            self.metadata_file = self.get_current_project_name() + '.dof'
            self.metadata_type = os.path.splitext(self.metadata_file)[1]

        # No metadata found, let's get some info from the current folder.
        if not os.path.isfile(self.metadata_file):
            self._metadata['name'] = os.path.basename(os.getcwd())
            self._metadata['project_name'] = self._metadata['name']
            return
            
        self._load_metadata()

    def get_current_project_name(self):
        dof_files = glob.glob('*.dof') 
        if dof_files:
           return os.path.splitext(dof_files[0])[0]
        return ''

    def _load_metadata(self):
        if self.metadata_type == '.json':
            self._load_json_metadata()
        elif self.metadata_type == '.dof':
            self._load_dof_metadata()

    def _load_dof_metadata(self):
        dof = configparser.ConfigParser()
        dof.read(self.metadata_file)
        major = dof.get('Version Info', 'MajorVer')
        minor = dof.get('Version Info', 'MinorVer')
        release = dof.get('Version Info', 'Release')
        self._metadata['name'] = os.path.splitext(self.metadata_file)[0]
        self._metadata['version'] = '{}.{}.{}'.format(major, minor, release)

    def _load_json_metadata(self):
        with open(self.metadata_file, 'r') as f:
            self._metadata = json.load(
                f,
                object_pairs_hook=collections.OrderedDict
            )

        # Adiciona propriedade 'version_tag'
        if "tag-prefix" in self._metadata:
            self._metadata["version_tag"] = self._metadata["tag-prefix"] + self._metadata["version"]
        else:
            self._metadata["version_tag"] = self._metadata["version"]

    def update_version(self, version):
        """ Updates package.json version info and Project.dof version info """
        self._metadata['version'] = version

        with open('package.json', 'w') as f:
            f.write(json.dumps(self._metadata, indent=2))

        if os.path.isfile(self.name + '.dof'):
            dof_file = DOFFile(self.name + '.dof')
            dof_file.update_version(version)

    @property
    def project_name(self):
        if self._metadata.has_key("project_name"):
            return self._metadata["project_name"]
        else:
            return self.name + ".dpr"

    @property
    def resource_file(self):
        if self._metadata.has_key("resource_file"):
            return self._metadata["resource_file"]
        else:
            return self.name + ".rc"

    @property
    def resources(self):
        return self._metadata['resources']

    @property
    def conditionals(self):
        return self._metadata['conditionals']

    def __getattr__(self, name):
        return self._metadata[name]
        
    def dependencies(self):
        for dep in self._metadata['dependencies'].keys():
            hash = self._metadata['dependencies'][dep]
            repo = self._metadata['repos'].get(dep, '')
            yield dep, repo, hash


if __name__ == "__main__":
    metadata = ProjectMetadata()
    print(metadata.version)
