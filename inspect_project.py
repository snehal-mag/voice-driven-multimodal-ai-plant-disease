from pathlib import Path
import json
import importlib.util

root = Path.cwd()

for folder in ["backend", "frontend", "training", "model"]:
    print(f"\n=== {folder.upper()} ===")
    path = root / folder
    if not path.exists():
        print("Folder missing")
        continue
    for item in sorted(path.rglob("*")):
        if item.is_file() and not any(
            part in {"__pycache__", ".git", "venv"} for part in item.parts
        ):
            print(f"{item.relative_to(root)} ({item.stat().st_size} bytes)")

classes_file = root / "model" / "combined_30_classes.json"
if classes_file.exists():
    classes = json.loads(classes_file.read_text(encoding="utf-8"))
    print(f"\nExisting model classes: {len(classes)}")

for module in ["torch", "torchvision", "fastapi", "uvicorn", "PIL", "edge_tts", "cv2"]:
    print(f"{module}: {'installed' if importlib.util.find_spec(module) else 'missing'}")

print("\n=== DATASET SPLITS ===")
for folder in ["combined_training_dataset", "new_plant_training_dataset"]:
    base = root / folder
    print(f"\n{folder}:")
    if base.exists():
        for split in ["train", "validation", "val", "test"]:
            split_path = base / split
            if split_path.is_dir():
                classes = [p for p in split_path.iterdir() if p.is_dir()]
                print(f"  {split}: {len(classes)} class folders")
