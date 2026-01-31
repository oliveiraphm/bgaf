import torch
import numpy as np
from transformers import BarkProcessor, AutoModel, BarkProcessor, BarkModel
from schemas34 import VoicePresets

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def load_audio_model() -> tuple[BarkProcessor, BarkModel]:
    processor = BarkProcessor.from_pretrained("suno/bark-small")
    model = BarkModel.from_pretrained("suno/bark-small")
    model = model.to(device)
    return processor, model


def generate_audio(
    processor: BarkProcessor,
    model: BarkModel,
    prompt: str,
    preset: VoicePresets,
) -> tuple[np.array, int]:
    inputs = processor(text=[prompt], return_tensors="pt", voice_preset=preset)
    output = model.generate(**inputs, do_sample=True).cpu().numpy().squeeze()
    sample_rate = model.generation_config.sample_rate
    return output, sample_rate