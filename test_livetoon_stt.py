#!/usr/bin/env python3
"""Test script for LiveToon STT service with actual audio file."""

import asyncio
import sys
from pathlib import Path

import aiohttp


async def test_livetoon_stt_api_direct():
    """Test LiveToon STT API directly with provided audio file."""
    
    audio_file_path = "/Users/daichi/Work/livetoon/nvidia/fuji_8b5dacb6-8f14-40be-9a43-5d47caaaba01.mp3"
    api_url = "https://livetoon-stt.dev-livetoon.com"
    
    if not Path(audio_file_path).exists():
        print(f"❌ Audio file not found: {audio_file_path}")
        return False
        
    print(f"🎵 Testing with audio file: {audio_file_path}")
    print(f"🌐 API URL: {api_url}")
    
    try:
        async with aiohttp.ClientSession() as session:
            # Read audio file first
            with open(audio_file_path, 'rb') as f:
                audio_data = f.read()
            
            # Prepare form data
            data = aiohttp.FormData()
            data.add_field('file', audio_data, filename='test_audio.mp3', content_type='audio/mpeg')
            data.add_field('decoding_type', 'tdt')
            
            # Send request
            transcribe_url = f"{api_url}/transcribe"
            print(f"📡 Sending request to: {transcribe_url}")
            
            async with session.post(transcribe_url, data=data) as response:
                print(f"📊 Response status: {response.status}")
                
                if response.status == 200:
                    result = await response.json()
                    print(f"✅ Transcription successful!")
                    print(f"📝 Text: {result.get('text', 'No text')}")
                    print(f"🎯 Confidence: {result.get('confidence', 'N/A')}")
                    print(f"⏱️  Duration: {result.get('duration', 'N/A')}s")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ API error: {response.status}")
                    print(f"📄 Error details: {error_text}")
                    return False
                    
    except aiohttp.ClientError as e:
        print(f"❌ HTTP error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


async def test_livetoon_stt_service():
    """Test LiveToon STT service class integration."""
    try:
        from pipecat.services.livetoon.stt import LiveToonSTTService
        
        # Create STT service
        stt = LiveToonSTTService(
            api_url="https://livetoon-stt.dev-livetoon.com",
            sample_rate=16000,
        )
        
        print(f"✅ LiveToon STT Service created successfully")
        print(f"📊 Sample rate: {stt._sample_rate}")
        print(f"🌐 API URL: {stt._api_url}")
        print(f"⚙️  Decoding type: {stt._params.decoding_type}")
        print(f"🎯 Confidence threshold: {stt._params.confidence_threshold}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating STT service: {e}")
        return False


async def main():
    """Run all tests."""
    print("🧪 LiveToon STT Testing Suite")
    print("=" * 50)
    
    # Test 1: Service creation
    print("\n📦 Test 1: Service Creation")
    service_test = await test_livetoon_stt_service()
    
    # Test 2: Direct API call
    print("\n🌐 Test 2: Direct API Call")
    api_test = await test_livetoon_stt_api_direct()
    
    # Summary
    print("\n📋 Test Summary")
    print("=" * 50)
    print(f"Service Creation: {'✅ PASS' if service_test else '❌ FAIL'}")
    print(f"Direct API Call:  {'✅ PASS' if api_test else '❌ FAIL'}")
    
    if service_test and api_test:
        print("🎉 All tests passed!")
        return True
    else:
        print("⚠️  Some tests failed")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)