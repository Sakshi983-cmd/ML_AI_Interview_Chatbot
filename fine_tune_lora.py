import json
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from peft import get_peft_model, LoraConfig, TaskType

# Step 1: Load Config
with open("training/config.json") as f:
    config = json.load(f)

# Step 2: Load Dataset
with open("training/dataset.json") as f:
    data = json.load(f)

inputs = [item["input"] for item in data]
outputs = [item["output"] for item in data]

# Step 3: Load Base Model & Tokenizer
tokenizer = AutoTokenizer.from_pretrained(config["model_name"])
base_model = AutoModelForCausalLM.from_pretrained(config["model_name"])

# Step 4: Apply LoRA
lora_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["c_attn"],  # For GPT2; use ["q_proj", "v_proj"] for LLaMA
    lora_dropout=0.1,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)
model = get_peft_model(base_model, lora_config)

# Step 5: Tokenize Inputs
input_encodings = tokenizer(inputs, truncation=True, padding=True)
output_encodings = tokenizer(outputs, truncation=True, padding=True)

# Step 6: Prepare Dataset
class SimpleDataset:
    def __init__(self, encodings_in, encodings_out):
        self.encodings_in = encodings_in
        self.encodings_out = encodings_out

    def __getitem__(self, idx):
        return {
            "input_ids": self.encodings_in["input_ids"][idx],
            "labels": self.encodings_out["input_ids"][idx]
        }

    def __len__(self):
        return len(self.encodings_in["input_ids"])

train_dataset = SimpleDataset(input_encodings, output_encodings)

# Step 7: Training Arguments
args = TrainingArguments(
    output_dir=config["save_dir"],
    per_device_train_batch_size=config["batch_size"],
    num_train_epochs=config["epochs"],
    learning_rate=config["learning_rate"],
    save_total_limit=1
)

# Step 8: Trainer Setup
trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_dataset,
    tokenizer=tokenizer
)

# Step 9: Train & Save
trainer.train()
model.save_pretrained(config["save_dir"])
tokenizer.save_pretrained(config["save_dir"])

print("✅ LoRA fine-tuning completed! Model saved at:", config["save_dir"])
