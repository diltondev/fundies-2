# Lab: Artist Discography Explorer

In this lab you will build a command-line tool that searches for a music artist, fetches their albums, and displays the full track listing using Apple's [iTunes Search API](https://performance-partners.apple.com/search-api).

You are already familiar with `requests` and calling `.json()` to get back Python dictionaries. In this lab you will go a step further: instead of passing raw dictionaries around your application, you will map API responses into proper Python objects using `from_dict` class methods. This class method will accept a dictionary and return a new instance of a class using relevant keys, this is a common pattern in real-world codebases and gives you control over attribute names, default values, and display formatting.

The files in this lab are:

- `models.py`: implement this first
- `itunes_api.py`: implement this second
- `discography.py`: implement this third
- `main.py`: run this once all three parts are done

## Part 1: Models

`models.py` already provides a complete `Track` class as an example. It uses a `from_dict` classmethod to construct an instance from an API dictionary, and a `duration_formatted` property to convert milliseconds to `M:SS`.

### Step 1

Implement `Artist`. It should store `artist_id`, `name`, and `genre`. The `from_dict` classmethod should map from:

| JSON Key             | Attribute   | Type  |
|----------------------|-------------|-------|
| `"artistId"`         | `artist_id` | `int` |
| `"artistName"`       | `name`      | `str` |
| `"primaryGenreName"` | `genre`     | `str` |

> [!TIP]
> `genre` should default to `"Unknown"` if the key is missing.

`__str__` should return:

```
Bicep (Electronic)
```

### Step 2

Implement `Album`. It should store `collection_id`, `name`, `artist_name`, `track_count`, `release_year`, `genre`, and `artwork_url`. It also needs a `tracks` attribute initialised to an empty list.

The `from_dict` classmethod should map from:

| JSON Key             | Attribute       | Type  |
|----------------------|-----------------|-------|
| `"collectionId"`     | `collection_id` | `int` |
| `"collectionName"`   | `name`          | `str` |
| `"artistName"`       | `artist_name`   | `str` |
| `"trackCount"`       | `track_count`   | `int` |
| `"releaseDate"`      | `release_year`  | `int` |
| `"primaryGenreName"` | `genre`         | `str` |
| `"artworkUrl100"`    | `artwork_url`   | `str` |

> [!TIP]
> Extract the year from `releaseDate` by taking the first 4 characters and converting to int, e.g. `int("2017-09-01T07:00:00Z"[:4])` gives `2017`.

`__str__` should return:

```
Bicep (2017) - 12 tracks
```

## Part 2: API Client

`itunes_api.py` provides the class structure and constants. You need to implement three methods.

### Step 1 - Searching for Artists
The search endpoint can be accessed using by making a GET request to the following URL:

```raw
GET https://itunes.apple.com/search
```

It accepts the following parameters:

| Parameter | Required | Description                                    | Example       |
|-----------|----------|------------------------------------------------|---------------|
| `term`    | Yes      | Search text (spaces become `+`)                | `bicep`       |
| `country` | Yes      | Two-letter country code                        | `GB`          |
| `entity`  | No       | Type of result: `musicArtist`, `album`, `song` | `musicArtist` |
| `limit`   | No       | Max results, 1–200 (default 50)                | `5`           |

Example request search for artists matching "bicep":

```
GET https://itunes.apple.com/search?term=bicep&entity=musicArtist&country=GB&limit=5
```

Example response:

```json
{
  "resultCount": 1,
  "results": [
    {
      "wrapperType": "artist",
      "artistId": 406148755,
      "artistName": "Bicep",
      "primaryGenreName": "Electronic",
      "artistLinkUrl": "https://music.apple.com/gb/artist/bicep/406148755"
    }
  ]
}
```

Implement `search_artist`. Use `requests.get()` to call the search endpoint with `entity=musicArtist`. Parse the JSON and return a list of `Artist` objects from the `results` key.

Hint for making requests:

```python
response = requests.get(url, params={"term": term, "country": "GB"}, timeout=10)
response.raise_for_status()
data = response.json()
```

You will also need to add the following parameters to the request, the `country` is a necessary field for the API:

