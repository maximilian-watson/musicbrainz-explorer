# Musicbrainz Explorer

A Python command-line toolkit for retrieving, storing and analysing music artist data from the MusicBrainz API.

**What to expect:**

- ✅ First request usually works
- ❌ Subsequent requests may fail with SSL errors
- ⏰ Waiting 5-10 minutes often resolves the block

## Features

- Retrieve artist metadata from MusicBrainz
- Save artist data to a local database
- List stored artists
- Analyse popular tags
- Filter artists by country
- Reset local data through the CLI

## Installation

```bash
git clone https://github.com/maximilian-watson/musicbrainz-explorer.git
cd musicbrainz-explorer
poetry install
```

### Requirements

- Python 3.10+
- Poetry

### Testing

```
poetry run pytest
```

## Usage

Getting an MBID (MusicBrainz ID)

To get the MBID for an artist, go to the MusicBrainz website https://musicbrainz.org and search for the artist. Open their page, then copy the final part of the URL.

For example, from this URL:

```bash
https://musicbrainz.org/artist/2d2ca38f-a8f8-4744-973a-d25275e5d3db
```

You should copy only this part:

```bash
2d2ca38f-a8f8-4744-973a-d25275e5d3db
```

### Get artist info and save to the database

```bash
poetry run mbz get-artist "artist-mbid" --save
```

### List all artists in your collection

```bash
poetry run mbz list-artists
```

### See most popular tags

```bash
poetry run mbz popular-tags
```

### Find artists by country

```bash
poetry run mbz artists-by-country "GB"
```

### Reset the database (deletes all data)

```bash
poetry run mbz reset-db
```

## Help

```bash
poetry run mbz --help
```

## Known Limitations

MusicBrainz protects their API with aggressive rate limiting for unregistered applications:
