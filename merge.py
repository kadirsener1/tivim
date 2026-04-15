import requests

# M3U linkleri (düzeltilmiş raw format)
m3u_urls = [
    "https://raw.githubusercontent.com/kadirsener1/tivim/main/1.m3u",
    "https://raw.githubusercontent.com/kadirsener1/atom/main/playlist.m3u"
]

output_file = "merged.m3u"

def fetch_m3u(url):
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Hata ({url}): {e}")
        return ""

def merge_m3u(urls):
    merged_lines = ["#EXTM3U"]
    seen = set()

    for url in urls:
        print(f"Çekiliyor: {url}")
        content = fetch_m3u(url)
        lines = content.splitlines()

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            if line.startswith("#EXTINF"):
                if i + 1 < len(lines):
                    stream_url = lines[i + 1].strip()

                    # Tekrar eden linkleri engelle
                    if stream_url not in seen:
                        merged_lines.append(line)
                        merged_lines.append(stream_url)
                        seen.add(stream_url)

                i += 2
            else:
                i += 1

    return "\n".join(merged_lines)

if __name__ == "__main__":
    merged_content = merge_m3u(m3u_urls)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(merged_content)

    print("✅ merged.m3u oluşturuldu ve güncellendi")
