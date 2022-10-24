# Fine-grained Vocal Imitation Set Data Card
## Dataset Overview
|Size of dataset|Number of audios|Duration|
|:----:|:-----:|:-----:|
|222 MB| 760|1.3hrs|
## Data Collection

|Source|<center>Collecting Method<center>|
|:---------:|:--------|
| [Fine-grained Vocal Imitation Set website](https://zenodo.org/record/3538534)  |Download audio files and meta data from the the website. 2. For every row in the dataset download audio file from YouTube.  <br>
## Preprocessing Principles

You may refer to [preprocess_fine_grained_vocal_imitation_set.py](/data_preprocess/preprocess_fine_grained_vocal_imitation_set.py) for all the details. Here is a concise summary:

We retrieve information
from the meta data (vocal_imitations.csv) and form a 3-field `.json` file for each audio. Here are some audio-json pairs selected from the processed dataset:


#### 
<audio id="audio" controls="controls" preload="yes">
      <source id="flac" src="1.flac">
</audio><br>

```json
{
    "text": [
        "a dog growling"
    ],
    "tag": [
        "Animal",
        "Domestic animals, pets",
        "Dog"
    ],
    "original_data": {
        "title": "Fine-grained Vocal Imitation Set",
        "description": "This dataset includes 763 vocal imitations of 108 sound events. The sound event recordings were taken from a subset of Vocal Imitation Set.",
        "license": "Creative Commons Attribution 4.0 International",
        "category_d1": "Animal",
        "category_d2": "Domestic animals, pets",
        "category_d3": "Dog",
        "filename": "005Animal_Domestic animals_ pets_Dog_Growling-322.wav",
        "duration": 10,
        "participants_sound_recording_description": "a dog growling",
        "participants_sound_recording_description_confidence": "Very confident"
    }
}
```




### I. Json file generation principles 
-  **` text  entry`** We use `participants_sound_recording_description` as a text.
-  **` tag  entry`** We use `category_d1`, `category_d2` and  `category_d3` for each vocal imitation as tags.
-  **` original data`** We save all the data from each row of meta data for every audio as well as timestamps, dataset name and dataset description.

### II. Audio filtering principles
1. Keep audios with sampling rate higher than **16KHZ** and discard the rest.
2. Discard all audios failed to be read by `soundfile.read()` method or denied by FFmpeg while processing.
3. Split evry audio in segements with one sentence in each.
### III. Audio format specifications
After the preprocessing work, all audio files should be in FLAC format with sampling rate of 48KHZ. (Processed by ffmpeg).