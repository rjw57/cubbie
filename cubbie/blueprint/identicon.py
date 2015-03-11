"""
Identicon avatar images.

"""
from flask import Blueprint, request, make_response
import pydenticon

identicon = Blueprint('identicon', __name__)

# Set-up a list of foreground colours (taken from Sigil).
foreground = [ "rgb(45,79,255)",
               "rgb(254,180,44)",
               "rgb(226,121,234)",
               "rgb(30,179,253)",
               "rgb(232,77,65)",
               "rgb(49,203,115)",
               "rgb(141,69,170)" ]

# Set-up a background colour (taken from Sigil).
background = "rgb(224,224,224)"

generator = pydenticon.Generator(5, 5,
    foreground=foreground, background=background
)

@identicon.route('/<hash>/profile.png')
def profile(hash):
    # How big an image do we want?
    sz = int(request.args.get('sz', 50))
    sz = min(256, max(1, sz))

    resp = make_response(generator.generate(hash, sz, sz))
    resp.headers['Content-Type'] = 'image/png'
    return resp
