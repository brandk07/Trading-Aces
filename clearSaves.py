import os
import shutil

# List of save types
save_types = ["Blitz", "Career", "Goal"]

for save_to_clear in save_types:
    for base_dir in ["Saves", os.path.join("Saves", "Complete")]:
        try:
            # Path to clear
            save_path = os.path.join(base_dir, save_to_clear)
            
            # Remove directory and contents if exists
            if os.path.exists(save_path):
                shutil.rmtree(save_path)
                
            # Recreate empty directory
            os.makedirs(save_path, exist_ok=True)
            
            print(f"Successfully cleared {save_to_clear} saves in {base_dir}")
            
        except Exception as e:
            print(f"Error clearing {save_to_clear} saves in {base_dir}: {str(e)}")
