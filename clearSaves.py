import os
import shutil

saveToClear = 2# 0 = Blitz, 1 = Career, 2 = Goal

# List of save types
if saveToClear == None:
    for i in range(3):
        save_types = ["Blitz", "Career", "Goal"]
        save_to_clear = save_types[i]
        try:
            # Path to clear
            save_path = os.path.join("Saves", save_to_clear)
            
            # Remove directory and contents if exists
            if os.path.exists(save_path):
                shutil.rmtree(save_path)
                
            # Recreate empty directory
            os.makedirs(save_path, exist_ok=True)
            
            print(f"Successfully cleared {save_to_clear} saves")
            
        except Exception as e:
            print(f"Error clearing saves: {str(e)}")
            
save_types = ["Blitz", "Career", "Goal"]
save_to_clear = save_types[saveToClear]

try:
    # Path to clear
    save_path = os.path.join("Saves", save_to_clear)
    
    # Remove directory and contents if exists
    if os.path.exists(save_path):
        shutil.rmtree(save_path)
        
    # Recreate empty directory
    os.makedirs(save_path, exist_ok=True)
    
    print(f"Successfully cleared {save_to_clear} saves")
    
except Exception as e:
    print(f"Error clearing saves: {str(e)}")