import xml.etree.ElementTree as ET
import random
import asyncio
import sys
from tile import Tile

XMLSTRING = """<?xml version="1.0" encoding="UTF-8"?>
<tileset>
    <length value="5"/>
    <tile id="sea">
        <color r="0" g="0" b="255"/>
        <neighbors>
            <neighbor type="sea"/>
            <neighbor type="coast"/>
        </neighbors>
        <restrictions>
        </restrictions>
    </tile>
    <tile id="deepsea">
        <color r="11" g="47" b="125"/>
        <neighbors>
            <neighbor type="sea"/>
            <neighbor type="deepsea"/>
        </neighbors>
    </tile>
    <tile id="coast">
        <color r="255" g="255" b="0"/>
        <neighbors>
            <neighbor type="sea"/>
            <neighbor type="coast"/>
            <neighbor type="land"/>
        </neighbors>
        <restrictions>
            <adjacent generateAnyway="true" chance="0.97" diagonals="true"/>
        </restrictions>
    </tile>
    <tile id="land">
        <color r="0" g="255" b="0"/>
        <neighbors>
            <neighbor type="coast"/>
            <neighbor type="land"/>
        </neighbors>
    </tile>
    <tile id="trail">
        <color r="139" g="69" b="19"/>
        <neighbors>
            <neighbor type="land"/>
            <neighbor type="trail"/>
        </neighbors>
        <restrictions>
            <adjacent generateAnyway="true" chance="0.80" diagonals="false"/>
            <thickness/>
        </restrictions>
    </tile>
</tileset>
"""

def load_tileset():
    root = ET.fromstring(XMLSTRING)
    tiles = root.findall('tile')

    tileset = []

    for tile in tiles:
        id = tile.get('id')
        color_element = tile.find('color')
        color = {
            'r': int(color_element.get('r')),
            'g': int(color_element.get('g')),
            'b': int(color_element.get('b'))
        }

        neighbors = [neighbor.get('type') for neighbor in tile.findall('neighbors/neighbor')]

        restrictions = []
        restriction_elements = tile.find('restrictions')
        if restriction_elements is not None:
            for restriction_element in restriction_elements:
                restriction = {key: restriction_element.get(key) for key in restriction_element.keys()}
                restriction['type'] = restriction_element.tag
                restrictions.append(restriction)

        if id == 'coast':
            coast = Tile(color, neighbors, restriction, id)

        tileset.append(Tile(color, neighbors, restrictions, id))

    return tileset