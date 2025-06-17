import whisperx
import torch
from dotenv import load_dotenv
load_dotenv()


torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True

class Whisper():
  
  def __init__(self):
    self.device = "cuda"
    self.model = whisperx.load_model(
      "distil-large-v3-turbo", # distil-large-v3-turbo
      device=self.device,
      compute_type="int8_float16"
    )

  def transcribe(self, audio_path):
    audio = whisperx.load_audio(audio_path)
    result = self.model.transcribe(audio, batch_size=16)

    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=self.device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, self.device, return_char_alignments=False)
    transcription = '. '.join([segment['text'] for segment in result["segments"]])
    start, end = result['segments'][0]['start'], result['segments'][-1]['end']

    # with open("transcription.txt", "a") as f:
    #     f.write("[%.2fs -> %.2fs] %s\n" % (start, end, transcription))

    return transcription, start, end
  