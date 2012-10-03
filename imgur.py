#/usr/bin/env python
#coding=utf8

import argparse
import cStringIO
import gtk.gdk
import pycurl
from sys import exit
from time import sleep, gmtime, strftime
from xml.dom import minidom


def shoot(name, time):
    '''Take screenshot of all the screen after three seconds.'''
    screen = gtk.gdk.get_default_root_window()
    size = screen.get_size()
    pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, size[0], size[1])
    sleep(time)
    pb = pb.get_from_drawable(screen, screen.get_colormap(), 0, 0, 0, 0,
                              size[0], size[1])
    try:
        pb.save(name, 'png')
    except:
        exit()


def upload(image):
    '''Upload an image to imgur and return the URL.'''
    curl = pycurl.Curl()
    response = cStringIO.StringIO()
    parameters = [('key', '93176df1542c61b2fa74476baa735591'),
                  ('image', (curl.FORM_FILE, image))]
    curl.setopt(curl.URL, 'http://api.imgur.com/2/upload.xml')
    curl.setopt(curl.HTTPPOST, parameters)
    curl.setopt(curl.WRITEFUNCTION, response.write)
    curl.perform()
    curl.close()
    try:
        xml = minidom.parseString(response.getvalue())
        return xml.getElementsByTagName('original')[0].firstChild.data
    except:
        exit()


def clipboard(contents):
    '''Save contents to the clipboard.'''
    clipboard = gtk.clipboard_get()
    clipboard.set_text(contents)
    clipboard.store()


def process_args():
    form = lambda prog: argparse.HelpFormatter(prog, max_help_position=30)
    parser = argparse.ArgumentParser(prog='imgur',
                                     formatter_class=form,
                                     description='''imgur - take and upload
                                     screenshots or other images to imgur''')
    parser.add_argument('-v', '--version', action='version',
                        version='imgur 0.1')
    # NOTE Implement verbose and quiet later.
    #parser.add_argument('-V', '--verbose', action='store_true',
    #                    help='''show information about program execution''')
    #parser.add_argument('-q', '--quiet', action='store_true',
    #                    help='''do not show error messages''')
    parser.add_argument('-s', '--sleep', type=int, default=3,
                        help='''number of seconds to wait before taking a
                        screenshot (the default is 3)''')
    parser.add_argument('-o', '--output',
                        help='''output screenshot name''')
    parser.add_argument('-c', '--clipboard', action='store_true',
                        help='''save the imgur url to the clipboard''')
    parser.add_argument('-n', '--no-upload', action='store_true',
                        help='''do not upload to imgur''')
    parser.add_argument('image', nargs='?',
                        help='''image to upload''')
    return parser.parse_args()


def main():
    args = process_args()
    if not args.image:
        if not args.output:
            image = 'screen-%s.png ' % strftime('%d.%m.%Y-%H.%M.%S', gmtime())
            shoot(image, args.sleep)
        else:
            image = args.output
    else:
        image = args.image
    if not args.no_upload:
        url = upload(image)
        if args.clipboard:
            clipboard(url)
        else:
            print url
    else:
        exit()


if __name__ == '__main__':
    main()
