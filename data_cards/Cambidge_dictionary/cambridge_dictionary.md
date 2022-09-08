# Cambridge Dictionary Data Card
## Dataset Overview
|Size of dataset|Number of audios|
|:----:|:-----:|
|6.1 GB| 143000|
## Data Collection

|Source|<center>Collecting Method<center>|
|:---------:|:--------|
| [Cambridge Dictionary Website](https://dictionary.cambridge.org/)  |1.Scrape text and corresponding audio files URLs for British and American accent. 2. Create meta.csv - file with audio file URLs and pronounciations in two accents. 3. Download mp3 audio file for each row in meta.csv and create audio-json pairs for each <br>
## Preprocessing Principles

You may refer to [preprocess_cambridge_dictionary.py](/data_preprocess/preprocess_cambridge_dictionary.py) for all the details. Here is a concise summary:

We retrieve information
from the meta data (meta.csv) and form a 3-field `.json` file for each audio. Here are some audio-json pairs selected from the processed dataset:


#### 
<audio id="audio" controls="controls" preload="yes">
      <source id="flac" src="1.flac">
</audio><br>

```json
{
    "text": [
        "the person is reading the word downloadable in American accent"
    ],
    "tag": [
        "downloadable"
    ],
    "original_data": {
        "title": "Cambridge Dictionary dataset",
        "Description": "Words and their pronunciations scraped from the Cambridge Dictionary website",
        "URL": "https://dictionary.cambridge.org/media/english/us_pron/c/cus/cus00/cus00611.mp3",
        "accent": "American"
    }
}
```




### I. Json file generation principles 
-  **` text  entry`** We take the word from Cambridge Dictionary and create a caption with template `the person is reading the word {label} in American/British accent`.
-  **` tag  entry`** We use the word itself for each entry in the dataset as a tag.
-  **` original data`** We save URL and accent for every audio as well as duration of audio, the dataset name and dataset description.

### II. Audio filtering principles
1. Keep audios with sampling rate higher than **16KHZ** and discard the rest.
2. Discard all audios failed to be read by `soundfile.read()` method or denied by FFmpeg while processing.
### III. Audio format specifications
After the preprocessing work, all audio files should be in FLAC format with sampling rate of 48KHZ. (Processed by ffmpeg).