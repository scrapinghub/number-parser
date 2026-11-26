Changes
=======

0.3.3 (unreleased)
------------------

Security bug fixes:
- On interpreters without the int/str digit limit (CPython releases before 3.9.14 and 3.10.7), ``parse_number`` returns ``None`` for a digit string longer than 4300 characters instead of converting it in quadratic time


0.3.2 (2023-03-28)
------------------

Fix:
- Fix import bug (#91)


0.3.1 (2023-03-22)
------------------

Improvements:
- Add Python 3.10, 3.11 support (#83)
- Add __version__ (#87)
- Replace OrderedDict with dict (#88)

Fix:
- Inconsistent white space handling around sentence separators following numbers (#76, #77)


0.3.0 (2022-10-20)
------------------

Improvements:
- Added support for bigger numbers in Spanish (#43)
- Added pytest flake8 (#44)
- Refactored the code (#45)
- Improved testing (#46)
- Improved scripts (#47)
- Added tests (#50, #72)
- Added GitHub actions (#54, #55, #56, #57)
- Added support for simple fractions (#60)

New features:
- Added feature to parse numbers in Ukrainian (#79)


0.2.1 (2020-08-25)
------------------

Fix tokenization bug - Hindi


0.2.0 (2020-08-18)
------------------

Ordinal Number Support


0.1.0 (2020-07-30)
------------------

Initial release.
