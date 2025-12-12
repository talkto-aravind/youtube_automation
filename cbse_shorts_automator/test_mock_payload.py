import json
import random
import os

# Try to import USPContent
try:
    from usp_content_variations import USPContent
    print("✅ Loaded USPContent variations.")
except ImportError:
    # Fallback content if file is missing
    class USPContent:
        HOOKS = ["⚡ 7-MINUTE CHAPTER MASTERY ⚡"]
        TIMER_LABELS = ["⚡ THINK FAST"]
        ANSWER_PREFIXES = ["🎯 PERFECT!"]
        CTA_SOCIAL = ["🔔 SUBSCRIBE FOR MORE"]
        CTA_LINKS = ["Full Chapter Below"]
        OUTRO_MESSAGES = [("🚀 7-MINUTE CHAPTERS", "📚 Zero Boredom")]
        @staticmethod
        def get_random_hook(): return random.choice(USPContent.HOOKS)
        @staticmethod
        def get_random_timer_label(): return random.choice(USPContent.TIMER_LABELS)
        @staticmethod
        def get_random_answer_prefix(): return random.choice(USPContent.ANSWER_PREFIXES)
        @staticmethod
        def get_random_cta(): return (random.choice(USPContent.CTA_SOCIAL), random.choice(USPContent.CTA_LINKS))
        @staticmethod
        def get_random_outro(): return random.choice(USPContent.OUTRO_MESSAGES)

def generate_mock_scenario():
    # 1. Setup Directory Structure
    root_dir = os.getcwd()
    public_dir = os.path.join(root_dir, "visual_engine_v3", "public")
    # Note: Assets are expected to be in visual_engine_v3/public/assets/
    
    # 2. Verify Critical Assets Exist (Just a sanity check)
    required_assets = ["mock_audio.mp3", "mock_video.mp4", "font.woff2", "environment.hdr", "cloud.png"]
    missing = []
    for asset in required_assets:
        if not os.path.exists(os.path.join(public_dir, "assets", asset)):
            missing.append(asset)
    
    if missing:
        print(f"⚠️  WARNING: The following assets are missing in 'visual_engine_v3/public/assets/':")
        for m in missing: print(f"   - {m}")
        print("   (Run 'python3 download_assets.py' or check manual placement)")

    # 3. Generate JSON Payload (Strictly Local Paths)
    scenario = {
        "meta": {
            "version": "3.1",
            "resolution": { "w": 1080, "h": 1920 },
            "seed": random.randint(0, 999999),
            "duration_seconds": 10.0 
        },
        "assets": {
            "audio_url": "/assets/mock_audio.mp3", 
            "video_source_url": "/assets/mock_video.mp4",
            "thumbnail_url": "https://drive.google.com/uc?export=download&id=1Ajo0YbHKrlGOSPjB1mLGHvwMIrQOTRIV",
            "channel_logo_url": "/assets/logo.png",
            "font_url": "/assets/font.woff2",
            "env_map_url": "/assets/environment.hdr",
            "cloud_map_url": "/assets/cloud.png"
        },
        "timeline": {
            "hook": { "start_time": 0.0, "text_content": USPContent.get_random_hook() },
            "quiz": {
                "question": { "text": "Orbital Shape Quantum No.?", "start_time": 1.5 },
                "options": [
                    { "id": "A", "text": "Principal (n)", "start_time": 3.0 },
                    { "id": "B", "text": "Azimuthal (l)", "start_time": 4.0 },
                    { "id": "C", "text": "Magnetic (m)", "start_time": 5.0 },
                    { "id": "D", "text": "Spin (s)", "start_time": 6.0 }
                ]
            },
            "timer": { "start_time": 7.0, "duration": 3.0, "label_text": USPContent.get_random_timer_label() },
            "answer": { "start_time": 8.5, "correct_option_id": "B", "explanation_text": "Determines Shape", "celebration_text": USPContent.get_random_answer_prefix() },
            "cta": { "start_time": 9.0, "social_text": "SUBSCRIBE", "link_text": "LINK IN BIO" },
            "outro": { "start_time": 9.5, "line_1": "THANKS", "line_2": "WATCH MORE" }
        },
        "yt_overlay": { "progress_start": 0.15, "progress_end": 0.25 }
    }
    
    output_path = os.path.join(public_dir, "scenario_mock.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(scenario, f, indent=4)
    
    print(f"✨ Mock Payload Generated: {output_path}")

if __name__ == "__main__":
    generate_mock_scenario()