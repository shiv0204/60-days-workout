import shutil
from pathlib import Path
import argparse
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

extension_map = {ext:category for category, extns in FILE_CATEGORIES.items() for ext in extns}

def organize(directory):
    """CLI Tool to Organize Files in a Directory."""
    try:
        files = [f for f in directory.iterdir() if f.is_file()]
        
        for file_path in files:
            logger.info("Processing File or Folder:"+ file_path.name)
            
            ext = file_path.suffix.lower()
            folder = extension_map.get(ext,"Others")
            
            target_folder = directory / folder
            target_folder.mkdir(exist_ok = True)
            
            new_path = target_folder / file_path.name
            
            try:
                if file_path.parent != target_folder:
                    if new_path.exists():
                        logger.warning("Oops!! File already exists")
                        new_path = target_folder / f"copy_{file_path.name}"
                        logger.info("Renaming file to avoid overwrite")
                    
                    shutil.move(str(file_path), str(new_path))
                    logger.info(f"✅ Moved {file_path.name} -> {new_path}")
                else:
                    logger.info(f"Skipping {file_path.name}, already in correct folder.")

            except Exception as exp:
                logger.error(f"Oops!! Error in moving {file_path.name}: {exp}")
                    
    except Exception as exp:
        logger.critical(f"An Unexpected Error: {exp}", exc_info=True)
        print("❌ An unexpected error occurred. Check 'organizer.log' for details.")


    print("✅ Files organized successfully!")
    logger.info("✅ Files organized successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description= "Organize files in directory by ext. type")
    parser.add_argument("directory", type=str, help="Path to the directory to organize")
    
    args = parser.parse_args()
    
    directory_path = Path(args.directory)
    
    if not directory_path.exists():
        print(f"❌ Error: Directory '{args.directory}' does not exist.")
    else:
        organize(directory_path)