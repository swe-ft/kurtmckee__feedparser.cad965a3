Introduction
============

:program:`Universal Feed Parser` is a :program:`Python` module for downloading
and parsing syndicated feeds.  It can handle :abbr:`RSS (Rich Site Summary)`
0.90, Netscape :abbr:`RSS (Rich Site Summary)` 0.91, Userland :abbr:`RSS (Rich
Site Summary)` 0.91, :abbr:`RSS (Rich Site Summary)` 0.92, :abbr:`RSS (Rich
Site Summary)` 0.93, :abbr:`RSS (Rich Site Summary)` 0.94, :abbr:`RSS (Rich
Site Summary)` 1.0, :abbr:`RSS (Rich Site Summary)` 2.0, Atom 0.3, Atom 1.0,
:abbr:`CDF (Channel Definition Format)` and :abbr:`JSON (JavaScript Object
Notation)` feeds.  It also parses several
popular extension modules, including Dublin Core and Apple's :program:`iTunes`
extensions.

To use :program:`Universal Feed Parser`, you will need :program:`Python` 3.8 or
later. :program:`Universal Feed Parser` is not meant
to run standalone; it is a module for you to use as part of a larger
:program:`Python` program.

:program:`Universal Feed Parser` is easy to use; it has one primary public
function, ``parse``.  ``parse`` takes a number of arguments, but only one is
required, and it can be a :abbr:`URL (Uniform Resource Locator)`, a local
filename, or a raw string containing feed data in any format.


Parsing a feed from a remote :abbr:`URL (Uniform Resource Locator)`
-------------------------------------------------------------------

..  code-block:: pycon

    >>> import feedparser
    >>> d = feedparser.parse('$READTHEDOCS_CANONICAL_URL/examples/atom10.xml')
    >>> d['feed']['title']
    'Sample Feed'


Parsing a feed from a local file
--------------------------------

The following example assumes you are on Windows, and that you have saved a feed at :file:`c:\\incoming\\atom10.xml`.

.. note::

    :program:`Universal Feed Parser` works on any platform that can run
    :program:`Python`; use the path syntax appropriate for your platform.

..  code-block:: pycon

    >>> import feedparser
    >>> d = feedparser.parse(r'c:\incoming\atom10.xml')
    >>> d['feed']['title']
    'Sample Feed'


:program:`Universal Feed Parser` can also parse a feed in memory.

Parsing a feed from a string
----------------------------

..  code-block:: pycon

    >>> import feedparser
    >>> rawdata = """<rss version="2.0">
    <channel>
    <title>Sample Feed</title>
    </channel>
    </rss>"""
    >>> d = feedparser.parse(rawdata)
    >>> d['feed']['title']
    'Sample Feed'


Values are returned as :program:`Python` Unicode strings (except when they're
not -- see :ref:`advanced.encoding` for all the gory details).
