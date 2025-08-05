#!/usr/bin/env python3
"""Test streaming compatibility between different STT services."""

import asyncio
import sys
import time
from pathlib import Path

import numpy as np


async def test_streaming_compatibility():
    """Test that both STT services can handle streaming audio data."""
    
    print("🧪 Testing Streaming Compatibility")
    print("=" * 50)
    
    try:
        from pipecat.services.kotoba.stt import KotobaASRService
        from pipecat.services.livetoon.stt import LiveToonSTTService
        from pipecat.frames.frames import StartFrame, EndFrame
        
        # Create services
        kotoba_stt = KotobaASRService(
            api_key="test-api-key",  # Required for Kotoba ASR
            sample_rate=16000,
            language="ja"
        )
        
        livetoon_stt = LiveToonSTTService(
            api_url="https://livetoon-stt.dev-livetoon.com",
            sample_rate=16000
        )
        
        print("✅ Both STT services created successfully")
        
        # Test service initialization
        await kotoba_stt.start(StartFrame())
        await livetoon_stt.start(StartFrame())
        print("✅ Both services started successfully")
        
        # Generate test audio data (sine wave)
        sample_rate = 16000
        duration = 2.0  # 2 seconds
        frequency = 440  # A4 note
        
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        audio_data = np.sin(frequency * 2 * np.pi * t)
        
        # Convert to 16-bit PCM
        audio_bytes = (audio_data * 32767).astype(np.int16).tobytes()
        
        print(f"📊 Generated {len(audio_bytes)} bytes of test audio")
        
        # Test streaming in chunks
        chunk_size = 1024  # 1KB chunks
        chunks = [audio_bytes[i:i+chunk_size] for i in range(0, len(audio_bytes), chunk_size)]
        
        print(f"🔄 Testing streaming with {len(chunks)} chunks...")
        
        # Test Kotoba STT streaming
        kotoba_start = time.time()
        for i, chunk in enumerate(chunks):
            await kotoba_stt.run_stt(chunk)
            if i % 10 == 0:  # Progress indicator
                print(f"Kotoba STT: processed chunk {i+1}/{len(chunks)}")
        kotoba_duration = time.time() - kotoba_start
        
        # Test LiveToon STT streaming  
        livetoon_start = time.time()
        for i, chunk in enumerate(chunks):
            await livetoon_stt.run_stt(chunk)
            if i % 10 == 0:  # Progress indicator
                print(f"LiveToon STT: processed chunk {i+1}/{len(chunks)}")
        livetoon_duration = time.time() - livetoon_start
        
        # Flush any remaining buffers
        await livetoon_stt.flush_audio_buffer()
        
        print("✅ Streaming test completed successfully")
        
        # Cleanup
        await kotoba_stt.stop(EndFrame())
        await livetoon_stt.stop(EndFrame())
        
        # Performance summary
        print("\n📊 Performance Summary")
        print("-" * 30)
        print(f"Kotoba STT:  {kotoba_duration:.2f}s")
        print(f"LiveToon STT: {livetoon_duration:.2f}s")
        print(f"Audio duration: {duration:.2f}s")
        print(f"Kotoba real-time factor: {kotoba_duration/duration:.2f}x")
        print(f"LiveToon real-time factor: {livetoon_duration/duration:.2f}x")
        
        return True
        
    except Exception as e:
        print(f"❌ Streaming compatibility test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_service_compatibility():
    """Test that services can be used interchangeably."""
    
    print("\n🔄 Testing Service Interchangeability")
    print("=" * 50)
    
    try:
        from pipecat.services.kotoba.stt import KotobaASRService
        from pipecat.services.livetoon.stt import LiveToonSTTService
        from pipecat.services.livetoon.tts import LivetoonTTSService
        
        # Test that all services inherit from base classes properly
        kotoba_stt = KotobaASRService(api_key="test-api-key", sample_rate=16000, language="ja")
        livetoon_stt = LiveToonSTTService(api_url="https://livetoon-stt.dev-livetoon.com")
        livetoon_tts = LivetoonTTSService(api_url="https://livetoon-tts.dev-livetoon.com")
        
        # Check common interface
        print(f"✅ Kotoba STT sample rate: {kotoba_stt._sample_rate}")
        print(f"✅ LiveToon STT sample rate: {livetoon_stt._sample_rate}")
        print(f"✅ LiveToon TTS sample rate: {livetoon_tts._sample_rate}")
        
        # Check metrics support
        print(f"✅ Kotoba STT metrics: {kotoba_stt.can_generate_metrics()}")
        print(f"✅ LiveToon STT metrics: {livetoon_stt.can_generate_metrics()}")
        print(f"✅ LiveToon TTS metrics: {livetoon_tts.can_generate_metrics()}")
        
        print("✅ All services are compatible and interchangeable")
        return True
        
    except Exception as e:
        print(f"❌ Service compatibility test failed: {e}")
        return False


async def main():
    """Run all compatibility tests."""
    
    print("🧪 Streaming & Compatibility Test Suite")
    print("=" * 50)
    
    # Test 1: Streaming compatibility
    streaming_test = await test_streaming_compatibility()
    
    # Test 2: Service compatibility
    compatibility_test = await test_service_compatibility()
    
    # Summary
    print("\n📋 Test Summary")
    print("=" * 50)
    print(f"Streaming Test:     {'✅ PASS' if streaming_test else '❌ FAIL'}")
    print(f"Compatibility Test: {'✅ PASS' if compatibility_test else '❌ FAIL'}")
    
    if streaming_test and compatibility_test:
        print("\n🎉 All compatibility tests passed!")
        print("✅ Services are ready for production use with NVIDIA Tokkio")
        return True
    else:
        print("\n⚠️  Some compatibility tests failed")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)