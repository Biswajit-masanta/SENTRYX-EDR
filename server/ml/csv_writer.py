import csv
import os


def save_to_csv(features, filename="dataset.csv"):
    file_exists = os.path.isfile(filename)

    with open(filename, "a", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=features.keys()
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(features)