import pkgutil

from number_parser.parser import parse, parse_fraction, parse_number, parse_ordinal

__version__ = (pkgutil.get_data(__package__, "VERSION") or b"").decode("ascii").strip()

del pkgutil
