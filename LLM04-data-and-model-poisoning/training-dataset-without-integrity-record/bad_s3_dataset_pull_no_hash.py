"""Pulls the fine-tuning corpus from S3 with no checksum comparison.

Triggers training-dataset-without-integrity-record: the object is
downloaded and used directly for training; there is no ETag/checksum
comparison against a recorded manifest, so an overwritten/tampered
object in the bucket would go unnoticed.
"""
import boto3

s3 = boto3.client("s3")


def download_training_corpus(bucket: str, key: str, dest: str = "/data/corpus.jsonl"):
    s3.download_file(bucket, key, dest)  # object could've been overwritten/tampered
    return dest
