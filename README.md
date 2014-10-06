boxxy2
======

Python port of static image gallery script **boxxy.pl**.

Output is HTML and CSS only, no scripts.

User supplies the output directory and an arbitrary list of image dirs/files.

Features
--------

* No Javascript
* Custom gallery title
* Responsive thumbnail disposition
* Fancy opacity shading effect on hover
* Six different layouts (varying no. of columns)

Requirements
------------

* pillow (or PIL)
* jinja2

You can use **PIL** (_Python Imaging Library_) instead of Pillow, if you need to.

Installation
------------

    $ pip install -r requirements.txt

or

    $ pip install pillow jinja2

Usage
-----

    $ ./boxxy2.py -h
