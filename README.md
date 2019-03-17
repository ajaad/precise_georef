Precission of World files
=========================

This script was written to assess the world files created by the Georeferencer plugin in QGIS and the gcps2wld.py script in GDAL.

Georeferencing is currently used to assess planned clearcuts in the forest managment.
Due to lack of openness, norwegian enviormentalists need to reconstruct the data from poorly created maps provided shortly before logging.
This script was written to raise awarness on the precission issues by using georeferenced maps!


## Installation (Linux)

Append the path to these scripts to the ~/.bashrc file and make them executable with chmod!
Reload bash to make the scripts availabele from the enviormental path!

GDAL should be installed as well!
These script utilizes the following GDAL executables:

* gdal_translate
* gdaltransform

And the following python libraries:

* sys
* matplotlib
* pathlib

## Examples

I got several georeferenced images.
All of them are georeferenced by using the Georeferencer plugin in QGIS.
A world file is created and the Ground control points (GCPs) are saved.
The .wld- and .points-files are sidecar files.


```bash
$ ls
maridalen_kart-000.png         maridalen_kart-010.png         maridalen_kart-020.png
maridalen_kart-000.png.points  maridalen_kart-010.png.points  maridalen_kart-020.png.points
maridalen_kart-000.wld         maridalen_kart-010.wld         maridalen_kart-020.wld
```

The georef.sh accepts stdin.
Filter out the sidecar files!
If the image happends to be a .png-file, use it like this:

```bash
$ ls *.png | georef.sh
```

This will create DRMS, 2DRMS and CEP precission estimates, and also output scatterplots.

If you want to use the gcps2wld.py script, you need to remove the .wld-files.
This will overwrite the plots created earlier (!)

```bash
$ rm *.wld
$ ls *.png | georef.sh
```

## References

[GPS Position Accuracy Measures](https://www.novatel.com/assets/Documents/Bulletins/apn029.pdf)




