# WavText5K Data Card
## Dataset Overview
|Size of dataset|Number of audios|
|:----:|:-----:|
|5.2 GB| 4525|
## Data Collection

|Source|<center>Collecting Method<center>|
|:---------:|:--------|
| [WavText5K GitHub repo](https://github.com/microsoft/WavText5K)  |1.Download meta data (WavText5K.csv) from the repo. 2. For evry row in meta data download th audio file using the download_link. <br>
## Preprocessing Principles

You may refer to [preprocess_WavText5K.py](/data_preprocess/preprocess_WavText5K.py) for all the details. Here is a concise summary:

We retrieve information
from the meta data (WavText5K.csv) and form a 3-field `.json` file for each audio. Here are some audio-json pairs selected from the processed dataset:


#### 
<audio id="audio" controls="controls" preload="yes">
      <source id="flac" src="1.flac">
</audio><br>

```json
{
    "text": "Dark Cavern dripping and glitches soundscape",
    "tag": [
        "glitches",
        "glitch",
        "cavern",
        "cave",
        "dark cavern",
        "dark",
        "sewer",
        "drip",
        "dripping",
        "soundscape"
    ],
    "original_data": {
        "title": "WavText5K",
        "license": "MIT License",
        "download_link": "https://soundbible.com/grab.php?id=161&type=wav",
        "view_link": "https://soundbible.com/161-Dark-Cavern-Soundscape.html",
        "fname": "dark cavern soundscape_1961.wav",
        "description": "WavText5K collection consisting of 4525 audios, 4348 descriptions, 4525 audio titles and 2058 tags.",
        "tags": [
            "glitches",
            "glitch",
            "cavern",
            "cave",
            "dark cavern",
            "dark",
            "sewer",
            "drip",
            "dripping",
            "soundscape"
        ],
        "audio_title": "Dark Cavern Soundscape",
        "audio_description": " Dark Cavern dripping and glitches soundscape"
    }
}
```




### I. Json file generation principles 
-  **` text  entry`** We take the description of audio from the meta data (if there's no description we construct a caption with template `the sound of {title}`).
-  **` tag  entry`** We use the entry in `tags` field or if there's no tags given we use the title as a tag.
-  **` original data`** We save original title, download link,view link, description and title of the audio, audio file name, the description and the title of the dataset itself.

### II. Audio filtering principles
1. Keep audios with sampling rate higher than **16KHZ** and discard the rest.
2. Discard all audios failed to be read by `soundfile.read()` method or denied by FFmpeg while processing.
### III. Audio format specifications
After the preprocessing work, all audio files should be in FLAC format with sampling rate of 48KHZ. (Processed by ffmpeg).