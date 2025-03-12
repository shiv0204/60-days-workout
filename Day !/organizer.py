import shutil
import os
import click
import logging

#Setting up logger
logger = logging.getLogger("Organizer")
logger.setLevel(logging.INFO)
handler = logging.FileHandler('organizer.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Define file categories
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx",".page"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Music": [".mp3", ".wav"],
    "Archives": [".zip", ".rar", ".tar.gz"],
    "Code": [".py", ".java", ".cpp", ".js", ".html"],
    "Others": []
}

@click.command()
@click.argument("directory", type=click.Path(exists=True))
def organize(directory):
    """CLI Tool to Organize Files in a Directory."""
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        logger.info("File or Folder:"+ filename)
        if os.path.isfile(file_path):
            ext = os.path.splitext(filename)[1].lower()
            folder = "Others"

            # Find matching category
            for category, extensions in FILE_CATEGORIES.items():
                if ext in extensions:
                    folder = category
                    break

            target_folder = os.path.join(directory, folder)
            os.makedirs(target_folder, exist_ok=True)
            shutil.move(file_path, os.path.join(target_folder, filename))

    click.echo("✅ Files organized successfully!")

if __name__ == "__main__":
    organize()