import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from tqdm import tqdm
import os.path

def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def flatten_content(data, result=None):
    if result is None:
        result = []
    for item in data:
        if item is None:
            continue
        title = ""
        if 'title' in item:
            title = item['title']
        elif 'link' in item and 'title' in item['link']:
            title = item['link']['title']

        # Append the current item's content_id and title
        result.append({'content_id': str(item['content_id']), 'title': title})
        # If there are sub-sections, process them recursively
        if item.get('sub_sections'):
            flatten_content(item['sub_sections'], result)
    return result

def download_content(item):
    base_url = "https://codes.iccsafe.org/api/content/chapter-xml/2241/"
    response = requests.get(f"{base_url}{item['content_id']}")
    if response.status_code == 200:
        unescaped_content = response.text.encode().decode('unicode_escape').replace("\/", "/")
        unescaped_content = unescaped_content[1:len(unescaped_content)-1]
        unescaped_content = unescaped_content.encode().decode('unicode_escape')
        return unescaped_content, item
    else:
        print(f"Failed to download content for {item['content_id']}")
        return None, None

def download_and_save_content(flattened_content):
    dump_dir = "./dump"
    os.makedirs(dump_dir, exist_ok=True)
    
    # Initialize tqdm with the total number of items
    progress_bar = tqdm(total=len(flattened_content))
    
    # Concurrently download content using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = []
        for item in flattened_content:
            file_path = os.path.join(dump_dir, f"{flattened_content.index(item)}_{item['content_id']}.html")
            # Check if file already exists
            if os.path.exists(file_path):
                progress_bar.update(1)
                continue
            # If file does not exist, submit download task
            futures.append(executor.submit(download_content, item))
        
        for future in as_completed(futures):
            unescaped_content, item = future.result()
            if unescaped_content is not None and item is not None:
                index = flattened_content.index(item)
                file_path = os.path.join(dump_dir, f"{index}_{item['content_id']}.html")
                with open(file_path, 'w') as file:
                    file.write(unescaped_content)
            
            # Update the progress bar
            progress_bar.update(1)
    
    # Close the progress bar
    progress_bar.close()


def main():
    filename = 'index.json'
    data = load_json(filename)
    flattened_content = flatten_content(data)
    download_and_save_content(flattened_content)

if __name__ == '__main__':
    main()
