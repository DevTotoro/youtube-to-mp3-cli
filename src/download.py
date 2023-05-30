from typer import Exit

from rich import print as rprint
from rich.live import Live

from utils import is_playlist, escape_filename, create_progress_display


def download_playlist(url: str, output: str) -> None:
    if not is_playlist(url):
        rprint('[bold red]Error:[/bold red] Playlist URL is invalid')
        raise Exit(code=1)

    from pytube import Playlist
    playlist = Playlist(url)

    output_dir = output + f'\\{escape_filename(playlist.title)}'
    rprint(f'[bold red]Output directory:[/bold red] {output_dir}')

    # Progress bar display
    progress_table, playlist_progress, video_progress = create_progress_display(download_playlist=True)

    # Create playlist task
    playlist_task = playlist_progress.add_task(f'[bold green]{playlist.title}', total=len(playlist))

    with Live(progress_table):
        for video in playlist.videos:
            # Get audio stream
            audio = video.streams.get_audio_only()

            # Create progress task
            video_task = video_progress.add_task(f'[bold yellow]{video.title}', total=audio.filesize)

            # Callbacks
            video.register_on_progress_callback(
                lambda stream, chunk, bytes_remaining: video_progress.update(video_task, advance=len(chunk))
            )
            video.register_on_complete_callback(lambda stream, file_path: playlist_progress.advance(playlist_task))

            # Download audio
            audio.download(output_path=output_dir, filename=f'{video.title}.mp3', skip_existing=False)


def download_video(url: str, output: str) -> None:
    from pytube import YouTube
    video = YouTube(url)
    audio = video.streams.get_audio_only()

    output_dir = output + f'\\{escape_filename(video.title)}'
    rprint(f'[bold red]Output directory:[/bold red] {output_dir}')

    # Progress bar display
    progress_table, _, video_progress = create_progress_display()

    video_task = video_progress.add_task(f'[bold yellow]{video.title}', total=audio.filesize)

    with Live(progress_table):
        # Callbacks
        video.register_on_progress_callback(
            lambda stream, chunk, bytes_remaining: video_progress.update(video_task, advance=len(chunk))
        )

        # Download audio
        audio.download(output_path=output, filename=f'{video.title}.mp3', skip_existing=False)
