from pathlib import Path
import argparse
import random
import shutil


IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".tiff"
}


def distribute_images(source_folder: Path, output_folder: Path, number_of_folders: int):
    if number_of_folders <= 0:
        raise ValueError("Number of folders must be greater than 0.")

    images = [
        file for file in source_folder.iterdir()
        if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS
    ]

    if not images:
        print("No images found.")
        return

    random.shuffle(images)

    folders = []
    for i in range(1, number_of_folders + 1):
        folder = output_folder / f"folder_{i:02d}"
        folder.mkdir(parents=True, exist_ok=True)
        folders.append(folder)

    for image in images:
        selected_folder = random.choice(folders)
        destination = selected_folder / image.name

        counter = 1
        while destination.exists():
            destination = selected_folder / f"{image.stem}_{counter}{image.suffix}"
            counter += 1

        shutil.copy2(image, destination)

    print(f"Randomly distributed {len(images)} images into {number_of_folders} folders.")


def main():
    parser = argparse.ArgumentParser(description="Randomly distribute images into folders.")
    parser.add_argument("source_folder", help="Folder containing extracted images")
    parser.add_argument("output_folder", help="Folder where random folders will be created")
    parser.add_argument("number_of_folders", type=int, help="Number of folders to create")

    args = parser.parse_args()

    distribute_images(
        Path(args.source_folder),
        Path(args.output_folder),
        args.number_of_folders
    )


if __name__ == "__main__":
    main()
