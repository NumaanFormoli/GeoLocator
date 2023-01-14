# GeoLocator

1. geodata.sqlite
- This sqlite database holds the location given by user and results from Google API.
2. geoload.py
- Reads where.data and uses Google API to find locations from inputs by user.
3. geodump.py
- reads the data and write it into a javascript file of the longitude and latitude.
4. where.data
- inputs provided by user
5. where.js
- holds the longitude and latitude so it can be displayed on map.
6. where.html
- loads map onto a website
