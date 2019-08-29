What is save_url
================
Script to save and url in a single file with an automatic and structured name. It uses monolith as its backend.

This book is interactive and lets you find your movies quickly in a book with your prefered movie images.

Linux installation
==================

If you use Gentoo, you can find the ebuild in https://github.com/turulomio/myportage/tree/master/www-apps/save_url

For the rest of distributions:

- You need to install monolith from https://github.com/Y2Z/monolith/, setting the binary monolith in your binary path
- You need to download save_url file and give it execution permissions

Usage
=====

`save_url https://www.kde.org`

You will get a file with your current datetime and the title of the page. This is my way of storing interesting things. For example: 20190829 0814 KDE Community Home - KDE.org.html

Dependencies
============
* https://www.python.org/, as the main programming language.
* https://github.com/Y2Z/monolith/, as the backend to save one url in a single file. Thank you :)

Changelog
=========

0.1.0
-----
- Basic functionality
