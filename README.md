# NVIDIA Pipecat Unified (Kotoba ASR + LiveToon TTS)

[![NVIDIA Compatible](https://img.shields.io/badge/NVIDIA-Tokkio_5.0.0--ga-green)](https://docs.nvidia.com/ace/) [![Pipecat 0.0.68](https://img.shields.io/badge/Pipecat-0.0.68-blue)](https://github.com/pipecat-ai/pipecat) [![Japanese AI](https://img.shields.io/badge/Language-Japanese_AI-red)](https://github.com/kotoba-tech)

**A unified Pipecat integration** combining Kotoba ASR (Japanese Speech-to-Text) and LiveToon TTS (Japanese Text-to-Speech) services, specifically optimized for **NVIDIA Tokkio Digital Human** applications.

> **🚀 One-Command Setup**: `uv add "pipecat-ai[livetoon] @ git+https://github.com/livetoon-dev/nvidia-pipecat-unified"`

## 🎯 Key Features

- ✅ **Dual STT Options**: Choose between Kotoba ASR (Whisper-based) or LiveToon STT (Parakeet-based)
- ✅ **VAD-Based STT**: LiveToon STT uses Voice Activity Detection for dynamic buffering
- ✅ **High-Quality TTS**: LiveToon TTS with multiple Japanese voices and emotional control
- ✅ **Single Installation**: One command installs all Japanese AI services
- ✅ **NVIDIA Tokkio Compatible**: Fixed to Pipecat 0.0.68 for full compatibility  
- ✅ **Japanese Optimized**: All services designed specifically for Japanese language
- ✅ **Production Ready**: Tested and optimized for real-time Digital Human applications
- ✅ **Simplified Build**: Replaces complex multi-step Docker builds with single dependency

## 🏗️ What This Solves

**Before** (Complex Multi-Step Build):
```bash
git clone https://github.com/NVIDIA/ace-controller.git
uv add "git+https://github.com/kotoba-tech/pipecat.git@feature/kotoba-asr#egg=pipecat-ai[kotoba]"
cd /tmp && git clone https://github.com/livetoon-dev/pipecat.git
cp /tmp/pipecat/src/pipecat/services/livetoon/* src/llm-rag/src/livetoon/
# Version conflicts, unstable builds, crashes...
```

**After** (Unified Solution):
```bash
uv add "pipecat-ai[livetoon] @ git+https://github.com/livetoon-dev/nvidia-pipecat-unified"
# Done! Both Kotoba ASR and LiveToon TTS ready to use
```

## 📦 Installation

### Prerequisites
- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager  
- NVIDIA Tokkio 5.0.0-ga environment

### Install with uv
```bash
# Install with both Kotoba ASR and LiveToon TTS
uv add "pipecat-ai[livetoon] @ git+https://github.com/livetoon-dev/nvidia-pipecat-unified"
```

### Manual Installation
```bash
# Clone repository
git clone https://github.com/livetoon-dev/nvidia-pipecat-unified.git
cd nvidia-pipecat-unified

# Install with uv
uv sync --extra livetoon
```

## 🔨 Usage Examples

### Complete ASR + TTS Pipeline (Option 1: Kotoba ASR + LiveToon TTS)
```python
import asyncio
from pipecat.services.kotoba.stt import KotobaASRService
from pipecat.services.livetoon.tts import LivetoonTTSService
from pipecat.services.openai.llm import OpenAILLMService
from pipecat.transports.daily_transport import DailyTransport
from pipecat.pipeline.pipeline import Pipeline

async def main():
    # Kotoba Japanese ASR (Speech-to-Text)
    stt = KotobaASRService(
        model="kotoba-whisper-v1.0",
        language="ja"
    )
    
    # LiveToon Japanese TTS (Text-to-Speech)
    tts = LivetoonTTSService(
        api_url="https://livetoon-tts.dev-livetoon.com",
        voice_id="default",
        sample_rate=24000
    )
    
    # LLM processing
    llm = OpenAILLMService(
        api_key="your-openai-key",
        model="gpt-4"
    )
    
    # Set up complete pipeline
    transport = DailyTransport(...)
    pipeline = Pipeline([transport, stt, llm, tts])
    
    await pipeline.run()

if __name__ == "__main__":
    asyncio.run(main())
```

### Complete Pipeline (Option 2: LiveToon ASR + LiveToon TTS)
```python
import asyncio
from pipecat.services.livetoon.stt import LiveToonSTTService
from pipecat.services.livetoon.tts import LivetoonTTSService
from pipecat.services.openai.llm import OpenAILLMService
from pipecat.transports.daily_transport import DailyTransport
from pipecat.pipeline.pipeline import Pipeline

async def main():
    # LiveToon Japanese ASR (Speech-to-Text) - NEW!
    stt = LiveToonSTTService(
        api_url="https://livetoon-stt.dev-livetoon.com",
        sample_rate=16000,
        params=LiveToonSTTService.InputParams(
            decoding_type="tdt",
            confidence_threshold=0.7,
            vad_enabled=True,
            silence_threshold=1.0
        )
    )
    
    # LiveToon Japanese TTS (Text-to-Speech)
    tts = LivetoonTTSService(
        api_url="https://livetoon-tts.dev-livetoon.com",
        voice_id="default",
        sample_rate=24000
    )
    
    # LLM processing
    llm = OpenAILLMService(
        api_key="your-openai-key",
        model="gpt-4"
    )
    
    # Set up complete pipeline
    transport = DailyTransport(...)
    pipeline = Pipeline([transport, stt, llm, tts])
    
    await pipeline.run()

if __name__ == "__main__":
    asyncio.run(main())
```

### Individual Service Examples

#### Kotoba ASR Only
```python
from pipecat.services.kotoba.stt import KotobaASRService

stt = KotobaASRService(
    model="kotoba-whisper-v1.0",
    language="ja",
    sample_rate=16000
)
```

#### LiveToon STT Only (NEW!)
```python
from pipecat.services.livetoon.stt import LiveToonSTTService

stt = LiveToonSTTService(
    api_url="https://livetoon-stt.dev-livetoon.com",
    sample_rate=16000,
    params=LiveToonSTTService.InputParams(
        decoding_type="tdt",        # "tdt" or "ctc"  
        confidence_threshold=0.7,   # 0.0-1.0
        vad_enabled=True,          # Use VAD-based dynamic buffering
        silence_threshold=1.0       # Silence duration to trigger transcription
    )
)
```

#### LiveToon TTS Only
```python
from pipecat.services.livetoon.tts import LivetoonTTSService

tts = LivetoonTTSService(
    api_url="https://livetoon-tts.dev-livetoon.com",
    voice_id="yasaike",  # Available: default, men, yasaike, zange, uranai
    alpha=0.5,           # Voice style (0.0-1.0)
    beta=0.8,            # Voice emotion (0.0-1.0)
    speed=1.2            # Speech speed (0.1-4.0)
)
```

## 🎯 NVIDIA Tokkio Integration

### Updated Dockerfile
Replace complex multi-step build process with single unified dependency:

```dockerfile
FROM python:3.10-slim

# Install uv
RUN pip install uv

# Install unified pipecat (replaces complex multi-repo setup)
RUN uv add "pipecat-ai[livetoon] @ git+https://github.com/livetoon-dev/nvidia-pipecat-unified"

# Copy application code
COPY . /app
WORKDIR /app

# Run application
CMD ["python", "main.py"]
```

### Simplified Build Process
```bash
# OLD: Complex multi-step process
## git clone https://github.com/NVIDIA/ace-controller.git
## uv add "git+https://github.com/kotoba-tech/pipecat.git@feature/kotoba-asr#egg=pipecat-ai[kotoba]"
## uv sync && rm -rf .venv && cd ..
## cp /tmp/pipecat/src/pipecat/services/livetoon/* src/llm-rag/src/livetoon/
## docker build --no-cache --build-context ace-controller=../ace-controller -t ace-controller:5.0.0-kotoba .

# NEW: Single command
uv add "pipecat-ai[livetoon] @ git+https://github.com/livetoon-dev/nvidia-pipecat-unified"
docker build -t ace-controller:5.0.0-unified .
```

## ⚠️ Troubleshooting

### Common Issues

#### 1. Version Conflicts
```bash
Error: Package version conflicts detected
```
**Solution:** This package uses Pipecat 0.0.68-compatible dependencies. Remove other Pipecat installations:
```bash
uv remove pipecat-ai
uv add "pipecat-ai[livetoon] @ git+https://github.com/livetoon-dev/nvidia-pipecat-unified"
```

#### 2. Import Errors
```python
ImportError: No module named 'pipecat.services.kotoba'
```
**Solution:** Ensure you installed with the `livetoon` extra:
```bash
uv add "pipecat-ai[livetoon] @ git+https://github.com/livetoon-dev/nvidia-pipecat-unified"
```

#### 3. NVIDIA Tokkio Compatibility Issues
```bash
Error: Incompatible pipecat version
```
**Solution:** This package is fixed to Pipecat 0.0.68 for NVIDIA Tokkio compatibility. Do not upgrade.

#### 4. LiveToon TTS API Connection
```bash
Error: Failed to connect to LiveToon TTS API
```
**Solution:** Verify API URL and credentials:
```python
tts = LivetoonTTSService(
    api_url="https://livetoon-tts.dev-livetoon.com",  # Correct URL
    api_key="your-api-key"  # If required
)
```

### Environment Variables
```bash
# LiveToon TTS API (if required)
export LIVETOON_TTS_API_KEY="your-tts-api-key"
export LIVETOON_TTS_API_URL="https://livetoon-tts.dev-livetoon.com"

# LiveToon STT API (if required)
export LIVETOON_STT_API_KEY="your-stt-api-key"
export LIVETOON_STT_API_URL="https://livetoon-stt.dev-livetoon.com"

# Kotoba ASR configuration
export KOTOBA_MODEL_PATH="/path/to/model"
```

## 🧪 Testing

### Basic Import Test
```bash
python -c "from pipecat.services.kotoba.stt import KotobaASRService; print('✅ Kotoba ASR: OK')"
python -c "from pipecat.services.livetoon.stt import LiveToonSTTService; print('✅ LiveToon STT: OK')"
python -c "from pipecat.services.livetoon.tts import LivetoonTTSService; print('✅ LiveToon TTS: OK')"
```

### Full Integration Test
```python
import asyncio
from pipecat.services.kotoba.stt import KotobaASRService
from pipecat.services.livetoon.stt import LiveToonSTTService
from pipecat.services.livetoon.tts import LivetoonTTSService

async def test_integration():
    # Test Kotoba ASR
    kotoba_stt = KotobaASRService(model="kotoba-whisper-v1.0", language="ja")
    print("✅ Kotoba ASR initialized")
    
    # Test LiveToon STT
    livetoon_stt = LiveToonSTTService(api_url="https://livetoon-stt.dev-livetoon.com")
    print("✅ LiveToon STT initialized")
    
    # Test LiveToon TTS
    livetoon_tts = LivetoonTTSService(api_url="https://livetoon-tts.dev-livetoon.com")
    print("✅ LiveToon TTS initialized")
    
    print("🎉 All services integration test passed!")

if __name__ == "__main__":
    asyncio.run(test_integration())
```

### LiveToon STT VAD-Based Processing Test
```python
# Test with VAD-based dynamic buffering
import asyncio
from pipecat.services.livetoon.stt import LiveToonSTTService
from pipecat.frames.frames import StartFrame, UserStartedSpeakingFrame, UserStoppedSpeakingFrame
from pipecat.processors.frame_processor import FrameDirection

async def test_livetoon_stt_vad():
    # Create STT service with VAD enabled
    stt = LiveToonSTTService(
        api_url="https://livetoon-stt.dev-livetoon.com",
        sample_rate=16000,
        params=LiveToonSTTService.InputParams(
            vad_enabled=True,
            confidence_threshold=0.5,
            silence_threshold=1.0
        )
    )
    
    await stt.start(StartFrame())
    
    # Simulate VAD-triggered processing
    await stt.process_frame(UserStartedSpeakingFrame(), FrameDirection.DOWNSTREAM)
    
    # Process audio chunks (example with your audio data)
    with open("audio.wav", "rb") as f:
        audio_data = f.read()
        chunk_size = 1024
        for i in range(0, len(audio_data), chunk_size):
            chunk = audio_data[i:i+chunk_size]
            await stt.run_stt(chunk)
    
    # Trigger transcription when speech stops
    await stt.process_frame(UserStoppedSpeakingFrame(), FrameDirection.DOWNSTREAM)

asyncio.run(test_livetoon_stt_vad())
```

### LiveToon STT Direct API Test
```python
# Test direct API call (without VAD)
import asyncio
import aiohttp

async def test_livetoon_stt_direct():
    async with aiohttp.ClientSession() as session:
        with open("audio.wav", "rb") as f:
            audio_data = f.read()
        
        data = aiohttp.FormData()
        data.add_field('file', audio_data, filename='audio.wav', content_type='audio/wav')
        data.add_field('decoding_type', 'tdt')
        
        async with session.post('https://livetoon-stt.dev-livetoon.com/transcribe', data=data) as response:
            result = await response.json()
            print(f"Transcription: {result.get('text')}")
            print(f"Confidence: {result.get('confidence')}")

asyncio.run(test_livetoon_stt_direct())
```

## 🔧 Configuration

### Kotoba ASR Configuration
```python
stt_config = {
    "model": "kotoba-whisper-v1.0",        # Available models
    "language": "ja",                       # Japanese language
    "sample_rate": 16000,                   # Audio sample rate
    "chunk_size": 8192                      # Processing chunk size
}
```

### LiveToon TTS Configuration
```python
tts_config = {
    "api_url": "https://livetoon-tts.dev-livetoon.com",
    "voice_id": "default",                  # default, men, yasaike, zange, uranai
    "alpha": 0.3,                          # Voice style control (0.0-1.0)
    "beta": 0.7,                           # Voice emotion control (0.0-1.0)
    "speed": 1.0,                          # Speech speed (0.1-4.0)
    "sample_rate": 24000,                  # Audio output sample rate
    "language": "ja"                       # Japanese language
}
```

## 📈 Version Information

- **Base**: Pipecat 0.0.68 (NVIDIA Tokkio compatible)
- **Kotoba ASR**: Based on [kotoba-tech/pipecat@feature/kotoba-asr](https://github.com/kotoba-tech/pipecat/tree/feature/kotoba-asr)
- **LiveToon TTS**: Based on [livetoon-dev/pipecat](https://github.com/livetoon-dev/pipecat)
- **Python**: 3.10+
- **Dependencies**: All fixed to 0.0.68-compatible versions

## 🔧 Development

### Local Development Setup
```bash
# Clone and setup
git clone https://github.com/livetoon-dev/nvidia-pipecat-unified.git
cd nvidia-pipecat-unified

# Install in development mode
uv sync --extra livetoon
```

### Generate uv.lock for Reproducible Builds
```bash
# Generate lock file for dependency stability
uv lock
```

## 📄 License

- **Pipecat**: BSD-2-Clause License
- **LiveToon TTS**: MIT License  
- **This Integration**: MIT License

## 🤝 Support & Contributing

### Support Channels
For issues related to:
- **NVIDIA Tokkio Integration**: [Create issue in this repository](https://github.com/livetoon-dev/nvidia-pipecat-unified/issues)
- **Kotoba ASR**: [kotoba-tech/pipecat](https://github.com/kotoba-tech/pipecat)
- **LiveToon TTS**: [livetoon-dev/pipecat](https://github.com/livetoon-dev/pipecat)

### Contributing
1. Fork this repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make changes ensuring 0.0.68 compatibility
4. Test with NVIDIA Tokkio
5. Submit pull request

---

**⚠️ Important Notice**: This package is specifically designed for NVIDIA Tokkio compatibility using Pipecat 0.0.68. Do not upgrade to newer Pipecat versions without thorough testing of the entire Tokkio stack.

**🚀 Quick Start**: `uv add "pipecat-ai[livetoon] @ git+https://github.com/livetoon-dev/nvidia-pipecat-unified"`
