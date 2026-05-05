import requests
import re

urls = [
    "https://raw.githubusercontent.com/kadirsener1/tivim/refs/heads/main/m3u/hit.m3u",
    "https://raw.githubusercontent.com/kadirsener1/tivim/refs/heads/main/m3u/ss.m3u",
    "https://raw.githubusercontent.com/kadirsener1/tivim/refs/heads/main/m3u/cafe.m3u",
    "https://raw.githubusercontent.com/kadirsener1/tivim/refs/heads/main/m3u/ulusal.m3u",
    "https://raw.githubusercontent.com/kadirsener1/tivim/refs/heads/main/m3u/cocuk.m3u",
]

def parse_m3u(content):
    """Her kanalı (meta_lines, url, kanal_adı) olarak parse et"""
    channels = {}
    order = []
    lines = content.strip().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("#EXTINF"):
            # Kanal adını al (virgülden sonraki kısım)
            match = re.search(r',(.+)$', line)
            channel_name = match.group(1).strip() if match else line
            
            meta_lines = [line]
            i += 1
            # EXTVLCOPT veya diğer meta satırları
            while i < len(lines) and lines[i].strip().startswith("#"):
                meta_lines.append(lines[i].strip())
                i += 1
            # URL satırı
            url = lines[i].strip() if i < len(lines) else ""
            
            if channel_name in channels:
                # Sadece linki güncelle, meta bilgileri koru
                channels[channel_name]["url"] = url
            else:
                channels[channel_name] = {
                    "meta": meta_lines,
                    "url": url
                }
                order.append(channel_name)
            i += 1
        else:
            i += 1
    return channels, order

all_channels = {}
all_order = []

for url in urls:
    print(f"Fetching: {url}")
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        content = resp.text
        channels, order = parse_m3u(content)
        
        for name in order:
            if name in all_channels:
                # Sadece URL güncelle
                all_channels[name]["url"] = channels[name]["url"]
            else:
                all_channels[name] = channels[name]
                all_order.append(name)
    except Exception as e:
        print(f"  HATA: {e}")

# merged.m3u yaz
with open("merged.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n\n")
    for name in all_order:
        ch = all_channels[name]
        for meta in ch["meta"]:
            f.write(meta + "\n")
        f.write(ch["url"] + "\n\n")

print(f"\nToplam {len(all_order)} kanal merged.m3u dosyasına yazıldı.")
