import requests
import xml.etree.ElementTree as ET
import re
from datetime import datetime

# Your Sitemap URL
SITEMAP_URL = "https://resources.vallarasuk.com/post-sitemap.xml"

def get_resources():
    try:
        # Fetch the sitemap
        response = requests.get(SITEMAP_URL)
        response.raise_for_status()
        
        # Parse XML
        root = ET.fromstring(response.content)
        
        # Register namespace (standard for WP sitemaps)
        ns = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        urls = root.findall('sitemap:url', ns)
        
        # 1. Extract Data into a List
        extracted_posts = []
        for url in urls:
            loc = url.find('sitemap:loc', ns).text
            
            # Try to find the date, default to old date if missing
            lastmod_tag = url.find('sitemap:lastmod', ns)
            if lastmod_tag is not None:
                date_str = lastmod_tag.text
            else:
                date_str = "1970-01-01T00:00:00+00:00" 

            # Skip homepage
            if loc == "https://resources.vallarasuk.com/":
                continue

            extracted_posts.append({'loc': loc, 'date': date_str})

        # 2. SORT by Date (Reverse = Newest First) 📅
        extracted_posts.sort(key=lambda x: x['date'], reverse=True)

        # 3. Build Markdown Table (Top 20)
        # We add an extra newline \n to ensure spacing is clean
        markdown_output = "\n| Resource Name | Link |\n| :--- | :--- |\n"
        
        for post in extracted_posts[:20]:
            # Clean up title
            slug = post['loc'].strip('/').split('/')[-1]
            title = slug.replace('-', ' ').title()
            
            markdown_output += f"| **{title}** | [Read Now]({post['loc']}) |\n"
            
        return markdown_output

    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return None

def update_readme():
    new_content = get_resources()
    
    if not new_content:
        return

    with open("README.md", "r") as f:
        readme = f.read()
    
    # ⚠️ THIS IS THE CRITICAL FIX ⚠️
    # This regex looks specifically for the START and END comments
    pattern = r"()(.*?)()"
    
    # This replaces ONLY the middle part with the new table
    replacement = f"\\1{new_content}\\3"
    
    new_readme = re.sub(pattern, replacement, readme, flags=re.DOTALL)
    
    with open("README.md", "w") as f:
        f.write(new_readme)

if __name__ == "__main__":
    update_readme()