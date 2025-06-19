import pandas as pd
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

class CSVHandler(FileSystemEventHandler):
    def __init__(self, js_file_path):
        self.js_file_path = js_file_path
        
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.csv'):
            print(f"New CSV detected: {event.src_path}")
            self.process_csv(event.src_path)
    
    def convert_csv_to_js_arrays(self, csv_path):
        """Convert CSV content to JavaScript arrays matching the specific structure"""
        # Read CSV with pandas using your specific parameters
        df = pd.read_csv(csv_path,
                        delimiter=';',
                        encoding='utf-8',
                        header=0)
        
        # Initialize the arrays exactly as in your script
        firstPart = []
        secondPart = []
        missingElement = []
        hints = []
        
        # Populate arrays from DataFrame values
        for array in df.values:
            firstPart.append(array[0])
            secondPart.append(array[1])
            missingElement.append(array[2])
            hints.append(array[3])
            
        return {
            'firstPart': firstPart,
            'secondPart': secondPart,
            'missingElement': missingElement,
            'hints': hints
        }
    
    def update_js_file(self, arrays):
        """Update JavaScript file with new arrays exactly matching the original format"""
        # Create JS array declarations matching your exact format
        js_content = [
            f"firstPart = [ {', '.join(f'\"{item}\"' for item in arrays['firstPart'])} ];",
            f"secondPart = [ {', '.join(f'\"{item}\"' for item in arrays['secondPart'])} ];",
            f"missingElement = [ {', '.join(f'\"{item}\"' for item in arrays['missingElement'])} ];",
            f"hints = [ {', '.join(f'\"{item}\"' for item in arrays['hints'])} ];"
        ]
        
        try:
            with open(self.js_file_path, 'r', encoding='utf-8') as file:
                existing_content = file.read()
            
            # Find the insertion point - now looking for the variable declarations
            insert_marker = "var firstPart, secondPart, missingElement;"
            
            if insert_marker in existing_content:
                # Split at the marker and then at the first semicolon after window.onload
                first_part = existing_content.split(insert_marker)[0]
                second_part = existing_content.split("window.onload")[1]
                
                # Combine everything
                new_content = (
                    f"{first_part}{insert_marker}\n"
                    f"{chr(10).join(js_content)}\n"
                    f"window.onload{second_part}"
                )
                
                # Write back to file
                with open(self.js_file_path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                print("JavaScript file updated successfully!")
            else:
                print("Variable declaration marker not found in JS file!")
        except Exception as e:
            print(f"Error updating JavaScript file: {e}")
    
    def process_csv(self, csv_path):
        """Process the CSV file and update JS"""
        try:
            arrays = self.convert_csv_to_js_arrays(csv_path)
            self.update_js_file(arrays)
            # Optionally move processed CSV to backup folder
            # os.rename(csv_path, os.path.join('processed', os.path.basename(csv_path)))
        except Exception as e:
            print(f"Error processing CSV: {e}")

def watch_directory(path_to_watch, js_file_path):
    """Set up directory watching"""
    event_handler = CSVHandler(js_file_path)
    observer = Observer()
    observer.schedule(event_handler, path_to_watch, recursive=False)
    observer.start()
    
    try:
        print(f"Watching directory: {path_to_watch}")
        print(f"Will update JS file: {js_file_path}")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopping directory watch...")
    observer.join()

if __name__ == "__main__":
    # Configure these paths for your setup
    WATCH_DIRECTORY = "./hot_folder"
    JS_FILE_PATH = "./missing-element.js"
    
    # Create watch directory if it doesn't exist
    os.makedirs(WATCH_DIRECTORY, exist_ok=True)
    
    # Start watching
    watch_directory(WATCH_DIRECTORY, JS_FILE_PATH)