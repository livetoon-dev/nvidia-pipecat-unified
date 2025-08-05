#!/usr/bin/env python3
"""Example: How to use LiveToon STT with automatic VAD."""

import asyncio
from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.services.livetoon.stt import LiveToonSTTService
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask


async def main():
    """LiveToon STT with automatic VAD example."""
    
    # 1. Create VAD analyzer (automatically detects speech)
    vad = SileroVADAnalyzer(
        sample_rate=16000,
        # VAD sends UserStartedSpeakingFrame/UserStoppedSpeakingFrame automatically
    )
    
    # 2. Create LiveToon STT service (responds to VAD frames) 
    stt = LiveToonSTTService(
        api_url="https://livetoon-stt.dev-livetoon.com",
        sample_rate=16000,
        params=LiveToonSTTService.InputParams(
            vad_enabled=True,  # Responds to VAD frames
            confidence_threshold=0.3
        )
    )
    
    # 3. Pipeline: Audio → VAD → STT
    pipeline = Pipeline([
        vad,   # Analyzes audio, sends VAD frames
        stt,   # Receives VAD frames + audio, does transcription
    ])
    
    # This automatically handles:
    # Audio → VAD detects speech → UserStartedSpeakingFrame → STT starts buffering
    # Audio → VAD detects silence → UserStoppedSpeakingFrame → STT transcribes
    
    print("✅ VAD + STT pipeline ready!")
    print("🎤 VAD will automatically detect speech and trigger transcription")


if __name__ == "__main__":
    asyncio.run(main())