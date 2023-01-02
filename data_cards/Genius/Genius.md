# Genius Data Card
## Dataset Overview
|Size of dataset|Number of audios|Duration|
|:----:|:-----:|:-----:|
|1.9 TB| 87135|5748 hrs|
## Data Collection

|Source|<center>Collecting Method<center>|
|:---------:|:--------
| [Genius Website](https://genius.com/#top-songs)  | Scrape all the metadata from the Genius website (audio links, reviews, song title, artist name). Download audio from audio lins. <br>
## Preprocessing Principles

You may refer to [preprocess_genius.py](/data_preprocess/preprocess_genius.py) for all the details. Here is a concise summary:

We retrieve information
from the meta data and form a 3-field `.json` file for each audio. Here are some audio-json pairs selected from the processed dataset:


#### 
<audio id="audio" controls="controls" preload="yes">
      <source id="flac" src="1.flac">
</audio><br>

```json
{
    "text": [
        "The Twelve Days of Christmas is an English Christmas carol that enumerates each day by the gifts given on each of the twelve days of Christmas.\nFrederic Austin was known to popularize the arrangement of the song we know today in 1909."
    ],
    "tag": [
        "12 days of christmas lyrics",
        "twelve days of christmas lyrics",
        "tweleve days song",
        "Twelve Days Of Christmas (Holiday)",
        "Christmas song",
        "Christmas carols",
        "popular Christmas songs",
        "christmas songs",
        "merry Christmas",
        "christmas songs with lyrics",
        "christmas songs lyrics",
        "12 days of christmas",
        "telve day of xmas",
        "song 12 day christmas",
        "12 christmas",
        "12 xmas",
        "12 xmas song",
        "xmas 12",
        "christmas 12 days",
        "christmas songs and carols"
    ],
    "original_data": {
        "title": "Genius",
        "description": "A lyrics & music review website",
        "song": "The Twelve Days of Christmas",
        "artist": "Christmas Songs",
        "about": "The Twelve Days of Christmas is an English Christmas carol that enumerates each day by the gifts given on each of the twelve days of Christmas.\nFrederic Austin was known to popularize the arrangement of the song we know today in 1909.",
        "url": "http://www.youtube.com/watch?v=oyEyMjdD2uk"
    }
}
```




### I. Json file generation principles 
-  **` text  entry`** We use review of audio as the text.
-  **` tag  entry`** We use tags from YouTube.
-  **` original data`** We save filename, song name, artist and album name as well as the dataset name and dataset description.

### II. Audio filtering principles
1. Keep audios with sampling rate higher than **16KHZ** and discard the rest.
2. Discard all audios failed to be read by `soundfile.read()` method or denied by FFmpeg while processing.
### III. Audio format specifications
After the preprocessing work, all audio files should be in FLAC format with sampling rate of 48KHZ. (Processed by ffmpeg).