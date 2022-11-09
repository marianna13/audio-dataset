# CMU Arctic Data Card
## Dataset Overview
|Size of dataset|Number of audios|Duration|
|:----:|:-----:|:-----:|
|1.4 GB| 13192|11.5 hrs|
## Data Collection

|Source|<center>Collecting Method<center>|
|:---------:|:--------
| [CMU Arctic Website](http://www.festvox.org/cmu_arctic/)  | Download the archive of audio files and the meta data from the website  <br>
## Preprocessing Principles

You may refer to [preprocess_cmu_arctic.py](/data_preprocess/preprocess_cmu_arctic.py) for all the details. Here is a concise summary:

We retrieve information
from the meta data and form a 3-field `.json` file for each audio. Here are some audio-json pairs selected from the processed dataset:


#### 
<audio id="audio" controls="controls" preload="yes">
      <source id="flac" src="1.flac">
</audio><br>

```json
{
    "text": [
        "A man reads out \"Famine had been my great ally.\" in the Indian accent"
    ],
    "tag": [
        "male",
        "Indian accent"
    ],
    "original_data": {
        "title": "CMU_Arctic",
        "description": "The databases consist of around 1150 utterances carefully selected from out-of-copyright texts from Project Gutenberg. The databses include US English male (bdl) and female (slt) speakers (both experinced voice talent) as well as other accented speakers.",
        "license": "BSD",
        "text": "Famine had been my great ally.",
        "accent": "Indian",
        "gender": "male",
        "filename": "cmu_in_male_3/arctic_b0436.wav"
    }
}
```




### I. Json file generation principles 
-  **` text  entry`** We take the reader gender, text and the accent of the reader and create a caption with template `A {gender} reads out "{text}" in the {accent} accent`.
-  **` tag  entry`** We use the gender and accent as tags.
-  **` original data`** We save filename, gender, text and accent as well as the dataset name, license and dataset description.

### II. Audio filtering principles
1. Keep audios with sampling rate higher than **16KHZ** and discard the rest.
2. Discard all audios failed to be read by `soundfile.read()` method or denied by FFmpeg while processing.
### III. Audio format specifications
After the preprocessing work, all audio files should be in FLAC format with sampling rate of 48KHZ. (Processed by ffmpeg).