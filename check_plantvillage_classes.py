import json
from pathlib import Path

existing = set(json.loads(
    Path("model/combined_30_classes.json").read_text(encoding="utf-8")
))

dataset = Path("PlantVillage-Dataset/raw/color")

if not dataset.exists():
    print("PlantVillage dataset folder not found!")
    raise SystemExit(1)

available = sorted(
    folder.name for folder in dataset.iterdir()
    if folder.is_dir()
)

print("\nEXISTING MODEL CLASSES:", len(existing))
print("PLANTVILLAGE CLASSES:", len(available))

print("\nADDITIONAL PLANTVILLAGE CLASSES:")
for name in available:
    if name not in existing:
        count = sum(
            1 for f in (dataset / name).iterdir()
            if f.suffix.lower() in {".jpg", ".jpeg", ".png"}
        )
        print(f"{name}: {count} images")

print("\nTOTAL ADDITIONAL FOLDER LABELS:",
      len(set(available) - existing))
