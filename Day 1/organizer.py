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
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            logger.info("Processing File or Folder:"+ filename)
            
            # Check if it's a file (not a folder)
            if not os.path.isfile(file_path):
                logger.warning(f"Skipped (Not a file): {filename}")
                continue
            
                ext = os.path.splitext(filename)[1].lower()
                folder = "Others"

                # Find matching category
                for category, extensions in FILE_CATEGORIES.items():
                    if ext in extensions:
                        folder = category
                        break

                target_folder = os.path.join(directory, folder)
                os.makedirs(target_folder, exist_ok=True)
                
                try:
                    new_path = os.path.join(target_folder, filename)
                    if os.path.exists(new_path):
                        logger.warning("Oops!! File already exists")
                        new_path = os.path.join(target_folder, f"copy_{filename}")
                        logger.info("Renaming file to avoid overwrite")
                    shutil.move(file_path, new_path)
                    logger.info(f"✅ Moved {filename} -> {new_path}")
                except Exception as exp:
                    logger.error(f"Oops!! Error in moving {filename}: {exp}")
                    
    except Exception as exp:
        logger.critical(f"An Unexpected Error: {exp}", exc_info=True)
        click.echo("❌ An unexpected error occurred. Check 'organizer.log' for details.")


    click.echo("✅ Files organized successfully!")
    logger.info("✅ Files organized successfully!")

if __name__ == "__main__":
    organize()