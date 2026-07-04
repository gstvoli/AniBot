import re
import difflib
from pathlib import Path

def clean_file_tags(file_name):
    pattern_content = r'\[(.*?)\]'
    tags = re.findall(pattern_content, file_name)

    pattern_remove = r'\[.*?\]'
    clean_name = re.sub(pattern_remove, '', file_name)
    
    obj_path = Path(clean_name)
    pure_name = obj_path.stem
    ext = obj_path.suffix

    pure_name = re.sub(r'\s+', ' ', pure_name)
    pure_name = pure_name.strip()

    clean_name = f"{pure_name}{ext}"
    return tags, clean_name

def find_media_folder(clean_name, destination_path):
    destination_path = Path(destination_path)
    name_wout_ext = Path(clean_name).stem

    if ' - ' in name_wout_ext:
        base_name = name_wout_ext.split(' - ')[0].strip()
    else:
        base_name = name_wout_ext

    existent_folders = [p for p in destination_path.iterdir() if p.is_dir()]
    folder_names = [p.name for p in existent_folders]

    for folder in folder_names:
        if folder.lower() == base_name.lower() or folder.lower() in base_name.lower():
            return destination_path / folder
    
    correspondencies = difflib.get_close_matches(base_name, folder_names, n=1, cutoff=0.7)

    if correspondencies:
        folder_found = correspondencies[0]
        return destination_path / folder_found
    else:  
        return destination_path / base_name
