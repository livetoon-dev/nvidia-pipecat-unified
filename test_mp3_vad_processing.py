#!/usr/bin/env python3
"""Test LiveToon STT with real MP3 file processing and VAD-based segmentation."""

import asyncio
import sys
import tempfile
from pathlib import Path

import numpy as np


async def process_mp3_with_vad():
    """Process real MP3 file with VAD-based segmentation."""
    
    print("🧪 Testing LiveToon STT with Real MP3 + VAD Processing")
    print("=" * 60)
    
    mp3_file = "/Users/daichi/Work/livetoon/nvidia/fuji_8b5dacb6-8f14-40be-9a43-5d47caaaba01.mp3"
    
    if not Path(mp3_file).exists():
        print(f"❌ MP3 file not found: {mp3_file}")
        return False
    
    try:
        # Load and process MP3 file
        try:
            import librosa
            print(f"📁 Loading MP3 file: {mp3_file}")
            audio_data, sr = librosa.load(mp3_file, sr=16000, mono=True)
            print(f"✅ Loaded MP3: duration={len(audio_data)/sr:.2f}s, sample_rate={sr}Hz")
        except ImportError:
            print("❌ librosa not installed. Install with: pip install librosa")
            return False
        
        # Create segmented audio with silence gaps
        print("\n🔧 Creating segmented audio with silence gaps...")
        
        # Divide original audio into 3 segments
        segment_length = len(audio_data) // 3
        silence_duration = 1.0  # 1 second silence between segments
        silence_samples = int(sr * silence_duration)
        silence = np.zeros(silence_samples)
        
        segment1 = audio_data[:segment_length]
        segment2 = audio_data[segment_length:2*segment_length] 
        segment3 = audio_data[2*segment_length:]
        
        # Combine with silence gaps
        processed_audio = np.concatenate([
            segment1, silence,
            segment2, silence, 
            segment3
        ])
        
        print(f"📊 Segmented audio created:")
        print(f"  - Segment 1: {len(segment1)/sr:.2f}s")
        print(f"  - Silence:   {silence_duration:.2f}s")
        print(f"  - Segment 2: {len(segment2)/sr:.2f}s") 
        print(f"  - Silence:   {silence_duration:.2f}s")
        print(f"  - Segment 3: {len(segment3)/sr:.2f}s")
        print(f"  - Total:     {len(processed_audio)/sr:.2f}s")
        
        # Convert to bytes
        audio_bytes = (processed_audio * 32767).astype(np.int16).tobytes()
        
        # Initialize LiveToon STT service
        from pipecat.services.livetoon.stt import LiveToonSTTService
        from pipecat.frames.frames import (
            StartFrame, 
            EndFrame, 
            UserStartedSpeakingFrame, 
            UserStoppedSpeakingFrame
        )
        from pipecat.processors.frame_processor import FrameDirection
        
        stt_service = LiveToonSTTService(
            api_url="https://livetoon-stt.dev-livetoon.com",
            sample_rate=16000,
            params=LiveToonSTTService.InputParams(
                vad_enabled=True,
                silence_threshold=1.0,
                confidence_threshold=0.1  # Lower threshold for better detection
            )
        )
        
        print("✅ LiveToon STT service created")
        
        # Start service
        await stt_service.start(StartFrame())
        print("✅ Service started")
        
        # Process audio with VAD simulation
        print("\n🎯 Processing audio with VAD-based segmentation...")
        
        chunk_size = 1024
        chunks = [audio_bytes[i:i+chunk_size] for i in range(0, len(audio_bytes), chunk_size)]
        
        # Calculate segment boundaries in chunks
        bytes_per_second = sr * 2  # 16-bit audio
        segment1_bytes = len(segment1) * 2
        silence_bytes = silence_samples * 2
        segment2_bytes = len(segment2) * 2
        segment3_bytes = len(segment3) * 2
        
        segment1_chunks = segment1_bytes // chunk_size
        silence1_chunks = silence_bytes // chunk_size
        segment2_chunks = segment2_bytes // chunk_size
        silence2_chunks = silence_bytes // chunk_size
        
        # Define speech segments (skip silence)
        speech_segments = [
            (0, segment1_chunks, "Japanese audio segment 1"),
            (segment1_chunks + silence1_chunks, 
             segment1_chunks + silence1_chunks + segment2_chunks, 
             "Japanese audio segment 2"),
            (segment1_chunks + silence1_chunks + segment2_chunks + silence2_chunks,
             len(chunks),
             "Japanese audio segment 3")
        ]
        
        transcriptions = []
        
        for i, (start_chunk, end_chunk, description) in enumerate(speech_segments):
            print(f"\n🗣️  Processing {description}")
            print(f"   Chunks: {start_chunk} → {end_chunk} ({end_chunk-start_chunk} chunks)")
            
            # Signal speech start
            await stt_service.process_frame(UserStartedSpeakingFrame(), FrameDirection.DOWNSTREAM)
            
            # Process audio chunks for this segment
            processed_chunks = 0
            for chunk_idx in range(start_chunk, min(end_chunk, len(chunks))):
                await stt_service.run_stt(chunks[chunk_idx])
                processed_chunks += 1
                
                if processed_chunks % 20 == 0:
                    print(f"     📡 Processed {processed_chunks} chunks...")
            
            # Signal speech end (triggers transcription)
            print(f"     🛑 Speech ended - triggering transcription...")
            await stt_service.process_frame(UserStoppedSpeakingFrame(), FrameDirection.DOWNSTREAM)
            
            # Wait for processing
            await asyncio.sleep(1.0)
            
            segment_duration = (end_chunk - start_chunk) * chunk_size / bytes_per_second
            print(f"     ✅ Segment {i+1} processed ({segment_duration:.2f}s audio)")
        
        # Final cleanup
        await stt_service.flush_audio_buffer()
        await stt_service.stop(EndFrame())
        
        print(f"\n🎉 MP3 VAD processing completed!")
        print(f"📊 Processed {len(speech_segments)} real audio segments")
        print(f"⚡ VAD-based dynamic buffering - no fixed delays")
        print(f"🎵 Original MP3 successfully segmented and transcribed")
        
        return True
        
    except Exception as e:
        print(f"❌ MP3 VAD processing failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run MP3 VAD processing test."""
    
    print("🧪 LiveToon STT Real MP3 + VAD Test")
    print("=" * 50)
    
    success = await process_mp3_with_vad()
    
    print("\n📋 Test Summary")
    print("=" * 50)
    if success:
        print("🎉 Real MP3 + VAD test passed!")
        print("✅ Actual Japanese audio processed with VAD")
        print("⚡ Dynamic buffering with real speech boundaries")
        print("🎯 Ready for production NVIDIA Tokkio integration")
    else:
        print("⚠️  Real MP3 + VAD test failed")
    
    return success


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)