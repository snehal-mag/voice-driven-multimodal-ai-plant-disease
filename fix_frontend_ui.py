from pathlib import Path

path = Path("frontend/index.html")
source = path.read_text(encoding="utf-8")

spread = "...UI.en,"
if source.count(spread) != 3:
    raise SystemExit(
        f"STOP: Expected 3 English fallback spreads, found {source.count(spread)}. No changes made."
    )

marker = '};\n\n\n/* =========================================================\n   CLASS TRANSLATIONS'
if source.count(marker) != 1:
    raise SystemExit(
        "STOP: UI dictionary boundary not found exactly once. No changes made."
    )

# Remove references to UI.en from inside UI's own initialization.
source = source.replace(spread, "", 3)

# Apply English defaults only after the UI object has been created.
replacement = '''};

for (const lang of ["mr", "te", "ta"]) {
    Object.assign(UI[lang], UI.en, UI[lang]);
}


/* =========================================================
   CLASS TRANSLATIONS'''

source = source.replace(marker, replacement, 1)
path.write_text(source, encoding="utf-8")
print("Fixed UI initialization. English defaults are applied after UI is created.")
