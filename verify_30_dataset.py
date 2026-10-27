import json
from pathlib import Path

base = Path("combined_training_dataset")
classes = json.loads(
    Path("model/combined_30_classes.json").read_text(encoding="utf-8")
)

for split in ["train", "validation", "test"]:
    folder = base / split
    actual = {p.name for p in folder.iterdir() if p.is_dir()}
    expected = set(classes)

    print(f"\n{split.upper()}")
    print("Classes found:", len(actual))
    print("Missing classes:", sorted(expected - actual))
    print("Unexpected classes:", sorted(actual - expected))

print("\nCHECK COMPLETE")
