from os import getcwd
from re import match as regex_match

from typer import run, Argument, Option, Exit
from typing_extensions import Annotated

from rich import print as rprint
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.progress import Progress

from pytube import YouTube, Playlist

__app_name__ = 'YouTube to MP3 CLI'
__version__ = '0.0.1'


def _is_playlist(url: str) -> bool:
    pattern = r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.*(?:\?|\&)list=([^&]+)'

    return regex_match(pattern, url) is not None


def _escape_filename(filename: str) -> str:
    char_list = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', ' ']

    for char in char_list:
        filename = filename.replace(char, '_')

    return filename


def _create_progress_display(is_playlist: bool = False) -> (Table, Progress, Progress):
    playlist_progress = Progress()
    video_progress = Progress()

    # Create progress bars display
    progress_table = Table.grid()
    progress_table.add_column(justify='left')

    if is_playlist:
        progress_table.add_row(Panel.fit(playlist_progress, title='Playlist', border_style='green', padding=(0, 2)))

    progress_table.add_row(Panel.fit(video_progress, title='Video(s)', border_style='yellow', padding=(1, 2)))

    return progress_table, playlist_progress, video_progress


def _download_playlist(url: str, output: str) -> None:
    if not _is_playlist(url):
        rprint('[bold red]Error:[/bold red] Playlist URL is invalid')
        raise Exit(code=1)

    playlist = Playlist(url)

    output_dir = output + f'\\{_escape_filename(playlist.title)}'
    rprint(f'[bold red]Output directory:[/bold red] {output_dir}')

    # Progress bar display
    progress_table, playlist_progress, video_progress = _create_progress_display(is_playlist=True)

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


def _download_video(url: str, output: str) -> None:
    video = YouTube(url)
    audio = video.streams.get_audio_only()

    output_dir = output + f'\\{_escape_filename(video.title)}'
    rprint(f'[bold red]Output directory:[/bold red] {output_dir}')

    # Progress bar display
    progress_table, _, video_progress = _create_progress_display()

    video_task = video_progress.add_task(f'[bold yellow]{video.title}', total=audio.filesize)

    with Live(progress_table):
        # Callbacks
        video.register_on_progress_callback(
            lambda stream, chunk, bytes_remaining: video_progress.update(video_task, advance=len(chunk))
        )

        # Download audio
        audio.download(output_path=output, filename=f'{video.title}.mp3', skip_existing=False)


# CLI
def _version_callback(value: bool):
    if value:
        rprint(f'{__app_name__} [bold green]v{__version__}[/bold green]')
        raise Exit()


def main(
        url: Annotated[str, Argument(help='YouTube video or playlist URL', show_default=False)],
        output: Annotated[str, Argument(help='Output directory')] = f'{getcwd()}\\output',
        download_playlist: Annotated[bool, Option('--playlist', '-p', help='Download playlist')] = False,
        version: Annotated[bool, Option('--version', '-v', help='Show version', callback=_version_callback)] = False,
) -> None:
    """
    Convert a YouTube video or playlist to mp3 and download it.
    """
    _download_playlist(url, output) if download_playlist else _download_video(url, output)


if __name__ == '__main__':
    run(main)
