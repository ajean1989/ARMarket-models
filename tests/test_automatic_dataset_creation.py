import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print(sys.path)
from src.model1.automatic_dataset_creation import automatic_dataset
import pytest

auto = automatic_dataset()

def test_reset(mongodb):
    docs = mongodb.dataset_test.find()
    assert len(docs) > 0 

    auto.reset()
    docs = mongodb.dataset_test.find()
    assert len(docs) == 0 