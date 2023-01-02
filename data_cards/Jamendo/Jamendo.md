# Genius Data Card
## Dataset Overview
|Size of dataset|Number of audios|Duration|
|:----:|:-----:|:-----:|
|200 GB| 10000|657 hrs|
## Data Collection

|Source|<center>Collecting Method<center>|
|:---------:|:--------
| [Jamendo Website](https://www.juno.co.uk/products/wu-tang-clan-the-charmels-cream/861381-01/)  | Scrape all the metadata from the Juno website (audio links, reviews, song title, artist name). Download audio from audio lins. <br>
## Preprocessing Principles

You may refer to [preprocess_jamendo.py](/data_preprocess/preprocess_jamendo.py) for all the details. Here is a concise summary:

We retrieve information
from the meta data and form a 3-field `.json` file for each audio. Here are some audio-json pairs selected from the processed dataset:


#### 
<audio id="audio" controls="controls" preload="yes">
      <source id="flac" src="1.flac">
</audio><br>

```json
{
    "text": [
        "You can always count on Jus Ed to bring the no-nonsense approach to house music to its logical conclusion, and so it is on his latest release, which extends some love to an undisclosed acquaintance. The first version features Alison Crockett crooning over the whimsical piano chords and direct drum programming you would expect from the Underground Quality label boss, while the second version switches the feminine delivery for Jaymz Nylon's baritone interpretation. On the flip, Glen Thornton turns out a remix that embellishes the original with moodier keys and a more forthright groove. Rounding out the EP Ed drops a dubbed out \"Gratitude\" mix that draws on his greatest deep house strengths for a more developed trip through both vocal contributions."
    ],
    "tag": [
        "Deep House",
        "Thank You For Being A Friend (feat Jaymz Nylon)",
        "DJ Jus Ed",
        "Thank You EP"
    ],
    "original_data": {
        "title": "Juno",
        "description": "A music review webset",
        "track_title": "Thank You For Being A Friend (feat Jaymz Nylon)",
        "artist": "DJ Jus Ed",
        "album": "Thank You EP",
        "url": "https://www.juno.co.uk/MP3/SF495461-01-01-02.mp3",
        "review": "You can always count on Jus Ed to bring the no-nonsense approach to house music to its logical conclusion, and so it is on his latest release, which extends some love to an undisclosed acquaintance. The first version features Alison Crockett crooning over the whimsical piano chords and direct drum programming you would expect from the Underground Quality label boss, while the second version switches the feminine delivery for Jaymz Nylon's baritone interpretation. On the flip, Glen Thornton turns out a remix that embellishes the original with moodier keys and a more forthright groove. Rounding out the EP Ed drops a dubbed out \"Gratitude\" mix that draws on his greatest deep house strengths for a more developed trip through both vocal contributions.",
        "genre": "Deep House"
    }
}
```




### I. Json file generation principles 
-  **` text  entry`** We use review of audio as the text.
-  **` tag  entry`** We use thesong, artist and album as well as `music` and `song` as tags.
-  **` original data`** We save filename, song name, artist and album name as well as the dataset name and dataset description.

### II. Audio filtering principles
1. Keep audios with sampling rate higher than **16KHZ** and discard the rest.
2. Discard all audios failed to be read by `soundfile.read()` method or denied by FFmpeg while processing.
### III. Audio format specifications
After the preprocessing work, all audio files should be in FLAC format with sampling rate of 48KHZ. (Processed by ffmpeg).