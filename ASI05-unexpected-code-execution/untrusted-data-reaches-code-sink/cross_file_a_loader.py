"""
cross_file_a_loader.py
Part 1/2 of a cross-file chain (see cross_file_b_sink.py): loads an untrusted
dataset at module level.
"""
from datasets import load_dataset

poisoned_dataset = load_dataset("attacker/poison-ds")
