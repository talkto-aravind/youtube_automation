import os
import urllib.request
import ssl
import shutil

# Fix SSL issues in some environments
ssl._create_default_https_context = ssl._create_unverified_context

def download_asset(url, filepath, description):
    if not os.path.exists(filepath):
        print(f"⬇️  Downloading {description}...")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
                out_file.write(response.read())
            print(f"✅ Downloaded {description}.")
        except Exception as e:
            print(f"⚠️ Failed to download {description}: {e}")
            # Create dummy file to prevent crash
            with open(filepath, 'wb') as f: f.write(b'')
    else:
        print(f"✅ Found local {description} (Skipping download).")

def main():
    # 1. Setup Directory Structure
    root_dir = os.getcwd()
    assets_dir = os.path.join(root_dir, "visual_engine_v3", "public", "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    print(f"📂 Asset Directory: {assets_dir}\n")

    # 2. Define Standard Assets
    assets = {
        "audio": {
            "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
            "path": os.path.join(assets_dir, "mock_audio.mp3")
        },
        "hdr": {
            "url": "https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/1k/studio_small_09_1k.hdr",
            "path": os.path.join(assets_dir, "environment.hdr")
        },
        "font": {
            "url": "https://fonts.gstatic.com/s/poppins/v20/pxiByp8kv8JHgFVrLGT9Z1xlFQ.woff2",
            "path": os.path.join(assets_dir, "font.woff2")
        },
        "video": {
            "url": "https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4",
            "path": os.path.join(assets_dir, "mock_video.mp4")
        }
    }

    # 3. Check/Download Standard Assets
    download_asset(assets["audio"]["url"], assets["audio"]["path"], "Audio")
    download_asset(assets["hdr"]["url"], assets["hdr"]["path"], "Studio Lighting (HDR)")
    download_asset(assets["font"]["url"], assets["font"]["path"], "Poppins Font")

    # 4. Handle Video (Prefer Local Source)
    user_source_path = os.path.join(root_dir, "temp", "test_source.mp4")
    if os.path.exists(user_source_path):
        print(f"📂 Found local 'temp/test_source.mp4'. Copying to assets...")
        shutil.copy2(user_source_path, assets["video"]["path"])
    else:
        download_asset(assets["video"]["url"], assets["video"]["path"], "Fallback Video")

    # 5. Check Manual Cloud Asset
    cloud_path = os.path.join(assets_dir, "cloud.png")
    if os.path.exists(cloud_path):
        print(f"✅ Found Manual 'cloud.png'.")
    else:
        print(f"❌ MISSING 'cloud.png'. Please place your downloaded file in:")
        print(f"   {cloud_path}")

if __name__ == "__main__":
    main()