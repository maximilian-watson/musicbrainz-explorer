"""CLI commands using Click."""
import click
from ..api.client import MusicBrainzClient

@click.group()
def cli():
    """MusicBrainz Explorer - Analyze music artist data."""
    pass

@cli.command()
@click.argument('mbid')
def get_artist(mbid):
    """Get information about an artist by MusicBrainz ID."""
    client = MusicBrainzClient("MusicBrainzExplorer", "2.max.leo.watson@gmail.com")
    artist = client.get_artist(mbid)
    
    if artist:
        click.echo(f"🎵 Artist: {artist.name}")
        click.echo(f"📍 Country: {artist.country}")
        click.echo(f"🎤 Type: {artist.type}")
        click.echo("✅ Success!")
    else:
        click.echo("❌ Artist not found or error occurred.")

def main():
    """Main entry point for CLI."""
    cli()

if __name__ == '__main__':
    main()