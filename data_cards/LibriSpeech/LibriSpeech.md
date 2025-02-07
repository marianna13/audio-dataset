# LibriSpeech Data Card
## Dataset Overview
|Size of dataset|Number of audios|
|:----:|:-----:|
|8.7GB| 56544 |
## Data Collection

|Source|<center>Collecting Method<center>|
|:---------:|:--------|
| [LibriSpeech HF website](https://huggingface.co/datasets/librispeech_asr)  |1.Download from HF Hub with HF cli <br>
## Preprocessing Principles

You may refer to [preprocess_librispeech.py](/data_preprocess/preprocess_librispeech.py) for all the details. Here is a concise summary:

For each audio, there are 6 fields in the metadata file, respectively named `file`, `audio`, `text`, `speaker_id`, `chapter_id` and `id`. We retrieve information
from these 6 fields and form a 2-field `.json` file for each audio. Here are some audio-json pairs selected from the processed dataset:


#### 
<audio id="audio" controls="controls" preload="yes">
      <source id="flac" src="1.flac">
</audio><br>

```json
{
    "text": [
        "a person saying \"saying above all make haste your recital could not be more minute exclaimed lecoq approvingly now how about these two women\""
    ],
    "original_data": {
        "title": "librispeech_asr",
        "description": "LibriSpeech is a corpus of approximately 1000 hours of 16kHz read English speech, prepared by Vassil Panayotov with the assistance of Daniel Povey. ",
        "license": "CC BY 4.0",
        "filename": "6081-41997-0014.flac",
        "text": "SAYING ABOVE ALL MAKE HASTE YOUR RECITAL COULD NOT BE MORE MINUTE EXCLAIMED LECOQ APPROVINGLY NOW HOW ABOUT THESE TWO WOMEN",
        "speaker_id": 6081,
        "chapter_id": 41997,
        "id": "6081-41997-0014"
    }
}
```




### I. Json file generation principles 
-  **` text  entry`** We just take data from `text` field of the original dataset and create a caption with template `a person saying "{text}"`.

### II. Audio filtering principles
1. Keep audios with sampling rate higher than **16KHZ** and discard the rest.
2. Discard all audios failed to be read by `soundfile.read()` method or denied by FFmpeg while processing.
### III. Audio format specifications
After the preprocessing work, all audio files should be in FLAC format with sampling rate of 48KHZ. (Processed by ffmpeg).
