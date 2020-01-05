# XML to VRT conversion script

Convert.py converts the text corpora of four Mara Bantu languages acquired from FieldWorks Language Explorer
into the vrt-file format for importing into the Korp concordance search tool.

When exporting interlinear from FieldWorks Language Explorer, choose Verifiable generic XML. Make sure you have
only selected the text you want to export, as FLEX merges multiple texts into one file which may break the script and
result in an ill outcome.

To use the script, as usual, make sure you have the script and the input file in a same directory.
Run script with the following command:

`python3 convert.py <inputfile> <outputfile>`

For example:

`python3 convert.py masheu-ikoma.xml masheu-ikoma.vrt`

if you want to convert the file *masheu-ikoma.xml* into *masheu-ikoma.vrt*.


