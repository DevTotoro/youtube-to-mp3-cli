from re import match as regex_match

from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress


def is_playlist(url: str) -> bool:
    pattern = r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.*(?:\?|\&)list=([^&]+)'

    return regex_match(pattern, url) is not None


def escape_filename(filename: str) -> str:
    char_list = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', ' ']

    for char in char_list:
        filename = filename.replace(char, '_')

    return filename


def create_progress_display(download_playlist: bool = False) -> (Table, Progress, Progress):
    playlist_progress = Progress()
    video_progress = Progress()

    # Create progress bars display
    progress_table = Table.grid()
    progress_table.add_column(justify='left')

    if download_playlist:
        progress_table.add_row(Panel.fit(playlist_progress, title='Playlist', border_style='green', padding=(0, 2)))

    progress_table.add_row(Panel.fit(video_progress, title='Video(s)', border_style='yellow', padding=(1, 2)))

    return progress_table, playlist_progress, video_progress