``` python
params = {
    "term": term,
    "entity": "musicArtist",
    "country": COUNTRY,
    "limit": limit,
},
```

> [!TIP]
> Remember that artist results returned from the API are inside the `"results"` key after you convert them to JSON.

### Step 2 - Album Lookup
Implement `get_albums` by calling the lookup endpoint with the artist's ID and `entity=album`. Filter results to only those where `wrapperType == "collection"` and return a list of `Album` objects.

Use this to fetch related content by a known ID (e.g. an artist's albums, or an album's tracks) from the lookup endpoint.

```
GET https://itunes.apple.com/lookup
```

| Parameter | Required | Description                           | Example     |
|-----------|----------|---------------------------------------|-------------|
| `id`      | Yes      | An iTunes ID (artist or collection)   | `406148755` |
| `entity`  | No       | Related content type: `album`, `song` | `album`     |
| `country` | Yes      | Two-letter country code               | `GB`        |
| `limit`   | No       | Max results, 1–200                    | `50`        |

Example request to fetch albums for artist 406148755:

```
GET https://itunes.apple.com/lookup?id=406148755&entity=album&country=GB
```

> [!NOTE]
> The first item in `results` key is always the parent entity (the artist). Albums start from index 1. Filter the returned list for elements where `wrapperType` is `"collection"` to get only the albums.

Example album object in the response:

```json
{
  "wrapperType": "collection",
  "collectionId": 1262692855,
  "collectionName": "Bicep",
  "artistName": "Bicep",
  "trackCount": 12,
  "releaseDate": "2017-09-01T07:00:00Z",
  "primaryGenreName": "Electronic",
  "artworkUrl100": "https://is1-ssl.mzstatic.com/.../100x100bb.jpg"
}
```

### Step 3

Implement `get_tracks`. Same pattern as `get_albums` but with a `collectionId` and `entity=song`.

The same pattern applies when looking up tracks for an album: pass the `collectionId` as `id` and `entity=song`. The first result is the album itself, filter by `wrapperType == "track"`.

Example track object:

```json
{
  "wrapperType": "track",
  "trackName": "Glue",
  "trackNumber": 4,
  "trackTimeMillis": 243120,
  "previewUrl": "https://audio-ssl.itunes.apple.com/.../mzaf_abc123.m4a"
}
```

## Part 3: Discography
`discography.py` provides the Discography class with `__init__` already implemented. This class brings everything together: it holds an `Artist` and their list of `Album` objects, fetches the tracks for each album, and displays the complete discography.


### Step 1
Implement load_all_tracks. This method receives an `ITunesAPI` instance as a parameter. It should loop through `self.albums` and, for each album, call `api.get_tracks()` passing the album's `collection_id`.

Assign the returned list of `Track` objects to `album.tracks`. Print a message for each album as it loads, and add a `time.sleep(3)` between each request to respect the API rate limit.

The API allows roughly 20 requests per minute. Use `time.sleep(3)` between each request, for example:

```python
import time

for album in self.albums:
    # Fetch tracks for album then wait three seconds after each album
    time.sleep(3)
```

### Step 2
Implement `display`. This method should print every album followed by its track listing. For each album print the album using its `__str__`, then print each track indented with its track number, name, and formatted duration. See the expected output below for the exact format.

## Running the Finished System

```bash
uv run python main.py
```

Expected output (example):

```
Enter artist name: bicep

Search results:
  1. Bicep (Electronic)

Select an artist [1]: 1

Albums for Bicep:
  1. Bicep (2017) - 12 tracks
  2. Isles (2021) - 10 tracks

Loading tracks for all albums...
  Loading tracks for "Bicep"...
  Loading tracks for "Isles"...

Bicep (2017) - 12 tracks
   1. Foreword                    0:26
   2. Orca                        5:19
   3. Kites                       4:30
   4. Glue                        4:03
   ...

Isles (2021) - 10 tracks
   1. Atlas                       5:05
   2. Cazenove                    4:34
   3. Apricots                    5:02
   4. Saku                        4:45
   ...
```

## Submission

1. Run the linter: `uv run ruff check`
2. Format your code: `uv run ruff format`
3. Commit and push to GitHub
4. Submit your repository link on Canvas
