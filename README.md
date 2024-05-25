# YaCy Bookmark Importer

Import bookmarks from Netscape style bookmarks HTML files to YaCy.

The script iterates through the bookmarks and sends each URL to YaCy's crawler.

## Install requirements

```
pip install -r requirements.txt
```

## How to run

```
python3 yacy_bookmark_importer.py --file bookmarks.html
```