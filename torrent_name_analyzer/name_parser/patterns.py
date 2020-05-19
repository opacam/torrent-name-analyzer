# -*- coding: utf-8 -*-

delimiters = r'[\.\s\-\+_\/]'
langs = (
    r'rus|(?:True)?fr(?:ench)?|e?n(?:g(?:lish)?)?|vost(?:fr)?|ita(?:liano)?|'
    r'castellano|swedish|spanish|dk|german|multi|nordic|exyu|chs|hindi|polish'
    r'|mandarin'
)
producers = 'ATVP|AMZN|NF|NICK|RED|DSNP'

season_range_pattern = (
    r'(?:Complete' + delimiters + r'*)?(?:' + delimiters
    + r'*)?(?:s(?:easons?)?)?' + delimiters
    + r'?(?:s?[0-9]{1,2}[\s]*(?:\-|(?:\s*to\s*))[\s]*s?[0-9]{1,2})(?:'
    + delimiters + r'*Complete)?'
)
episode_pattern = (
    '(?:(?:[ex]|ep)(?:[0-9]{1,2}(?:-(?:[ex]|ep)?(?:[0-9]{1,2})))|'
    '(?:[ex]|ep)([0-9]{1,2}))'
)

year_pattern = '(?:19[0-9]|20[0-2])[0-9]'
month_pattern = '0[1-9]|1[0-2]'
day_pattern = '[0-2][0-9]|3[01]'

patterns = [
    ('season', delimiters + '('  # Season description can't be at the beginning, must be after this pattern  # noqa: 501
     '' + season_range_pattern + '|'  # Describes season ranges
     '(?:Complete' + delimiters + ')?s([0-9]{1,2})(?:' + episode_pattern + ')?|'  # Describes season, optionally with complete or episode  # noqa: 501
     '([0-9]{1,2})x[0-9]{2}|'  # Describes 5x02, 12x15 type descriptions
     '(?:Complete' + delimiters + r')?Season[\. -]([0-9]{1,2})'  # Describes Season.15 type descriptions  # noqa: 501
     ')(?:' + delimiters + '|$)'),
    ('episode', '(' + episode_pattern + ')(?:[^0-9]|$)'),
    ('year', r'([\[\(]?(' + year_pattern + r')[\]\)]?)'),
    ('month', '(?:' + year_pattern + ')'
     + delimiters + '(' + month_pattern + ')'
     + delimiters + '(?:' + day_pattern + ')'
     ),
    ('day', '(?:' + year_pattern + ')' + delimiters
     + '(?:' + month_pattern + ')' + delimiters + '(' + day_pattern + ')'),
    ('resolution', '([0-9]{3,4}p|1280x720)'),
    ('quality', (r'((?:PPV\.)?[HP]DTV|CAM-RIP|(?:HD)?CAM|B[DR]Rip|(?:HD-?)?TS|'
                 r'HDRip|HDTVRip|DVDRip|DVDRIP|CamRip|(?:(?:' + producers + ')'
                 + delimiters + r'?)?(?:PPV )?W[EB]B(?:-?DL(?:Mux)?)'
                 r'?(?:Rip| DVDRip)?|BluRay|DvDScr|hdtv|telesync)')),
    ('codec', r'(xvid|[hx]\.?26[45])'),
    ('audio', (r'(MP3|DD5\.?1|Dual[\- ]Audio|LiNE|DTS|DTS5\.1|'
               r'AAC[ \.-]LC|AAC(?:(?:\.?2(?:\.0)?)?|(?:\.?5(?:\.1)?)?)|'
               r'(?:E-?)?AC-?3(?:' + delimiters + r'*?(?:2\.0|5\.1))?)')),
    ('group', '(- ?([^-]+(?:-={[^-]+-?$)?))$'),
    ('region', 'R[0-9]'),
    ('extended', '(EXTENDED(:?.CUT)?)'),
    ('hardcoded', 'HC'),
    ('proper', 'PROPER'),
    ('repack', 'REPACK'),
    ('container', '(MKV|AVI|MP4)'),
    ('widescreen', 'WS'),
    ('website', r'^(\[ ?([^\]]+?) ?\])'),
    ('subtitles', r'((?:(?:' + langs + r'|e-?)[\-\s.]*)*subs?)'),
    ('language', r'((?:(?:' + langs + ')' + delimiters
     + r'*)+)(?!(?:[\-\s.]*(?:' + langs + r')*)+[\-\s.]?subs)'),
    ('sbs', '(?:Half-)?SBS'),
    ('unrated', 'UNRATED'),
    ('size', r'(\d+(?:\.\d+)?(?:GB|MB))'),
    ('bitDepth', '(?:8|10)bit'),
    ('3d', '3D'),
    ('internal', 'iNTERNAL'),
    ('readnfo', 'READNFO')
]

types = {
    'season': 'integer',
    'episode': 'integer',
    'year': 'integer',
    'month': 'integer',
    'day': 'integer',
    'extended': 'boolean',
    'hardcoded': 'boolean',
    'proper': 'boolean',
    'repack': 'boolean',
    'widescreen': 'boolean',
    'unrated': 'boolean',
    '3d': 'boolean',
    'internal': 'boolean',
    'readnfo': 'boolean'
}
