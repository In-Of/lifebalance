from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin, quote

# Путь к сайту (текущая директория)
site_root = Path(".")
base_url = "https://lifebalance.ru"

urlset = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']

for filepath in site_root.rglob("*.html"):
    if filepath.name.lower() in ["404.html", "offline.html"]:
        continue

    rel_path = filepath.relative_to(site_root)
    url_path = "/" + rel_path.as_posix()

    # Убираем index.html
    if url_path.endswith("/index.html"):
        url_path = url_path[:-10]
    elif url_path == "/index.html":
        url_path = "/"

    # URL должен быть в нормальной UTF-8 форме (для sitemap не нужен quote!)
    full_url = urljoin(base_url, url_path)

    lastmod = datetime.fromtimestamp(filepath.stat().st_mtime).date().isoformat()

    urlset.append("  <url>")
    urlset.append(f"    <loc>{full_url}</loc>")
    urlset.append(f"    <lastmod>{lastmod}</lastmod>")
    urlset.append("  </url>")

urlset.append("</urlset>")

# Запись в UTF-8
with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(urlset))
