# Changelog


## [Unreleased](https://github.com/opacam/torrent-name-analyzer/tree/HEAD) (2020-05-25)
[Full Changelog](https://github.com/opacam/torrent-name-analyzer/compare/v2020.05.19...HEAD)

**General:**

- Add more information to `pyproject.toml`
- Add project files: `CONTRIBUTING.md` & CHANGELOG.md

**Fixed bugs:**

- Fix project version at `pyproject.toml`
- Fix `LICENSE.md` detection for github interface
- Fix badge's link for `LICENSE.md`

## [v2020.05.19](https://github.com/opacam/torrent-name-analyzer/tree/v2020.05.19) (2020-05-19)
[Full Changelog](https://github.com/opacam/torrent-name-analyzer/compare/d3dbf4c7dcc30990b10e88e93596ca1e8afa2c8b...v2020.05.19)

**General:**

- Add CI tests via github actions
- Implement a web server via gunicorn
- Add Dockerfile
- Add tests for the REST API
- Add API documentation via swagger file
- Build a REST API on top of previous work
- Make use of poetry to manage project dependencies
- Limit to Python 3.6+
- Move/rename old module `parse_torrent_name` into a sub module `name_parser`

**Core - name_parser:**

- move some patterns to raw strings
- sort imports
- split long lines (included inline comments)
- remove redundant character escape from regex expressions
- remove object inheritance (no need for python3)
- Format parse.py and patterns.py (with black)

**Fixed bugs:**

- Fix `name_parser.parse`: avoid detect `codec` or `quality` as part of `group`
- Fix `name_parser.parse`: avoid empty encoder

## [Unreleased - Giorgio Momigliano](https://github.com/opacam/torrent-name-analyzer/tree/d3dbf4c7dcc30990b10e88e93596ca1e8afa2c8b)
[Full Changelog](https://github.com/opacam/torrent-name-analyzer/compare/39ba2f0dcded7e222ca948a5021fc501167f2fe3...d3dbf4c7dcc30990b10e88e93596ca1e8afa2c8b)

**General:**

- Add matching for `episodeName`
- Update installation instructions and package info
- Adds `internal` field
- Cleans up excess
- Adds to `quality` field; cleans up excess; adds `internal` field
- Some WEB rips now come directly off some distributors, so we may have
  AMZN WEBRip rather than just WEBRip; we now include these in `quality`.
- The `excess` field contained multi-language, multi-episode, and
  multi-subtitles info that had been already parsed. They are now
  correctly removed.
- Added a boolean field for `internal` releases.
- Added 'Agents of S.H.I.E.L.D.' exception, as normally the dots would
  be replaced by spaces.
- Renames bit-depth field to bitDepth 
- Arranges test outputs' keys alphabetically Largely due to semi-automation
  of how new tests are being added
- Adds some encoders/groups to test against
- Improves quality & audio matches
- Adds multi-episode support and bit-depth field
- Improved subtitles match
- Added support for full YYYY.MM.DD dates, usually useful for daily shows
  (e.g. late night shows)
- Improved multi-season parsing & support
- Expanded support for subtitles and added more languages
- Added tests for media with year in the name and no release year
- Added exceptions list where manual fixes to media with known issues can be listed
- Added test for AAC5.1 and 2020 release dates
- Added support for AAC5/AAC5.1
- Now supports release years for the 2020s
- Now correctly handles titles with a year in them
- Now accepts single-digit episode descriptions, e.g. S1E5
- Added support for AAC2 audio
- Added hindi in language pattern
- Added multi-language support
- Added test for "Complete S02"-type strings
- Added support for "Complete.S15" type strings
- Added support for dash characters as season delimiter
- Added support for parsing "Season X" & "Season.X" in full-season torrents
- Ignore PyCharm config files

**Fixed bugs:**

- Fixed trailing whitespace breaking title parsing
- Superfluous information now mostly removed from excess field
- Multiple matches, instead of all but the first being ignored, now remove
  themselves from excess

## [Unreleased - Roi Dayan](https://github.com/opacam/torrent-name-analyzer/tree/39ba2f0dcded7e222ca948a5021fc501167f2fe3)
[Full Changelog](https://github.com/opacam/torrent-name-analyzer/compare/681d95828a66a563d8450c349d6513965dc99c4d...39ba2f0dcded7e222ca948a5021fc501167f2fe3)

**General:**

- Add language match nordic and a test
- Strip bt sites tag from group name
- Strip container string from group name
- Add support for multi season

**Fixed bugs:**

- Fix AAC-LC matching

## [Unreleased - Divij Bindlish](https://github.com/opacam/torrent-name-analyzer/tree/681d95828a66a563d8450c349d6513965dc99c4d)
[Full Changelog](https://github.com/opacam/torrent-name-analyzer/compare/1ee4f01566bf67019ffa43036c1b70f548175eee...681d95828a66a563d8450c349d6513965dc99c4d)

**General:**

- Implement python port of [Jānis](https://github.com/jzjzjzj) awesome [library](https://github.com/jzjzjzj/parse-torrent-name) written in javascript.

**Closed issues:**

- Test with Hyphen in the name is broken [\#21](https://github.com/divijbindlish/parse-torrent-name/issues/21)
- Python 3 compatibility [\#16](https://github.com/divijbindlish/parse-torrent-name/issues/16)
- Question about the field `group` and `excess` [\#15](https://github.com/divijbindlish/parse-torrent-name/issues/15)

**Merged pull requests:**

- URL fix [\#11](https://github.com/divijbindlish/parse-torrent-name/pull/11) ([tijptjik](https://github.com/tijptjik))
- Fix setup.py README read to work on Windows [\#9](https://github.com/divijbindlish/parse-torrent-name/pull/9) ([blakev](https://github.com/blakev))
- Fixes and more patterns [\#7](https://github.com/divijbindlish/parse-torrent-name/pull/7) ([roidayan](https://github.com/roidayan))
- Updates to PTN [\#6](https://github.com/divijbindlish/parse-torrent-name/pull/6) ([roidayan](https://github.com/roidayan))
- Match regex with word boundaries [\#4](https://github.com/divijbindlish/parse-torrent-name/pull/4) ([roidayan](https://github.com/roidayan))
- Parse sbs [\#3](https://github.com/divijbindlish/parse-torrent-name/pull/3) ([roidayan](https://github.com/roidayan))
- Torrent name caused PTN to crash. [\#1](https://github.com/divijbindlish/parse-torrent-name/pull/1) ([davidvuong](https://github.com/davidvuong))
