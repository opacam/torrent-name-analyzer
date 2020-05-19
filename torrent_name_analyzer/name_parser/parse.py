#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from .patterns import patterns, types, exceptions, delimiters, episode_pattern


class PTN(object):
    def _escape_regex(self, string):
        return re.sub('[\-\[\]{}()*+?.,\\\^$|#\s]', '\\$&', string)

    def __init__(self):
        self.torrent = None
        self.excess_raw = None
        self.group_raw = None
        self.start = None
        self.end = None
        self.title_raw = None
        self.parts = None

    def _part(self, name, match, raw, clean):
        # The main core instructuions
        self.parts[name] = clean

        if len(match) != 0:
            # The instructions for extracting title
            index = self.torrent['name'].find(match[0])
            if index == 0:
                self.start = len(match[0])
            elif self.end is None or index < self.end:
                self.end = index

        if name != 'excess':
            # The instructions for adding excess
            if name == 'group':
                self.group_raw = raw
            if raw is not None:
                self.excess_raw = self.excess_raw.replace(raw, '')

    @staticmethod
    def _get_pattern(pattern):
        return [p[1] for p in patterns if p[0] == pattern][0]

    @staticmethod
    def _clean_string(string):
        clean = re.sub('^ -', '', string)
        if clean.find(' ') == -1 and clean.find('.') != -1:
            clean = re.sub('\.', ' ', clean)
        clean = re.sub('_', ' ', clean)
        clean = re.sub('([\[\(_]|- )$', '', clean).strip()
        clean = clean.strip(' _-')

        return clean

    def parse(self, name):
        name = name.strip()
        self.parts = {}
        self.torrent = {'name': name}
        self.excess_raw = name
        self.group_raw = ''
        self.start = 0
        self.end = None
        self.title_raw = None

        for key, pattern in patterns:
            if key not in ('season', 'episode', 'episodeName', 'website'):
                pattern = r'\b%s\b' % pattern

            clean_name = re.sub('_', ' ', self.torrent['name'])
            match = re.findall(pattern, clean_name, re.IGNORECASE)
            if len(match) == 0:
                continue

            index = {}

            # With multiple matches, we will usually want to use the first match.
            # For 'year', we instead use the last instance of a year match since,
            # if a title includes a year, we don't want to use this for the year field.
            match_index = 0
            if key == 'year':
                match_index = -1

            if isinstance(match[match_index], tuple):
                match = list(match[match_index])
            if len(match) > 1:
                index['raw'] = 0
                index['clean'] = 0
                # for season we might have it in index 1 or index 2
                # i.e. "5x09"
                for i in range(1, len(match)):
                    if match[i]:
                        index['clean'] = i
                        break
            else:
                index['raw'] = 0
                index['clean'] = 0

            # patterns for multiseason/episode make the range, and only the range, appear in match[0]
            if (key == 'season' or key == 'episode') and index['clean'] == 0:
                # handle multi season/episode
                # i.e. S01-S09
                m = re.findall('[0-9]+', match[0])
                if m:
                    clean = list(range(int(m[0]), int(m[1])+1))
            elif key == 'language':
                # handle multi language
                m = re.split('{}+'.format(delimiters), match[0])
                clean = list(filter(None, m))
                if len(clean) == 1:
                    clean = clean[0]
            elif key in types.keys() and types[key] == 'boolean':
                clean = True
            else:
                clean = match[index['clean']]
                if key in types.keys() and types[key] == 'integer':
                    clean = int(clean)

            # Codec, quality and subtitles matches can interfere with group matching,
            # so we do this later as a special case.
            if key == 'group':
                if (re.search(self._get_pattern('codec'), clean, re.IGNORECASE) or
                    re.search(self._get_pattern('quality'), clean, re.IGNORECASE) or
                    re.search(self._get_pattern('subtitles'), clean, re.IGNORECASE)):
                    continue

            self._part(key, match, match[index['raw']], clean)

        # Start process for title
        raw = self.torrent['name']
        if self.end is not None:
            raw = raw[self.start:self.end].split('(')[0]
        clean = self._clean_string(raw)

        self._part('title', [], raw, clean)

        # Considerations for results that are known to cause issues, such
        # as media with years in them but without a release year.
        for exception in exceptions:
            incorrect_key, incorrect_value = exception['incorrect_parse']
            if self.parts['title'] == exception['parsed_title'] \
              and self.parts[incorrect_key] == incorrect_value:
                self.parts.pop(incorrect_key)
                self.parts['title'] = exception['actual_title']

        # Start process for end
        clean = re.sub('(^[-\. ()]+)|([-\. ]+$)', '', self.excess_raw)
        clean = re.sub('[\(\)\/]', ' ', clean)

        match = re.findall('((?:(?:[A-Za-z][a-z]+|[A-Za-z])(?:[\.\ \-\+\_]|$))+)', clean)
        if match:
            match = re.findall(episode_pattern + '[\.\_\-\s\+]*(' + re.escape(match[0]) + ')',
                               self.torrent['name'], re.IGNORECASE)
            if match:
                self._part('episodeName', match, match[0], self._clean_string(match[0]))
                clean = clean.replace(match[0], '')

        clean = re.sub('(^[-_\. ()]+)|([-\. ]+$)', '', clean)
        clean = re.sub('[\(\)\/]', ' ', clean)
        match = re.split('\.\.+| +', clean)
        if len(match) > 0 and isinstance(match[0], tuple):
            match = list(match[0])

        clean = filter(bool, match)
        clean = [item for item in filter(lambda a: a != '-', clean)]
        clean = [item.strip('-') for item in clean]

        if len(clean) != 0:
            group = clean.pop() + self.group_raw
            self._part('group', [], group, group)

        # clean group name from having a container name
        if 'group' in self.parts and 'container' in self.parts:
            group = self.parts['group']
            container = self.parts['container']
            if group.lower().endswith('.'+container.lower()):
                group = group[:-(len(container)+1)]
                self.parts['group'] = group

        # split group name and encoder, adding the latter to self.parts
        if 'group' in self.parts:
            group = self.parts['group']
            pat = '(\[(.*)\])'
            match = re.findall(pat, group, flags=re.IGNORECASE)
            if match:
                match = match[0]
                raw = match[0]
                if match:
                    self._part('encoder', match, raw, match[1])
                    self.parts['group'] = group.replace(raw, '')
                    if not self.parts['group'].strip():
                        self.parts.pop('group')

        if len(clean) != 0:
            if len(clean) == 1:
                clean = clean[0]  # Avoids making a list if it only has 1 element
            self._part('excess', [], self.excess_raw, clean)
        return self.parts
