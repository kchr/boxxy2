boxxy2
======

boxxy^2^ is a python port of the static image gallery script **boxxy.pl**.

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

You can use PIL (_Python Imaging Library_) instead of pillow, if you need to.

Installation
------------

    $ pip install -r requirements.txt

or

    $ pip install pillow jinja2
    
or with PIL instead of pillow:

    $ pip install --allow-external PIL --allow-unverified PIL PIL jinja2

These extra options (--allow-...) are required on Debian (testing) as of 2014-10-06.

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

    $ ./boxxy2.py -o ~/public_html/cats -t cats -c 6 ~/pics/cats
    [*] Created output directory: /home/user/public_html/cats
    [*] Created output directory: /home/user/public_html/cats/thumbs
    [*] Creating gallery 'cats' in /home/user/public_html/cats (47 files)...
    [*] Creating thumbnails (256x256)...
    [*] Rendering 6-column view from template...
    [*] Copied media asset: style.css
    [*] Copied media asset: grid.css
    [*] Wrote index file: /home/user/public_html/cats/index.html
