import kagglehub

print("Starting Rice disease dataset download...")

path = kagglehub.competition_download(
    "paddy-disease-classification"
)

print("Dataset downloaded successfully!")
print("Path to competition files:", path)
