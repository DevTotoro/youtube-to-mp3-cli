from os import getcwd

from typer import Argument, Option, Exit
from typing_extensions import Annotated

from rich import print as rprint

from download import download_playlist, download_video

__app_name__ = 'YouTube to MP3 CLI'
__version__ = '0.0.1'


def _version_callback(value: bool):
    if value:
        rprint(f'{__app_name__} [bold green]v{__version__}[/bold green]')
        raise Exit()


def main(
        url: Annotated[str, Argument(help='YouTube video or playlist URL', show_default=False)],
        output: Annotated[str, Argument(help='Output directory')] = f'{getcwd()}\\output',
        playlist: Annotated[bool, Option('--playlist', '-p', help='Download playlist')] = False,
        version: Annotated[bool, Option('--version', '-v', help='Show version', callback=_version_callback)] = False,
) -> None:
    """
    Convert a YouTube video or playlist to mp3 and download it.
    """
    download_playlist(url, output) if playlist else download_video(url, output)
