
from pathlib import Path
from urllib.request import urlretrieve

ROOT = Path(__file__).resolve().parents[1]

RAW_FOLDER = ROOT / "data" / "raw"
RAW_FOLDER.mkdir(parents=True, exist_ok=True)

URL = (
    "https://raw.githubusercontent.com/"
    "mimansha98/Tableau_Dashboards/master/"
    "sample-superstore.csv"
)

DESTINATION = RAW_FOLDER / "superstore.csv"

if DESTINATION.exists():
    print("Dataset already downloaded.")
else:
    print("Downloading retail dataset...")

    urlretrieve(URL, DESTINATION)

    print("Download completed.")

print("Dataset location:", DESTINATION)
