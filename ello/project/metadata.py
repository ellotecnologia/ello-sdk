# encoding: utf8
from __future__ import unicode_literals

import os
import json
import collections


class ProjectMetadata:

    def __init__(self, metadata_file='package.json'):
        self.metadata_file = metadata_file or 'package.json'
        self._load()

    def _load(self):
        """ Returns a dictionary with the project metadata
        """
        with open(self.metadata_file, 'r') as f:
            self._metadata = json.load(
                f,
                object_pairs_hook=collections.OrderedDict
            )

    def _save(self):
        """ Saves the project metadata to the file
        """
        with open(self.metadata_file, 'w') as f:
            f.write(json.dumps(self._metadata, indent=2))

    def update_version(self, version):
        self._metadata['version'] = version
        self._save()

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


if __name__ == "__main__":
    metadata = ProjectMetadata()
    print(metadata.version)
