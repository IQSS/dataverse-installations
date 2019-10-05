#!/bin/sh
prettier --parser html --write index.html
prettier --parser css --write css/styles.css
prettier --parser babel --write js/map.js
prettier --parser babel --write js/table.js
