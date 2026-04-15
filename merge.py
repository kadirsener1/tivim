import requests
import os

m3u_urls = [
    "https://raw.githubusercontent.com/kadirsener1/tivim/main/1.m3u",
    "https://raw.githubusercontent.com/kadirsener1/atom/main/playlist.m3u"
]

output_file = "merged.m3u"

def fetch_m3u(url):
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        return r.text
    except:
        return ""

def parse_m3u(content):
    channels = []
    lines = content.splitlines()

    i = 0
    while i < len(lines):
        if lines[i].startswith("#EXTINF"):
            name = lines[i]
            if i + 1 < len(lines):
                url = lines[i + 1].strip()
                channels.append((name, url))
            i += 2
        else:
            i += 1
    return channels

def load_existing():
    if not os.path.exists(output_file):
        return []

    with open(output_file, "r", encoding="utf-8") as f:
        return parse_m3u(f.read())

def merge():
    existing = load_existing()
    existing_dict = {url: name for name, url in existing}

    new_channels = []

    for url in m3u_urls:
        content = fetch_m3u(url)
        new_channels.extend(parse_m3u(content))

    new_dict = {url: name for name, url in new_channels}

    final_list = []

    # 🔥 Eski sıralamayı koru + link güncelle
    for name, url in existing:
        if url in new_dict:
            final_list.append((new_dict[url], url))  # güncel isim
        else:
            final_list.append((name, url))  # aynen bırak

    # ➕ Yeni kanalları sona ekle
    for url, name in new_dict.items():
        if url not in existing_dict:
            final_list.append((name, url))

    # Dosyaya yaz
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for name, url in final_list:
            f.write(f"{name}\n{url}\n")

    print("✅ Sıralama korunarak güncellendi")

if __name__ == "__main__":
    merge()
