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
    usage: boxxy2.py [-h] [-f] -o OUTPUT [-t TITLE] [-s SIZE] [-c {2,3,4,6,8,12}]
                     SOURCE [SOURCE ...]
    
    positional arguments:
        SOURCE                Directories and/or filenames to include

    optional arguments:
      -h, --help            show this help message and exit
      -f, --force           Force overwrite of existing files
      -o OUTPUT, --output OUTPUT
                            Output directory (required)
      -t TITLE, --title TITLE
                            Title for the output index page (default "boxxy2")
      -s SIZE, --size SIZE  Thumbnail width/height (default 256)
      -c {2,3,4,6,8,12}, --cols {2,3,4,6,8,12}
                            Columns on index page (default 8)
