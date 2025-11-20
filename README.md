# musicbrainz-explorer

A python toolkit for music and data analysis.

## Installation

git clone https://github.com/maximilian-watson/musicbrainz-explorer.git
cd musicbrainz-explorer
poetry install

## Usage

# Get artist info and save to database

poetry run mbz get-artist "artist-mbid" --save

# List all artists in your collection

poetry run mbz list-artists

# See most popular tags

poetry run mbz popular-tags

# Find artists by country

poetry run mbz artists-by-country "GB"

# Reset database (deletes all data)

poetry run mbz reset-db

# Help

poetry run mbz --help
