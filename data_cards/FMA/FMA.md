# Free Music Archive (FMA) Data Card
## Dataset Overview
|Size of dataset|Number of audios|
|:----:|:-----:|
|1.0 TiB| 2 324 700|
## Data Collection

|Source|<center>Collecting Method<center>|
|:---------:|:--------|
| [FMA GitHub Repo](https://github.com/mdeff/fma)  |1.Download fma_full.zip archive and meta data archive (fma_metadata.zip) from FMA GitHUb repo 2. extract data from all archives. <br>
## Preprocessing Principles

You may refer to [preprocess_fma.py](/data_preprocess/preprocess_fma.py) for all the details. Here is a concise summary:

We retrieve information
from the meta data (fma_metadata/tracks.csv) and form a 3-field `.json` file for each audio. Here are some audio-json pairs selected from the processed dataset:


#### 
<audio id="audio" controls="controls" preload="yes">
      <source id="flac" src="1.flac">
</audio><br>

```json
{
    "text": [
        "playing song titled White Man, by Blah Blah Blah, in album Green Collection, of which the language code is en, the genre is Rock, the date created is 2008-11-26 01:53:43"
    ],
    "tag": [
        "White Man"
    ],
    "original_data": {
        "title": "FMA: A Dataset For Music Analysis",
        "description": "Free Music Archive (FMA), an open and easily accessible dataset suitable for evaluating several tasks in MIR, a field concerned with browsing, searching, and organizing large music collections.",
        "license": "MIT License",
        "filename": "000142.mp3",
        "genre": "Rock",
        "album": "Green Collection",
        "duration": 270,
        "composer": "nan",
        "date_recorded": "2008-11-26 01:53:43",
        "language_code": "en",
        "split": [
            70,
            80
        ]
    }
}
```




### I. Json file generation principles 
-  **` text  entry`** We create two dictinaries song_info and extra_info. For song info we use fields like album, from which we construct a string like `in album {album}`, for title - `titled {title}`, for artist - `by {artist}`. In extra info we include genre with sitring like `the genre is {genre}`, date of creation (`the date created is {date_recorded}`), language code of a song - `the language code is {language_code}`, for composer - `the composer is {composer}` (in case some of attributes don't exist for a particular audio, we just don't include it). Then we randomly shuffle both song_info and extra_info and join each of the lists into a string. After that we create a following template `playing song {song_info}, of which {extra_info}`.
-  **` tag  entry`** We use the song title for each audio as a tag.
-  **` original data`** We save filename, genre, album, date created, composer, language code, duration of audio, the dataset name and dataset description.

### II. Audio filtering principles
1. Keep audios with sampling rate higher than **16KHZ** and discard the rest.
2. Discard all audios failed to be read by `soundfile.read()` method or denied by FFmpeg while processing.
3. Split evry audio in 10 sec segements.
### III. Audio format specifications
After the preprocessing work, all audio files should be in FLAC format with sampling rate of 48KHZ. (Processed by ffmpeg).