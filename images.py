#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests


for i in range(10):
    url = f'https://gestis-api.dguv.de/api/exactimage/GHS/ghs0{i}.gif'

    r = requests.get(url)
    with open(f'images/ghs0{i}.gif', 'wb') as file:
        file.write(r.content)