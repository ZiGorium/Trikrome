import os
import shutil
import re
from datetime import datetime

# Config
POSTS_DIR = "posts"
ARCHIVE_DIR = "archive"
INDEX_FILE = "index.html"
PLACEHOLDER_START = "<!-- POSTS_START -->"
PLACEHOLDER_END = "<!-- POSTS_END -->"
MAX_POSTS = 10

# Ensure archive folder exists
os.makedirs(ARCHIVE_DIR, exist_ok=True)

# Helper: extract date from HTML comment <!-- date: YYYY-MM-DD -->
def extract_date(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r"<!--\s*date:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})\s*-->", content)
    if match:
        return datetime.strptime(match.group(1), "%Y-%m-%d")
    else:
        # If no date found, use file modified time
        timestamp = os.path.getmtime(filepath)
        return datetime.fromtimestamp(timestamp)

# Step 1: Scan posts folder
posts = []
for filename in os.listdir(POSTS_DIR):
    if filename.endswith(".html"):
        path = os.path.join(POSTS_DIR, filename)
        date = extract_date(path)
        posts.append({"path": path, "date": date})

# Step 2: Sort descending by date
posts.sort(key=lambda x: x["date"], reverse=True)

# Step 3: Move older posts to archive
top_posts = posts[:MAX_POSTS]
old_posts = posts[MAX_POSTS:]

for post in old_posts:
    dest = os.path.join(ARCHIVE_DIR, os.path.basename(post["path"]))
    shutil.move(post["path"], dest)
    print(f"Archived: {post['path']} → {dest}")

# Step 4: Inject top posts into index.html
with open(INDEX_FILE, "r", encoding="utf-8") as f:
    index_content = f.read()

# Split at placeholder
start_idx = index_content.find(PLACEHOLDER_START)
end_idx = index_content.find(PLACEHOLDER_END)
if start_idx == -1 or end_idx == -1:
    raise ValueError("Placeholders not found in index.html")

before = index_content[:start_idx + len(PLACEHOLDER_START)] + "\n"
after = "\n" + index_content[end_idx:]

# Read top post content
injected_posts = ""
for post in top_posts:
    with open(post["path"], "r", encoding="utf-8") as f:
        injected_posts += f.read() + "\n"

# Write updated index.html
with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write(before + injected_posts + after)

print(f"Injected {len(top_posts)} posts into {INDEX_FILE}")
