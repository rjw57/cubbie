"""
Test identicon generation

"""
from io import BytesIO

from flask import url_for
from PIL import Image

def test_identicon(client):
    resp = client.get(url_for('identicon.profile', hash='foobar'))
    assert resp.status_code == 200
    assert resp.headers['Content-Type'] == 'image/png'

    data = resp.get_data()
    assert len(data) > 0

    # Check it parses as a png
    im = Image.open(BytesIO(data))

def test_min_size_1(client):
    resp = client.get(url_for('identicon.profile', hash='foobar', sz=0))
    data = resp.get_data()
    im = Image.open(BytesIO(data))
    assert im.size == (1, 1)

def test_max_size_256(client):
    resp = client.get(url_for('identicon.profile', hash='foobar', sz=1000))
    data = resp.get_data()
    im = Image.open(BytesIO(data))
    assert im.size == (256, 256)

def test_size_param(client):
    resp = client.get(url_for('identicon.profile', hash='foobar', sz=100))
    data = resp.get_data()
    im = Image.open(BytesIO(data))
    assert im.size == (100, 100)

