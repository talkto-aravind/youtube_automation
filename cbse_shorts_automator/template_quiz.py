#!/usr/bin/env python3
"""
File: template_quiz.py
Quiz template for YouTube Shorts
UPDATED: 
- Parallel Audio (Fast)
- CTA moved up & bigger (Visual Polish)
- Karaoke readability (Black Stroke)
"""

import imagemagick_setup
import os
import concurrent.futures
from moviepy.editor import CompositeVideoClip, CompositeAudioClip, ColorClip, AudioFileClip, TextClip, vfx
from voice_manager import VoiceManager
from karaoke_manager import KaraokeManager
from video_processor import VideoProcessor
from sfx_manager import SFXManager  # <--- NEW IMPORT
# IMPORT THE NEW MODULE
import quiz_visuals

WIDTH = 1080
HEIGHT = 1920

class QuizTemplate:
    def __init__(self, engine):
        self.engine = engine
    
    def generate(self, video_path, script, config, output_path):
        print("📝 Generating Quiz Template (Parallel Processing)...")
        
        theme = self.engine.get_theme(config.get('theme', 'energetic_yellow'))
        voice_name = config.get('voice', 'NeeraNeural2')
        
        voice_mgr = self.engine.voice_manager
        # Select ONE voice for entire video
        selected_voice_key = voice_name if voice_name else voice_mgr.get_random_voice_name()
        print(f"   🎤 Using voice: {selected_voice_key} (consistent across all segments)")
        video_proc = VideoProcessor(temp_dir=self.engine.config['DIRS']['TEMP'])
        karaoke_mgr = KaraokeManager(voice_mgr, self.engine.config['DIRS']['TEMP'])
        sfx_mgr = SFXManager() # <--- NEW INITIALIZATION
        
        vid_id = os.path.basename(output_path).split('.')[0]
        temp_dir = self.engine.config['DIRS']['TEMP']
        audio_files = []
        
        # 1. Parallel Audio Generation
        print("   🎙️  Synthesizing 8 voiceover tracks...")
        audio_tasks = {
            'hook': script['hook_spoken'],
            'question': script['question_spoken'],
            'opt_a': f"A: {script['opt_a_spoken']}",
            'opt_b': f"B: {script['opt_b_spoken']}",
            'opt_c': f"C: {script['opt_c_spoken']}",
            'opt_d': f"D: {script['opt_d_spoken']}",
            'think': "Think fast!",
            # SEPARATED: Explanation and CTA are now distinct files
            'explanation': f"The answer is {script['correct_opt']}! {script['explanation_spoken']}",
            'cta': script['cta_spoken']
        }
        
        generated_audio_paths = {}

        def generate_single_audio(key, text):
            path = f"{temp_dir}/{vid_id}_{key}.mp3"
            voice_mgr.generate_audio_with_specific_voice(text, path, selected_voice_key, provider='google')
            return key, path

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(generate_single_audio, k, t) for k, t in audio_tasks.items()]
            for future in concurrent.futures.as_completed(futures):
                k, path = future.result()
                generated_audio_paths[k] = path
                audio_files.append(path)

        aud_hook = AudioFileClip(generated_audio_paths['hook'])
        aud_q = AudioFileClip(generated_audio_paths['question'])
        aud_a = AudioFileClip(generated_audio_paths['opt_a'])
        aud_b = AudioFileClip(generated_audio_paths['opt_b'])
        aud_c = AudioFileClip(generated_audio_paths['opt_c'])
        aud_d = AudioFileClip(generated_audio_paths['opt_d'])
        aud_think = AudioFileClip(generated_audio_paths['think'])
        aud_expl = AudioFileClip(generated_audio_paths['explanation'])
        aud_cta = AudioFileClip(generated_audio_paths['cta'])
        
       

        # 2. Timing
        THINK_TIME = 3.0 
        t_hook = 0
        t_q = t_hook + aud_hook.duration
        t_a = t_q + aud_q.duration
        t_b = t_a + aud_a.duration
        t_c = t_b + aud_b.duration
        t_d = t_c + aud_c.duration
        t_think = t_d + aud_d.duration
        t_ans = t_think + THINK_TIME
        
        t_cta = t_ans + aud_expl.duration
        t_outro = t_cta + aud_cta.duration
        
        OUTRO_DURATION = 4.0
        total_dur = t_outro + OUTRO_DURATION
        
        # --- PROPOSED FIX: INJECT RENDER LIMIT HERE ---
        render_limit = config.get('test_render_limit')
        if render_limit and isinstance(render_limit, (int, float)) and render_limit > 0:
            if render_limit < total_dur:
                print(f"    ✂️ LOGIC OVERRIDE: Clamping total duration to {render_limit}s.")
                total_dur = render_limit
        # ---------------------------------------------


       # Package timings for the visual module
        timings = {
            't_hook': t_hook,
            't_q': t_q,
            't_a': t_a,
            't_b': t_b,
            't_c': t_c,
            't_d': t_d,
            't_think': t_think,
            't_ans': t_ans,
            't_cta': t_cta,
            't_outro': t_outro,
            'expl_duration': aud_expl.duration,
            'cta_duration': aud_cta.duration
        }

        # 3. VISUAL COMPOSITION (DELEGATED)
        # We pass the engine (self.engine), video_proc, and data to the new module
        clips = quiz_visuals.build_quiz_visuals(
            engine=self.engine,
            video_proc=video_proc,
            video_path=video_path,
            script=script,
            timings=timings,
            total_dur=total_dur,
            config=config
        )

        # Audio
        # === NEW SFX IMPLEMENTATION ===
        print("   🔊 Engineering SFX Layer...")
        
        # Map current timings for the SFX Manager
        # Map current timings for the SFX Manager
        sfx_timings = {
            'q': t_q,
            'a': t_a, 'b': t_b, 'c': t_c, 'd': t_d,
            'think': t_think,
            'ans': t_ans,
            'cta': t_cta,
            'outro': t_outro
        }
        
        # Get professionally mixed SFX clips
        sfx_clips = sfx_mgr.generate_quiz_sfx(sfx_timings)
        
        # Combine: Voice + SFX
        audio_list = [aud_hook.set_start(t_hook), aud_q.set_start(t_q), aud_a.set_start(t_a),
                      aud_b.set_start(t_b), aud_c.set_start(t_c), aud_d.set_start(t_d),
                      aud_think.set_start(t_think), aud_expl.set_start(t_ans), aud_cta.set_start(t_cta)] # CHANGED: aud_ans -> aud_expl, added aud_cta
        
        # Flatten the list (Voice + SFX)
        full_audio_stack = audio_list + sfx_clips
        
        final_audio = self.engine.add_background_music(CompositeAudioClip(full_audio_stack), total_dur)

        final_video=CompositeVideoClip(clips, size=(WIDTH, HEIGHT))
        #print(f"The duration of the final_video video is: {final_video.duration} seconds")
        final_raw = final_video.set_audio(final_audio.subclip(0, final_video.duration))
        #final_raw = final_video
        #print(f"The duration of the composite video is: {final_raw.duration} seconds")
        
        try:
            self.engine.render_with_effects(final_raw, script, output_path)
        finally:
            if self.engine.config.get('DELETE_TEMP_FILES', True):
                import glob
                for f in audio_files:
                    if os.path.exists(f): os.remove(f)
                for pattern in [f'{temp_dir}/{vid_id}*', f'{vid_id}*TEMP_*']:
                    for temp_file in glob.glob(pattern):
                        try: os.remove(temp_file)
                        except: pass

        return {'duration': total_dur}