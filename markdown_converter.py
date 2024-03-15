import os
import html2text

def convert_html_to_markdown(html_file_path):
    # Read HTML file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Convert HTML to Markdown
    converter = html2text.HTML2Text()
    markdown_content = converter.handle(html_content)
    
    return markdown_content

def convert_html_files_to_markdown(dump_dir):
    markdown_dir = "./markdown"
    os.makedirs(markdown_dir, exist_ok=True)
    
    # Get list of HTML files in dump directory
    html_files = [file for file in os.listdir(dump_dir) if file.endswith(".html")]
    
    for html_file in html_files:
        html_file_path = os.path.join(dump_dir, html_file)
        markdown_content = convert_html_to_markdown(html_file_path)
        
        # Save Markdown content to markdown directory
        markdown_file_name = html_file.replace(".html", ".md")
        markdown_file_path = os.path.join(markdown_dir, markdown_file_name)
        
        with open(markdown_file_path, 'w', encoding='utf-8') as file:
            file.write(markdown_content)

# Example usage
dump_dir = "./dump"
convert_html_files_to_markdown(dump_dir)
