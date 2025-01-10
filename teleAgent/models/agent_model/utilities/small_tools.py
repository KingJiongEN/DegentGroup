import base64
from datetime import datetime
import os
import glob
import re
import subprocess
from typing import Dict, List
from PIL import Image
import io

from teleAgent.constants import TIMESTAMP_FORMAT

# from teleAgent.constants import TIMESTAMP_FORMAT


def keep_latest_k_files(folder_path, k, suffix=".mp3"):
    # Get all files with suffix in the folder
    interest_files = glob.glob(os.path.join(folder_path, f"*{suffix}"))
    
    # Sort files by modification time (newest first)
    interest_files.sort(key=os.path.getmtime, reverse=True)
    
    # Remove files if there are more than K
    if len(interest_files) > k:
        files_to_delete = interest_files[k:]
        for file_path in files_to_delete:
            os.remove(file_path)
            # print(f"Deleted: {file_path}")
            

def get_audio_duration(file_path):
    result = subprocess.run(
        [
            'ffprobe', '-i', file_path, '-show_entries', 'format=duration',
            '-v', 'quiet', '-of', 'csv=p=0'
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    duration = float(result.stdout)
    return duration

def extract_json_from_markdown(markdown_text):
        # Regular expression to match the content inside ```json``` tags
        pattern = r'```json\n(.*?)```'
        # Find all matches
        matches = re.findall(pattern, markdown_text, re.DOTALL)
        # If there are matches, return the first one
        if matches:
            # Remove leading and trailing whitespace and newlines
            json_content = matches[0].strip()
            return json_content
        else:
            return markdown_text
        
def rollback_to_time(data, time_str):
    """
    Rolls back the list of dictionaries to a specific time.
    
    Args:
        data (list of dict): The list of dictionaries to rollback.
        time_str (str): The time in the format TIMESTAMP_FORMAT to roll back to.
    
    Returns:
        list of dict: The rolled back list of dictionaries.
    """
    target_time = datetime.strptime(time_str, TIMESTAMP_FORMAT)
    rolled_back_data = []
    
    for item in data:
        assert 'timestamp' in item, f'The item does not have a timestamp field. Item: {item}'
        item_time = datetime.strptime(item['timestamp'], TIMESTAMP_FORMAT)
        if item_time <= target_time:
            rolled_back_data.append(item)
    
    return rolled_back_data

def get_base64_image(image_path: str, max_size: int = 400, quality: int = 70) -> str:
    """
    Convert image to compressed base64 string
    
    Args:
        image_path (str): Path to the image file
        max_size (int): Maximum dimension (width or height) of the output image
        quality (int): JPEG compression quality (1-100, higher is better quality but larger file)
        
    Returns:
        str: Compressed image as base64 string
    """
    # Open and compress image
    with Image.open(image_path) as img:
        # Convert to RGB if image is in RGBA mode
        if img.mode == 'RGBA':
            img = img.convert('RGB')
            
        # Calculate new dimensions while maintaining aspect ratio
        ratio = min(max_size / img.width, max_size / img.height)
        if ratio < 1:  # Only resize if image is larger than max_size
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            
        # Save compressed image to bytes buffer
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=quality, optimize=True)
        
        # Convert to base64
        return base64.b64encode(buffer.getvalue()).decode('utf-8')

def convert_pil_to_bytes(pil_image: Image.Image) -> io.BytesIO:
    img_byte_arr = io.BytesIO()
    pil_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)  # Move to the beginning of BytesIO object
    return img_byte_arr


def add_image_to_one_message(message: str, image_url: str) -> List[Dict]:
    """Add image to the message to conform to gpt4v format"""
    # Handle both local file paths and URLs
    if image_url.startswith(('http://', 'https://')):
        base64_image = get_base64_image(image_url)
    else:
        # For local files, read directly
        with open(image_url, 'rb') as image_file:
            import base64
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    messages = [
        {
            'role': 'user',
            'content': [
                {"type": "text", "text": message},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]
        }
    ]
    return messages