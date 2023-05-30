# youtube-to-mp3-cli

A simple CLI to download and convert YouTube videos to MP3 files.

## Compiling

### Requirements

- [Python 3.6+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) (optional)

### Steps

1. Clone or download the repository
2. Create a virtual environment and activate it (optional) - [Guide](https://docs.python.org/3/library/venv.html)
3. Install the dependencies - `pip install -r requirements.txt`
4. View the available options - `python src/main.py --help`

## Usage

```bash
python src/main.py [OPTIONS] URL [OUTPUT]

Options:
  -p, --playlist  Download a playlist
  -v, --version   Show the version and exit.
  --help          Show this message and exit.
```

### Downloading a single video

```bash
python src/main.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### Downloading a single video at a specific location

```bash
python src/main.py https://www.youtube.com/watch?v=dQw4w9WgXcQ C:\Users\user\Music
```

### Downloading playlist

```bash
python src/main.py -p https://www.youtube.com/playlist?list=PLFgquLnL59alCl_2TQvOiD5Vgm1hCaGSI
```

### Downloading playlist at a specific location

```bash
python src/main.py -p https://www.youtube.com/playlist?list=PLFgquLnL59alCl_2TQvOiD5Vgm1hCaGSI C:\Users\user\Music
```
