#!/usr/bin/env python
# -*- vim set ft=python
#
# @author kchr

from PIL import Image as pil, ImageOps as pilops

import jinja2

import argparse

import os
import glob
import shutil
import time
import sys

parser = argparse.ArgumentParser()

parser.add_argument('-f', '--force', action="store_true",
                    help='Force overwrite of existing files')
parser.add_argument('-o', '--output', type=str, required=True,
                    help='Output directory (required)')
parser.add_argument('-t', '--title', type=str,
                    help='Title for the output index page (default "gallery")')
parser.add_argument('-s', '--size', type=int,
                    help='Thumbnail width/height (default 256)')
parser.add_argument('-c', '--cols', type=int, choices=[2, 3, 4, 6, 8, 12],
                    help='Columns on index page (default 8)')
parser.add_argument('sources', metavar='SOURCE', type=str, nargs='+',
                    help='Directory or filename to include')

args = parser.parse_args()

env = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates'))

tpl_list = env.get_template('list.html')
tpl_list_images = []

out_dir = args.output or 'www'
out_title = args.title or 'gallery'
out_size = args.size or 256
out_cols = args.cols or 8
out_force = args.force or False

# Thumbnail options
tn_size = (out_size, out_size)  # thumbnail width x height
tn_canvas = 'black'             # canvas bleed color (upsizing bg)
tn_dir = os.path.join(out_dir, 'thumbs')    # thumbnail subdir

s_list = []
s_failed = False

for d in [out_dir, tn_dir]:
    if not os.path.isdir(d):
        os.mkdir(d)
        print "[*] Created output directory: %s" % d
    else:
        print "[*] Using output directory: %s" % d


def wdir(files, dirname, names):
    for bn in names:
        f = os.path.join(dirname, bn)
        if os.path.isdir(f):
            pass
        elif os.path.isfile(f):
            if not f in files:
                files.append(f)
        else:
            print 'Unknown file: %s' % f

for s_glob in args.sources:
    for s in glob.glob(s_glob):
        ab = os.path.abspath(s)
        if not os.path.exists(s):
            s_failed = True
            print "Could not read source: %s" % s
        else:
            os.path.walk(s, wdir, s_list)


print "[*] Creating gallery '%s' in %s (%d files)..." \
    % (out_title, out_dir, len(s_list))

print "[*] Creating thumbnails (%dx%d)..." % tn_size

for infile in sorted(s_list):

    filename, ext = os.path.splitext(infile)
    basename = os.path.basename(filename)

    tn_name = '%s_tn%s' % (basename, ext)
    tn_path = '%s/%s' % (tn_dir, tn_name)

    im = pil.open(infile)

    (width, height) = im.size

    # No side is smaller than 256, fit (downsize) it
    if min(im.size) > min(tn_size):

        bleed = 0
        center = (0.5, 0.5)

        im_t = pilops.fit(im, tn_size, pil.NEAREST, bleed, center)

    # One side is smaller than 256, crop and paste
    else:

        im_t = pil.new(im.mode, tn_size, tn_canvas)

        box_ul = (tn_size[0] - width) / 2
        box_lr = (tn_size[1] - height) / 2

        im_t.paste(im, (box_ul, box_lr))

    try:
        # Read metadata from file
        created = time.ctime(os.path.getctime(infile))
        modified = time.ctime(os.path.getmtime(infile))

        target = os.path.join(out_dir, basename + ext)

        # Check if file exists, skip if not forced
        if os.path.isfile(target):
            if not out_force:
                print "[/] File exists, skipping: %s" % target
                continue

        # Copy infile to output directory
        shutil.copy2(infile, target)

        try:
            # Save thumbnail
            im_t.save(tn_path)

            # Image dict for template output
            image = {
                'url': basename + ext,
                'title': basename,
                'date_created': created,
                'date_modified': modified,
                'thumb_url': os.path.join('thumbs', tn_name)
            }

            tpl_list_images.append(image)

        except (IOError, os.error) as why:
            print "[x] Failed to save thumbnail: %s (%s)" % (tn_path, why)

    except (IOError, os.error) as why:
        print "[x] Failed to copy source: %s -> %s (%s)" \
            % (infile, out_dir, why)

try:
    print "[*] Rendering %d-column view from template..." % out_cols

    index = os.path.join(out_dir, 'index.html')

    # Render output from template
    output = tpl_list.render(title=out_title,
                             cols=out_cols,
                             images=tpl_list_images)

    # to save the results
    with open(index, 'wb') as fh:
        fh.write(output)

    # Copy CSS to output directory
    for f in ['templates/style.css', 'templates/grid.css']:
        bn = os.path.basename(f)
        try:
            shutil.copy2(f, os.path.join(out_dir, bn))
            print "[*] Copied media asset: %s" % bn
        except (IOError, os.error) as why:
            print "[x] Failed to copy media: %s (%s)" % (bn, why)

    print "[*] Wrote index file: %s" % index

except (IOError, os.error) as why:
    print "[x] Failed to write output: %s (%s)" % (index, why)
except (Exception, os.error) as why:
    print "Failed to compile output (%s)" % (why)
