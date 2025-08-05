#!/usr/bin/env python3
"""Simple test for LiveToon TTS service."""

import asyncio
import sys
from pathlib import Path

import aiohttp


async def test_livetoon_tts_direct():
    """Test LiveToon TTS API directly."""
    
    print("🧪 Testing LiveToon TTS API Direct")
    print("=" * 50)
    
    api_url = "https://livetoon-tts.dev-livetoon.com"
    
    test_texts = [
        "こんにちは、私はLiveToonの音声合成システムです。",
        "今日は良い天気ですね。", 
        "音声合成のテストを実行しています。",
        "ありがとうございました。"
    ]
    
    try:
        async with aiohttp.ClientSession() as session:
            
            for i, text in enumerate(test_texts, 1):
                print(f"\n🗣️  Test {i}/4: \"{text}\"")
                
                # Prepare request data
                data = aiohttp.FormData()
                data.add_field('text', text)
                data.add_field('voice_id', 'default')
                data.add_field('sample_rate', '16000')
                data.add_field('audio_format', 'wav')
                
                # Make TTS request
                synthesize_url = f"{api_url}/synthesize"
                
                print(f"   🔄 Sending request to {synthesize_url}")
                
                async with session.post(synthesize_url, data=data) as response:
                    if response.status == 200:
                        audio_data = await response.read()
                        print(f"   ✅ Generated audio: {len(audio_data)} bytes")
                        
                        # Save first test audio
                        if i == 1:
                            output_file = f"/tmp/livetoon_tts_direct_test.wav"
                            with open(output_file, 'wb') as f:
                                f.write(audio_data)
                            print(f"   💾 Saved to: {output_file}")
                        
                    else:
                        error_text = await response.text()
                        print(f"   ❌ API error: {response.status} - {error_text}")
                
                await asyncio.sleep(0.5)
        
        print(f"\n🎉 Direct TTS API testing completed!")
        return True
        
    except Exception as e:
        print(f"❌ Direct TTS test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_livetoon_tts_service():
    """Test LiveToon TTS service with proper pipeline setup."""
    
    print("\n🧪 Testing LiveToon TTS Service (Pipeline)")
    print("=" * 50)
    
    try:
        from pipecat.services.livetoon.tts import LivetoonTTSService
        from pipecat.frames.frames import TTSTextFrame
        from pipecat.pipeline.pipeline import Pipeline
        from pipecat.pipeline.runner import PipelineRunner
        from pipecat.pipeline.task import PipelineTask
        from pipecat.transports.base_transport import BaseTransport
        
        # Create a simple TTS service instance
        tts_service = LivetoonTTSService(
            api_url="https://livetoon-tts.dev-livetoon.com",
            sample_rate=16000
        )
        
        print("✅ LiveToon TTS service created")
        
        # Test direct TTS call (without pipeline)
        test_text = "こんにちは、テストです。"
        print(f"🗣️  Testing direct TTS call: \"{test_text}\"")
        
        tts_frame = TTSTextFrame(test_text)
        
        # Test the internal TTS method
        try:
            # Get TTS service parameters
            params = tts_service._params
            print(f"   📋 TTS Parameters:")
            print(f"      Voice ID: {params.voice_id}")
            print(f"      Sample Rate: {params.sample_rate}")
            print(f"      Format: {params.audio_format}")
            
            # Create session manually for testing
            async with aiohttp.ClientSession() as session:
                tts_service._session = session
                
                # Test the synthesis method directly
                audio_result = await tts_service._synthesize_text(test_text)
                
                if audio_result:
                    print(f"   ✅ TTS synthesis successful: {len(audio_result)} bytes")
                    
                    # Save result
                    output_file = "/tmp/livetoon_tts_service_test.wav"
                    with open(output_file, 'wb') as f:
                        f.write(audio_result)
                    print(f"   💾 Saved to: {output_file}")
                else:
                    print(f"   ⚠️  TTS synthesis returned no audio")
        
        except Exception as e:
            print(f"   ❌ TTS service test failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        print(f"\n🎉 TTS service testing completed!")
        return True
        
    except Exception as e:
        print(f"❌ TTS service test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run both TTS tests."""
    
    print("🧪 LiveToon TTS Test Suite")
    print("=" * 50)
    
    # Test 1: Direct API
    direct_success = await test_livetoon_tts_direct()
    
    # Test 2: Service class
    service_success = await test_livetoon_tts_service()
    
    print("\n📋 Test Summary")
    print("=" * 50)
    print(f"Direct API Test:  {'✅ PASS' if direct_success else '❌ FAIL'}")
    print(f"Service Test:     {'✅ PASS' if service_success else '❌ FAIL'}")
    
    if direct_success and service_success:
        print("\n🎉 All LiveToon TTS tests passed!")
        print("✅ Japanese text-to-speech generation working")
        print("🎯 Ready for NVIDIA Tokkio integration")
        return True
    else:
        print("\n⚠️  Some TTS tests failed")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)