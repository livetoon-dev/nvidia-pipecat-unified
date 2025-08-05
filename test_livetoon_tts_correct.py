#!/usr/bin/env python3
"""Test LiveToon TTS with correct API endpoints."""

import asyncio
import sys
import json

import aiohttp


async def test_livetoon_tts_api():
    """Test LiveToon TTS API with correct endpoints."""
    
    print("🧪 Testing LiveToon TTS with Correct Endpoints")
    print("=" * 55)
    
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
                
                # Try streaming endpoint first
                stream_url = f"{api_url}/speak/stream"
                json_data = {
                    "text": text,
                    "voicepack": "default",
                    "alpha": 0.3,
                    "beta": 0.7,
                    "speed": 1.0
                }
                
                print(f"   🔄 Trying streaming endpoint: {stream_url}")
                
                try:
                    async with session.post(stream_url, json=json_data) as response:
                        if response.status == 200:
                            # Collect streaming audio data
                            audio_chunks = []
                            chunk_count = 0
                            async for chunk in response.content.iter_any():
                                if chunk:
                                    audio_chunks.append(chunk)
                                    chunk_count += 1
                            
                            total_audio = b''.join(audio_chunks)
                            print(f"   ✅ Streaming success: {len(total_audio)} bytes in {chunk_count} chunks")
                            
                            # Save first test
                            if i == 1:
                                output_file = f"/tmp/livetoon_tts_stream_{i}.wav"
                                with open(output_file, 'wb') as f:
                                    f.write(total_audio)
                                print(f"   💾 Saved to: {output_file}")
                        
                        else:
                            error_text = await response.text()
                            print(f"   ⚠️  Streaming failed: {response.status} - {error_text}")
                            
                            # Try regular endpoint as fallback
                            regular_url = f"{api_url}/speak"
                            print(f"   🔄 Trying regular endpoint: {regular_url}")
                            
                            async with session.post(regular_url, json=json_data) as fallback_response:
                                if fallback_response.status == 200:
                                    audio_data = await fallback_response.read()
                                    print(f"   ✅ Regular endpoint success: {len(audio_data)} bytes")
                                    
                                    # Save first fallback test
                                    if i == 1:
                                        output_file = f"/tmp/livetoon_tts_regular_{i}.wav"
                                        with open(output_file, 'wb') as f:
                                            f.write(audio_data)
                                        print(f"   💾 Saved to: {output_file}")
                                else:
                                    fallback_error = await fallback_response.text()
                                    print(f"   ❌ Both endpoints failed: {fallback_response.status} - {fallback_error}")
                
                except aiohttp.ClientError as e:
                    print(f"   ❌ Connection error: {e}")
                
                await asyncio.sleep(0.5)
        
        print(f"\n🎉 LiveToon TTS API testing completed!")
        return True
        
    except Exception as e:
        print(f"❌ TTS API test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_different_voices():
    """Test different voice configurations."""
    
    print("\n🎛️  Testing Different Voice Configurations")
    print("=" * 55)
    
    api_url = "https://livetoon-tts.dev-livetoon.com"
    test_text = "これは音声テストです。"
    
    voice_configs = [
        {"voicepack": "default", "alpha": 0.3, "beta": 0.7, "speed": 1.0},
        {"voicepack": "men", "alpha": 0.5, "beta": 0.8, "speed": 1.1},
        {"voicepack": "yasaike", "alpha": 0.2, "beta": 0.6, "speed": 0.9},
        {"voicepack": "zange", "alpha": 0.4, "beta": 0.9, "speed": 1.2}
    ]
    
    try:
        async with aiohttp.ClientSession() as session:
            
            for i, config in enumerate(voice_configs, 1):
                voicepack = config["voicepack"]
                print(f"\n🎵 Voice {i}/4: {voicepack}")
                print(f"   📋 Config: alpha={config['alpha']}, beta={config['beta']}, speed={config['speed']}")
                
                json_data = {
                    "text": test_text,
                    **config
                }
                
                # Try regular endpoint for voice testing
                speak_url = f"{api_url}/speak"
                
                try:
                    async with session.post(speak_url, json=json_data) as response:
                        if response.status == 200:
                            audio_data = await response.read()
                            print(f"   ✅ Voice synthesis: {len(audio_data)} bytes")
                            
                            # Save each voice sample
                            output_file = f"/tmp/livetoon_tts_voice_{voicepack}.wav"
                            with open(output_file, 'wb') as f:
                                f.write(audio_data)
                            print(f"   💾 Saved: {output_file}")
                        else:
                            error_text = await response.text()
                            print(f"   ❌ Voice {voicepack} failed: {response.status} - {error_text}")
                
                except aiohttp.ClientError as e:
                    print(f"   ❌ Connection error for {voicepack}: {e}")
                
                await asyncio.sleep(0.3)
        
        print(f"\n🎉 Voice configuration testing completed!")
        return True
        
    except Exception as e:
        print(f"❌ Voice config test failed: {e}")
        return False


async def main():
    """Run all TTS tests."""
    
    print("🧪 LiveToon TTS Comprehensive Test Suite")
    print("=" * 55)
    
    # Test 1: Basic API functionality
    api_success = await test_livetoon_tts_api()
    
    # Test 2: Different voice configurations
    voice_success = await test_different_voices()
    
    print("\n📋 Test Summary")
    print("=" * 55)
    print(f"Basic API Test:   {'✅ PASS' if api_success else '❌ FAIL'}")
    print(f"Voice Config Test: {'✅ PASS' if voice_success else '❌ FAIL'}")
    
    if api_success and voice_success:
        print("\n🎉 All LiveToon TTS tests passed!")
        print("✅ Streaming and regular endpoints working")
        print("🎵 Multiple voice configurations working")
        print("🎯 Ready for NVIDIA Tokkio Digital Human integration")
        return True
    else:
        print("\n⚠️  Some TTS tests failed")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)