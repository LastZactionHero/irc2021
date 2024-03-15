import os
import re

def cleanup(markdown_content):
    # Replace single newlines with a space
    cleaned_content = markdown_content.replace('\n\n', 'BREAKBREAK')
    cleaned_content = cleaned_content.replace('\n', ' ')
    cleaned_content = cleaned_content.replace('BREAKBREAK', '\n\n')
    # Replace double newlines with a single newline

    content = ""
    lines = cleaned_content.split("\n")
    for line in lines:
        if len(line) > 0 and line.startswith("# R"):
            section_number = re.search("R[0-9]+\.?[0-9]+\.?[0-9]+", line).group()
            title = line[line.index(section_number) + len(section_number):-1]
            section_depth = section_number.count(".") + 1

            line = "#" * section_depth + " " + section_number + ": " + title
            content += line + "\n"

        else:
            content += line + "\n"

    return content

def concatenate_markdown_files(markdown_dir):
    # Get list of markdown files in markdown directory and sort them numerically
    markdown_files = sorted([file for file in os.listdir(markdown_dir) if file.endswith(".md")], key=lambda x: int(x.split('_')[0]))
    
    concatenated_content = []
    for markdown_file in markdown_files:
        markdown_file_path = os.path.join(markdown_dir, markdown_file)
        with open(markdown_file_path, 'r', encoding='utf-8') as file:
            markdown_content = file.read()
            processed_content = cleanup(markdown_content)
            concatenated_content.append(processed_content)
    
    # Write concatenated content to out.md
    with open("out.md", 'w', encoding='utf-8') as file:
        file.write('\n\n'.join(concatenated_content))

# Example usage
markdown_dir = "./markdown"
concatenate_markdown_files(markdown_dir)
