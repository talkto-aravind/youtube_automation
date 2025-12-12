import os

def audit_assets():
    print("🕵️ STARTING ASSET AUDIT...")
    print("=" * 60)
    
    # 1. Verify Directory
    frontend_assets = os.path.join("visual_engine_v3", "public", "assets")
    if not os.path.exists(frontend_assets):
        print(f"❌ CRITICAL ERROR: Asset directory missing: {frontend_assets}")
        return

    # 2. List of REQUIRED assets based on your codebase
    required_files = [
        "mock_audio.mp3",
        "mock_video.mp4",
        "environment.hdr",
        "font.woff2",
        "cloud.png"
    ]

    all_passed = True

    for filename in required_files:
        filepath = os.path.join(frontend_assets, filename)
        
        # Check Existence
        if not os.path.exists(filepath):
            print(f"❌ MISSING:   {filename}")
            all_passed = False
            continue
            
        # Check Size
        size = os.path.getsize(filepath)
        size_kb = size / 1024
        
        if size == 0:
            print(f"❌ CORRUPT:   {filename} (Size is 0 bytes - Download Failed)")
            all_passed = False
        elif size < 100: # Less than 100 bytes is suspicious for media/fonts
            print(f"⚠️ SUSPICIOUS: {filename} is very small ({size} bytes). Likely a text error file.")
            all_passed = False
        else:
            print(f"✅ OK:        {filename} ({size_kb:.2f} KB)")

    print("=" * 60)
    if all_passed:
        print("🎉 ALL ASSETS VALID. Issue is likely network/caching.")
    else:
        print("🚫 FIX REQUIRED: Delete the corrupt files and re-download/replace them.")

if __name__ == "__main__":
    audit_assets()