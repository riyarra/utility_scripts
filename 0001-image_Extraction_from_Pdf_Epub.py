from pathlib import Path
import fitz 
from ebooklib import epub, ITEM_IMAGE
import argparse
import shutil


def extract_from_pdf(input_file: Path, output_dir: Path):
    doc = fitz.open(input_file)
    count = 0

    for page_no in range(len(doc)):
        page = doc[page_no]
        images = page.get_images(full=True)

        for img_index, img in enumerate(images, start=1):
            xref = img[0]
            image_data = doc.extract_image(xref)

            img_bytes = image_data["image"]
            img_ext = image_data["ext"]

            count += 1
            filename = output_dir / f"pdf_page_{page_no + 1:03d}_img_{img_index:03d}.{img_ext}"

            with open(filename, "wb") as f:
                f.write(img_bytes)

    print(f"Extracted {count} images from PDF.")


def extract_from_epub(input_file: Path, output_dir: Path):
    book = epub.read_epub(str(input_file))
    count = 0

    for item in book.get_items():
        if item.get_type() == ITEM_IMAGE:
            count += 1

            original_name = Path(item.get_name()).name
            suffix = Path(original_name).suffix or ".jpg"

            filename = output_dir / f"epub_img_{count:03d}{suffix}"

            with open(filename, "wb") as f:
                f.write(item.get_content())

    print(f"Extracted {count} images from EPUB.")


def main():
    parser = argparse.ArgumentParser(description="Extract images from PDF or EPUB.")
    parser.add_argument("input_file", help="Path to PDF or EPUB file")
    parser.add_argument("output_folder", help="Folder where images will be saved")

    args = parser.parse_args()

    input_file = Path(args.input_file)
    output_dir = Path(args.output_folder)

    output_dir.mkdir(parents=True, exist_ok=True)

    ext = input_file.suffix.lower()

    if ext == ".pdf":
        extract_from_pdf(input_file, output_dir)
    elif ext == ".epub":
        extract_from_epub(input_file, output_dir)
    else:
        raise ValueError("Only PDF and EPUB files are supported.")


if __name__ == "__main__":
    main()
