"""Pulls a Hugging Face Hub dataset straight into a Trainer.

Triggers training-dataset-without-integrity-record: the dataset
revision is unpinned and no checksum is verified against a known-good
manifest before the data is used to fine-tune the model.
"""
from datasets import load_dataset
from transformers import AutoModelForCausalLM, Trainer, TrainingArguments


def finetune_on_hub_dataset(model_name: str, dataset_name: str):
    dataset = load_dataset(dataset_name, split="train")  # no revision pin, no hash check
    model = AutoModelForCausalLM.from_pretrained(model_name)
    trainer = Trainer(
        model=model,
        args=TrainingArguments(output_dir="out"),
        train_dataset=dataset,
    )
    trainer.train()
