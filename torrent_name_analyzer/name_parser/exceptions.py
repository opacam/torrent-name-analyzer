# -*- coding: utf-8 -*-


parse_exceptions = [
    {
        "parsed_title": "",
        "incorrect_parse": ("year", 1983),
        "actual_title": "1983",
    },
    {
        "parsed_title": "Marvel's Agents of S H I E L D",
        "incorrect_parse": ("title", "Marvel's Agents of S H I E L D"),
        "actual_title": "Marvel's Agents of S.H.I.E.L.D.",
    },
    {
        "parsed_title": "Marvels Agents of S H I E L D",
        "incorrect_parse": ("title", "Marvels Agents of S H I E L D"),
        "actual_title": "Marvel's Agents of S.H.I.E.L.D.",
    },
    {
        "parsed_title": "Marvels Agents of S.H.I.E.L.D.",
        "incorrect_parse": ("title", "Marvels Agents of S.H.I.E.L.D."),
        "actual_title": "Marvel's Agents of S.H.I.E.L.D.",
    },
    {
        "parsed_title": "Mayans M C",
        "incorrect_parse": ("title", "Mayans M C"),
        "actual_title": "Mayans M.C.",
    },
    {
        "parsed_title": "The Handmaids Tale",
        "incorrect_parse": ("title", "The Handmaids Tale"),
        "actual_title": "The Handmaid's Tale",
    },
]

# Add marvel series to exceptions
marvel_tvshows = [
    "Agent Carter",
    "Damage Control",
    "Daredevil",
    "Inhumans",
    "Iron Fist",
    "Jessica Jones",
    "Luke Cage",
    "The Defenders",
    "The Punisher",
]
for marvel_tvshow in marvel_tvshows:
    parse_exceptions.append(
        {
            "parsed_title": f"Marvels {marvel_tvshow}",
            "incorrect_parse": ("title", f"Marvels {marvel_tvshow}"),
            "actual_title": f"Marvel's {marvel_tvshow}",
        }
    )
