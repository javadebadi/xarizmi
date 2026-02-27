from invoke.collection import Collection

from .code import ns_code
from .database import ns_database

ns = Collection()
ns.add_collection(ns_code)
ns.add_collection(ns_database)
