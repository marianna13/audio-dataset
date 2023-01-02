# Common Voice English Data Card
## Dataset Overview
|Size of dataset|Number of audios|Duration|
|:----:|:-----:|:-----:|
|8.7GB| 964 745 ||
## Data Collection

|Source|<center>Collecting Method<center>|
|:---------:|:--------|
| [Common Voice English website](https://commonvoice.mozilla.org/en/datasets)  |1.Download from the website <br>
## Preprocessing Principles

You may refer to [preprocess_common_voice.py](/data_preprocess/preprocess_common_voice.py) for all the details. Here is a concise summary:

For each audio, there are 5 fields in the metadata file, respectively named `file`, `text`, `gender`, `age` and `accent`. We retrieve information
from these 6 fields and form a 2-field `.json` file for each audio. Here are some audio-json pairs selected from the processed dataset:


#### 
<audio id="audio" controls="controls" preload="yes">
      <source id="flac" src="1.flac">
</audio><br>

```json
{
    "text": [
        "A person  saying \"Joe Keaton disapproved of films, and Buster also had reservations about the medium.\" "
    ],
    "original_data": {
        "title": "Common Voice",
        "description": "Each entry in the dataset consists of a unique MP3 and corresponding text file. Many of the 24,211 recorded hours in the dataset also include demographic metadata like age, sex, and accent that can help train the accuracy of speech recognition engines.",
        "license": "CC-0",
        "text": "Joe Keaton disapproved of films, and Buster also had reservations about the medium.",
        "accent": "",
        "gender": "person",
        "age": "",
        "filename": "common_voice_en_27710027.mp3"
    }
}
```




### I. Json file generation principles 
-  **` text  entry`** We just take data from `text` field of the original dataset and create a caption with template `a {age if present} person (or gender if present) saying "{text}" {with accent if present}`.

### II. Audio filtering principles
1. Keep audios with sampling rate higher than **16KHZ** and discard the rest.
2. Discard all audios failed to be read by `soundfile.read()` method or denied by FFmpeg while processing.
### III. Audio format specifications
After the preprocessing work, all audio files should be in FLAC format with sampling rate of 48KHZ. (Processed by ffmpeg).
