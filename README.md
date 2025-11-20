# Musicbrainz Explorer

A Python toolkit for music and data analysis.

## Installation

```bash
git clone https://github.com/maximilian-watson/musicbrainz-explorer.git
cd musicbrainz-explorer
poetry install
```

## Usage

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
