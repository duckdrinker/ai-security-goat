"""
cross_file_b_sink.py
Part 2/2 of a cross-file chain (see cross_file_a_loader.py): deserializes the
records imported from there with pickle.loads() -- triggers
untrusted-data-reaches-code-sink via cross-file resolution
(crossFileDatasetToPickle_isFlagged).
"""
import pickle

from cross_file_a_loader import poisoned_dataset

for row in poisoned_dataset:
    obj = pickle.loads(row["pickle_data"])
    obj.train()
