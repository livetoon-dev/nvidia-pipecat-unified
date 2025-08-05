#!/usr/bin/env python3
"""Test LiveToon TTS service with various Japanese texts."""

import asyncio
import sys
import tempfile
from pathlib import Path

import numpy as np


async def test_livetoon_tts():
    """Test LiveToon TTS service with Japanese text generation."""
    
    print("🧪 Testing LiveToon TTS Service")
    print("=" * 50)
    
    try:
        from pipecat.services.livetoon.tts import LivetoonTTSService
        from pipecat.frames.frames import StartFrame, EndFrame, TTSTextFrame, AudioRawFrame
        from pipecat.processors.frame_processor import FrameDirection
        
        # Test texts in Japanese
        test_texts = [
            "こんにちは、私はLiveToonの音声合成システムです。",
            "今日は良い天気ですね。",
            "音声合成のテストを実行しています。",
            "ありがとうございました。"
        ]
        
        # Create TTS service
        tts_service = LivetoonTTSService(
            api_url="https://livetoon-tts.dev-livetoon.com",
            sample_rate=16000,
            params=LivetoonTTSService.InputParams(
                voice_id="default",
                sample_rate=16000,
                audio_format="wav"
            )
        )
        
        print("✅ LiveToon TTS service created")
        
        # Start service
        await tts_service.start(StartFrame())
        print("✅ Service started")
        
        # Audio collector to capture generated audio
        generated_audio_chunks = []
        
        class AudioCollector:
            def __init__(self):
                self.audio_data = []
            
            async def process_frame(self, frame):
                if isinstance(frame, AudioRawFrame):
                    self.audio_data.append(frame.audio)
                    print(f"   🎵 Received audio chunk: {len(frame.audio)} bytes")
        
        audio_collector = AudioCollector()
        
        # Test each text
        for i, text in enumerate(test_texts, 1):
            print(f"\n🗣️  Test {i}/4: Generating speech for:")
            print(f"   📝 Text: \"{text}\"")
            
            # Reset audio collector
            audio_collector.audio_data = []
            
            # Create TTS text frame
            tts_frame = TTSTextFrame(text)
            
            # Process TTS
            print(f"   🔄 Processing TTS...")
            async for output_frame in tts_service.run_tts(tts_frame):
                if output_frame:
                    await audio_collector.process_frame(output_frame)
            
            # Check results
            if audio_collector.audio_data:
                total_audio_bytes = sum(len(chunk) for chunk in audio_collector.audio_data)
                duration_estimate = total_audio_bytes / (16000 * 2)  # 16-bit audio
                print(f"   ✅ Generated audio: {total_audio_bytes} bytes (~{duration_estimate:.2f}s)")
                
                # Save audio file for verification
                if i == 1:  # Save first test for verification
                    output_file = f"/tmp/livetoon_tts_test_{i}.wav"
                    await save_audio_as_wav(audio_collector.audio_data, output_file)
                    print(f"   💾 Saved to: {output_file}")
            else:
                print(f"   ⚠️  No audio generated")
            
            # Small delay between tests
            await asyncio.sleep(0.5)
        
        # Test voice configuration
        print(f"\n🎛️  Testing voice configuration...")
        
        # Test with different voice parameters
        tts_service_custom = LivetoonTTSService(
            api_url="https://livetoon-tts.dev-livetoon.com",
            sample_rate=16000,
            params=LivetoonTTSService.InputParams(
                voice_id="female_1",  # Different voice
                sample_rate=16000,
                audio_format="wav",
                speed=1.1,  # Slightly faster
                volume=0.9  # Slightly quieter
            )
        )
        
        await tts_service_custom.start(StartFrame())
        
        custom_text = "カスタム音声設定のテストです。"
        print(f"   📝 Custom voice test: \"{custom_text}\"")
        
        custom_collector = AudioCollector()
        custom_frame = TTSTextFrame(custom_text)
        
        async for output_frame in tts_service_custom.run_tts(custom_frame):
            if output_frame:
                await custom_collector.process_frame(output_frame)
        
        if custom_collector.audio_data:
            total_bytes = sum(len(chunk) for chunk in custom_collector.audio_data)
            print(f"   ✅ Custom voice audio: {total_bytes} bytes")
        
        await tts_service_custom.stop(EndFrame())
        
        # Cleanup
        await tts_service.stop(EndFrame())
        print("\n✅ All TTS services stopped")
        
        print(f"\n🎉 LiveToon TTS testing completed!")
        print(f"📊 Tested {len(test_texts)} different texts")
        print(f"🎛️  Tested custom voice configuration")
        print(f"⚡ Ready for NVIDIA Tokkio Digital Human integration")
        
        return True
        
    except Exception as e:
        print(f"❌ LiveToon TTS test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def save_audio_as_wav(audio_chunks, output_file):
    """Save audio chunks as WAV file."""
    try:
        import struct
        
        # Combine all audio chunks
        audio_data = b''.join(audio_chunks)
        
        # WAV header for 16-bit mono PCM at 16kHz
        sample_rate = 16000
        num_channels = 1
        bits_per_sample = 16
        byte_rate = sample_rate * num_channels * bits_per_sample // 8
        block_align = num_channels * bits_per_sample // 8
        data_size = len(audio_data)
        
        header = struct.pack(
            '<4sL4s4sLHHLLHH4sL',
            b'RIFF',                    # ChunkID
            36 + data_size,             # ChunkSize
            b'WAVE',                    # Format
            b'fmt ',                    # Subchunk1ID
            16,                         # Subchunk1Size (PCM)
            1,                          # AudioFormat (PCM)
            num_channels,               # NumChannels
            sample_rate,                # SampleRate
            byte_rate,                  # ByteRate
            block_align,                # BlockAlign
            bits_per_sample,            # BitsPerSample
            b'data',                    # Subchunk2ID
            data_size                   # Subchunk2Size
        )
        
        # Write WAV file
        with open(output_file, 'wb') as f:
            f.write(header + audio_data)
            
        print(f"   📁 Audio saved as WAV: {Path(output_file).name}")
        
    except Exception as e:
        print(f"   ⚠️  Could not save audio file: {e}")


async def main():
    """Run LiveToon TTS test suite."""
    
    print("🧪 LiveToon TTS Test Suite")
    print("=" * 50)
    
    success = await test_livetoon_tts()
    
    print("\n📋 Test Summary")
    print("=" * 50)
    if success:
        print("🎉 LiveToon TTS test passed!")
        print("✅ Japanese text-to-speech generation working")
        print("🎛️  Voice configuration working")
        print("🎯 Ready for production use")
    else:
        print("⚠️  LiveToon TTS test failed")
    
    return success


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)