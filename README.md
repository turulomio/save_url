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
* https://github.com/Y2Z/monolith/, as the backend to save one url in a single file. Thank you :)
* https://github.com/python-mechanize/mechanize, to get url title

