import pathlib

import yaml
from orator import DatabaseManager
from orator import Model


yml = pathlib.Path(__file__).parent / "orator.yml"

with open(yml) as fp:
    DATABASES = yaml.load(fp)

db = DatabaseManager(DATABASES["databases"])
Model.set_connection_resolver(db)
