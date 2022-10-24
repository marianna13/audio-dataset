# ZAPSPLAT Data Card
## Dataset Overview
|Size of dataset|Number of audios|Duration|
|:----:|:-----:|:-----:|
|51 GB| 98716|196 hrs|
## Data Collection

|Source|<center>Collecting Method<center>|
|:---------:|:--------|
| [ZAPSPLAT Website](https://www.zapsplat.com/sound-effect-category)  |1.Scrape sound effects audio files URLs and the title of effects from ZAPSPLAT website. 2. Create meta.parquet - file with audio file URLs and titles. 3. Download mp3 audio file for each row in meta.parquet and create audio-json pairs for each <br>
## Preprocessing Principles

You may refer to [preprocess_zapsplat.py](/data_preprocess/preprocess_zapsplat.py) for all the details. Here is a concise summary:

We retrieve information
from the meta data (meta.csv) and form a 3-field `.json` file for each audio. Here are some audio-json pairs selected from the processed dataset:


#### 
<audio id="audio" controls="controls" preload="yes">
      <source id="flac" src="1.flac">
</audio><br>

```json
{
    "text": [
        "Medicine tablet or vitamin pill drop into an empty plastic pot 3"
    ],
    "tag": [
        "Household",
        "Medicine"
    ],
    "original_data": {
        "title": "ZAPSPLAT dataset",
        "Description": "Free sound effects from ZAPSPLAT website",
        "audio_title": "Medicine tablet or vitamin pill drop into an empty plastic pot 3",
        "category": "Household",
        "URL": "https://www.zapsplat.com/wp-content/uploads/2015/sound-effects-61905/zapsplat_household_medicine_tablet_x1_drop_into_empty_plastic_pot_003_68518.mp3",
        "license": "Standard License",
        "tags": [
            "Household",
            "Medicine"
        ]
    }
}
```




### I. Json file generation principles 
-  **` text  entry`** We take title of the sound effect and put it into test attribute.
-  **` tag  entry`** We use tags from ZAPSPLAT website.
-  **` original data`** We save URL, tags, category and license (all those attributes are present on ZAPSPLAT website) for every audio as well as the dataset name and dataset description.

### II. Audio filtering principles
1. Keep audios with sampling rate higher than **16KHZ** and discard the rest.
2. Discard all audios failed to be read by `soundfile.read()` method or denied by FFmpeg while processing.
3. Split evry audio in segements with one sentence in each.
### III. Audio format specifications
After the preprocessing work, all audio files should be in FLAC format with sampling rate of 48KHZ. (Processed by ffmpeg).