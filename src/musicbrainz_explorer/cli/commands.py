"""Enhanced CLI commands with database and service layer integration."""
import click

from ..services.artist_service import ArtistService
from ..database.manager import db_manager

@click.group()
def cli():
    """MusicBrainz Explorer - Analyze music artist data."""
    # Initialize database on startup
    db_manager.create_tables()

@cli.command()
@click.argument('mbid')
@click.option('--save', is_flag=True, help='Save artist to database')
def get_artist(mbid, save):
    """Get information about an artist by MusicBrainz ID."""
    if save:
        # Use service layer to fetch and store
        service = ArtistService()
        artist = service.fetch_and_store_artist(mbid)
        
        if artist:
            click.echo(f"💾 Saved to database: {artist.name}")
            click.echo(f"📍 Country: {artist.country}")
            click.echo(f"🎤 Type: {artist.type}")
            if artist.tags:
                click.echo(f"🏷️  Tags: {', '.join(artist.tags)}")
        else:
            click.echo("❌ Failed to fetch and save artist")
    else:
        # Original API-only behavior
        from ..api.client import MusicBrainzClient
        client = MusicBrainzClient("MusicBrainzExplorer", "test@example.com")
        artist = client.get_artist(mbid)
        
        if artist:
            click.echo(f"🎵 Artist: {artist.name}")
            click.echo(f"📍 Country: {artist.country}")
            click.echo(f"🎤 Type: {artist.type}")
            click.echo("✅ Success! (Use --save to store in database)")
        else:
            click.echo("❌ Artist not found or error occurred.")

@cli.command()
def list_artists():
    """List all artists in the database."""
    service = ArtistService()
    artists = service.get_stored_artists()
    
    if artists:
        click.echo("📋 Artists in database:")
        for artist in artists:
            tags_display = f" - Tags: {', '.join(artist.tags)}" if artist.tags else ""
            click.echo(f"  • {artist.name} ({artist.country}){tags_display}")
        click.echo(f"\nTotal: {len(artists)} artists")
    else:
        click.echo("💾 No artists in database yet. Use 'get-artist --save' to add some.")

@cli.command()
@click.option('--limit', default=10, help='Number of top tags to show')
def popular_tags(limit):
    """Show the most popular tags in the database."""
    service = ArtistService()
    tags = service.get_popular_tags(limit)
    
    if tags:
        click.echo("🏷️  Most popular tags:")
        for i, tag in enumerate(tags, 1):
            click.echo(f"  {i}. {tag['name']} ({tag['count']} artists)")
    else:
        click.echo("📊 No tags in database yet. Add artists with 'get-artist --save'")

@cli.command()
@click.argument('country')
def artists_by_country(country):
    """List artists from a specific country."""
    service = ArtistService()
    artists = service.get_artists_by_country(country)
    
    if artists:
        click.echo(f"🇺🇸 Artists from {country}:")
        for artist in artists:
            click.echo(f"  • {artist.name} ({artist.type})")
        click.echo(f"\nTotal: {len(artists)} artists from {country}")
    else:
        click.echo(f"❌ No artists found from {country}")

@cli.command()
@click.confirmation_option(prompt='Are you sure you want to reset the database? This will delete all data!')
def reset_db():
    """Reset the database (delete all data)."""
    from ..models.database import Base
    
    try:
        # Drop all tables and recreate
        Base.metadata.drop_all(bind=db_manager.engine)
        Base.metadata.create_all(bind=db_manager.engine)
        click.echo("✅ Database reset successfully!")
    except Exception as e:
        click.echo(f"❌ Error resetting database: {e}")

def main():
    """Main entry point for CLI."""
    cli()