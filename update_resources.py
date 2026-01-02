import requests
import xml.etree.ElementTree as ET

# Your Sitemap URL
SITEMAP_URL = "https://resources.vallarasuk.com/post-sitemap.xml"

# 1. THE STATIC HEADER (Your Profile, Links, Tools)
# We store this inside the script so it always writes a FRESH copy.
README_HEADER = """# 🚀 Awesome Developer Resources

A curated collection of cheat sheets, interview guides, and roadmaps for modern developers.
**Maintained by [Vallarasu K](https://vallarasuk.com)**

---

## 🌐 Connect with Me
| Platform | Link |
| :--- | :--- |
| **Portfolio** | [vallarasuk.com](https://vallarasuk.com) |
| **LinkedIn** | [linkedin.vallarasuk.com](https://linkedin.vallarasuk.com) |
| **GitHub** | [github.vallarasuk.com](https://github.vallarasuk.com) |
| **Instagram** | [insta.vallarasuk.com](http://insta.vallarasuk.com/) |
| **WhatsApp Community** | [Join the Squad 🚀](http://squad.vallarasuk.com/) |

---

## 🛠️ My Products & Tools
Here are some free tools and SaaS products I have built:

| Project | Description | Link |
| :--- | :--- | :--- |
| **ATS Resume Maker** | Create ATS-friendly resumes for free. | [atsresumemaker.vallarasuk.com](https://atsresumemaker.vallarasuk.com/) |
| **Place Finder** | Find great places around you. | [placefinder.vallarasuk.com](https://placefinder.vallarasuk.com/) |
| **Dev Portfolio** | My developer-centric portfolio. | [dev.vallarasuk.com](https://dev.vallarasuk.com) |
| **Book Store** | Curated books collection. | [books.vallarasuk.com](https://books.vallarasuk.com/) |
| **Space App** | Explore the universe. | [space.vallarasuk.com](https://space.vallarasuk.com/) |

---

## 🧩 Extensions (VS Code & Chrome)
Boost your productivity with these extensions:

* **[Auto Console Log (VS Code)](https://marketplace.visualstudio.com/items?itemName=VallarasuKanthasamy.auto-console-log-by-vallarasu-kanthasamy)** - Insert console logs with one shortcut.
* **[Tech Stack Checker (Chrome)](https://chromewebstore.google.com/detail/tech-stack-checker/lhcplmfhkmjobfnndaabeddibhimghgf?hl=en)** - Identify website technologies instantly.
* **[Opacity Adjuster (Chrome)](https://chromewebstore.google.com/detail/opacity-adjuster/elgajofcbjicopepiodbabodkajnihog?hl=en)** - Change web element opacity for testing.
* **[View All VS Code Extensions](https://marketplace.visualstudio.com/publishers/VallarasuKanthasamy)**

---

## 📚 Latest Resources (Auto-Updated)
"""

# 2. THE FOOTER
README_FOOTER = """
## 🤝 Contributing
Have a great resource? Feel free to open a Pull Request!
"""

def get_resources():
    try:
        print("Fetching sitemap...")
        response = requests.get(SITEMAP_URL)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        ns = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        urls = root.findall('sitemap:url', ns)
        
        extracted_posts = []
        for url in urls:
            loc = url.find('sitemap:loc', ns).text
            
            lastmod_tag = url.find('sitemap:lastmod', ns)
            if lastmod_tag is not None:
                date_str = lastmod_tag.text
            else:
                date_str = "1970-01-01T00:00:00+00:00" 

            if loc == "https://resources.vallarasuk.com/":
                continue

            extracted_posts.append({'loc': loc, 'date': date_str})

        extracted_posts.sort(key=lambda x: x['date'], reverse=True)

        markdown_output = "| Resource Name | Link |\n| :--- | :--- |\n"
        
        for post in extracted_posts:
            slug = post['loc'].strip('/').split('/')[-1]
            title = slug.replace('-', ' ').title()
            markdown_output += f"| **{title}** | [Read Now]({post['loc']}) |\n"
            
        print(f"Successfully fetched {len(extracted_posts)} links.")
        return markdown_output

    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return None

def update_readme():
    # 1. Get the dynamic list
    resource_table = get_resources()
    
    if not resource_table:
        return

    # 2. Combine parts: HEADER + TABLE + FOOTER
    # We add markers just in case you want to switch back to regex later, but currently we overwrite everything.
    final_content = (
        README_HEADER + 
        "\n" +
        resource_table + 
        "\n" +
        README_FOOTER
    )

    # 3. OVERWRITE the file completely (This fixes the duplicate bug)
    with open("README.md", "w") as f:
        f.write(final_content)
    
    print("✅ README completely overwritten with fresh content!")

if __name__ == "__main__":
    update_readme()