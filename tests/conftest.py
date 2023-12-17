import pytest

from pymongo import MongoClient

import sys
print(sys.path)
from backend.config import *


@pytest.fixture(scope='module') 
def mongo():
    client = MongoClient(f'mongodb://{user_mongo}:{pass_mongo}@{ip_vps}:{port_mongo}')
    db = client.ARMarket
    dataset_test_collection = db.dataset_test
    return  dataset_test_collection

