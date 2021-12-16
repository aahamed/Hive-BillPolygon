# Hive-BillPolygon
Use bill polygon data collected on Hive to annotate bird images

## Files
1. read_data.py: reads csv file from Hive and converts it into a pickle file
2. draw_annotation.py: takes an image file as input and annotates it with a polygon

## Instructions
1. Generate the pickle file:

`python read_data.py --csv-file=bill-polygon.csv --output-file=bill-polygon.pkl`

2. Use the pickle file to annotate one of the images:

`python draw_annotation.py --img-file=AMAV003.jpg --output-file=AMAV003-ann.jpg --ann-file=bill-polygon.pkl`
