#!/usr/bin/env python3
"""Quick test for latest Pipecat compatibility."""

import asyncio


async def test_imports():
    """Test basic imports work with latest Pipecat."""
    
    print("🧪 Testing Latest Pipecat Compatibility")
    print("=" * 50)
    
    try:
        # Test core imports
        from pipecat.services.livetoon.stt import LiveToonSTTService
        from pipecat.services.livetoon.tts import LivetoonTTSService
        from pipecat.services.kotoba.stt import KotobaASRService
        print("✅ All service imports successful")
        
        # Test service creation
        stt = LiveToonSTTService(
            api_url="https://livetoon-stt.dev-livetoon.com",
            sample_rate=16000
        )
        print("✅ LiveToon STT creation successful")
        
        tts = LivetoonTTSService(
            api_url="https://livetoon-tts.dev-livetoon.com",
            sample_rate=16000
        )
        print("✅ LiveToon TTS creation successful")
        
        kotoba = KotobaASRService(
            api_key="test-key",
            sample_rate=16000
        )
        print("✅ Kotoba ASR creation successful")
        
        # Test basic properties
        print(f"✅ STT can generate metrics: {stt.can_generate_metrics()}")
        print(f"✅ TTS can generate metrics: {tts.can_generate_metrics()}")
        print(f"✅ Kotoba can generate metrics: {kotoba.can_generate_metrics()}")
        
        print("\n🎉 Latest Pipecat compatibility confirmed!")
        print("✅ All services compatible with latest version")
        return True
        
    except Exception as e:
        print(f"❌ Compatibility test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run compatibility test."""
    success = await test_imports()
    return success


if __name__ == "__main__":
    success = asyncio.run(main())
    print(f"\n📋 Result: {'✅ PASS' if success else '❌ FAIL'}")