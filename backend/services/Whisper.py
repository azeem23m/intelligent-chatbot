from faster_whisper import WhisperModel
import torch

torch.backends.cuda.matmul.allow_tf32 = True  
torch.backends.cudnn.allow_tf32 = True

class Whisper():
  
  def __init__(self):
     self.model = WhisperModel(
        "models/whisper-small-codeswitching-ArabicEnglish-ct2",
        device="cuda",
        compute_type="float16"
    )

  def transcribe(self, audio_path, start, end):
    segments, info = self.model.transcribe(audio_path, beam_size=5, language='en')
    transcription = ''.join(segment.text for segment in segments)
    with open("transcription.txt", "a") as f:
        f.write("[%.2fs -> %.2fs] %s\n" % (start, end, transcription))

    return transcription
