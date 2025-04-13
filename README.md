What is save_url?
=================
It's a script to save and url in a single file with an automatic and structured name. It uses monolith as its backend.

Usage
=====

`save_url https://www.kde.org`

You will get a file with your current datetime and the title of the page. This is my way of storing interesting things. For example: 20190829 0814 KDE Community Home - KDE.org.html

Linux installation
==================

If you use Gentoo, you can find the ebuild in https://github.com/turulomio/myportage/tree/master/www-apps/save_url

For the rest of distributions:

- You need to install monolith from https://github.com/Y2Z/monolith/, setting the binary monolith in your binary path
- pip install save_url

Dependencies
============
* https://www.python.org/, as the main programming language.
* https://github.com/Y2Z/monolith/, as the backend to save one url in a single file. Thank you :)
* https://github.com/python-mechanize/mechanize, to get url title

Changelog
=========
1.0.0 (2025-04-13)
------------------
- Updated to poetry>2.0.0
- Updated poe monolith_ebuild

0.7.0 (2023-10-14)
------------------
- Improved method to search title
- Code is converted to a python module

0.6.0 (2022-11-11)
------------------
-  Added --notime parameter to remove date and time in file name

0.5.0 (2020-07-08)
-----------------
- [#4] Script asks user if title hasn't been found.

0.4.0
-----
- Script now uses mechanize to get web page title.

0.1.0
-----
- Basic functionality.
