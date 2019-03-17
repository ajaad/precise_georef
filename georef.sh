#!/bin/bash

# This script does linear georeferencing
# from QGIS georeferencer input data..

# This script assesses the precission of several georeferenced images in a batch process.
# Only the original image and a sidecar .gcp-file are required.
# If a world file is not provided, this script will generate one by using the gcps2wld.py script.
# Otherwise the provided world file will be assessed.

# This script is written to assess the precission of linear georeferencing.
# It looks like the gcps2wld.py script is better than the world files created by the Georeferencer plugin in QGIS.

#use it like this: 
#  $ ls *.png | georef.sh

mkdir plots

last_name="gammeltnavn"

while read LINE; do

  name=$(echo ${LINE} | cut -f1 -d ".") # remove all extentions

  if [ "${name}" = "${last_name}" ]; then
    # if there is two files.. make sure to use a ls expression that only pics the actual files
    continue
  fi

  last_name=${name}

  mkdir ${name} 
  rm ${name}/* >/dev/null

  wld=0

  for i in $(ls ${name}*); do
    if [[ $i == *".points" ]]; then
      punktfil=$i
    elif [[ $i == *".wld" ]]; then
      wld=$i
    elif [[ $i == *"."* ]]; then
      extent=$(echo ${i#"${name}"})
    fi
  done #< ls --ignore="*.points"

  echo  -- Name:     ${name}
  echo  -- Extent:   ${extent}
  echo  -- Verdensfil: ${wld}
  echo  -- Punktfil: ${punktfil}
  



  # get gpcs
  gpcs=$(cat ${punktfil} | load_gcp.sh)

  count=0
  mapX=0;mapY=0;pixelX=0;pixelY=0
  for i in ${gpcs}; do
    case $count in
      1) mapX=$i
      ;;
      2) mapY=$i
      ;;
      3) pixelX=$i
      ;;
      4) pixelY=$i
      ;;
    esac

    count=$((${count}+1))
    if [ ${count} -eq 5 ]; then
      # write coordinates to files!
      echo ${mapX} ${mapY} >>${name}/picture_original.csv
      echo ${pixelX} ${pixelY} >>${name}/map_original.csv
      
      count=0
    fi
  done
  
  #georeference with GCPs
  gdal_translate -a_srs EPSG:25832 ${gpcs} ${name}${extent} ${name}/${name}.tif

  

  # create worldfile an link it to the original image
  if [ ${wld} -eq 0 ]; then
    gcps2wld.py ${name}/${name}.tif > ${name}.wld
    echo  -- lager verdensfil
    cat ${name}/picture_original.csv | gdaltransform ${name}${extent} > ${name}/map_bestfit_worldfile.csv
    wld_status=gdalwld
  else
    echo -- verdensfil eksisterer allerede
    wld_status=qgiswld
  fi


  # pythonscript for both table and figure
  cat ${name}/picture_original.csv | gdaltransform ${name}${extent} > ${name}/map_bestfit_worldfile.csv
  echo ${name}/map_original.csv ${name}/map_bestfit_worldfile.csv | georef_plot.py > ${name}/worldfile_result.csv

  cp ${name}/${name}.eps plots/${name}_${wld_status}.eps

  #vrt 
  cat ${name}/picture_original.csv | gdaltransform ${name}/${name}.tif > ${name}/map_bestfit.csv
  echo ${name}/map_original.csv ${name}/map_bestfit.csv | georef_plot.py > ${name}/vrt_result.csv

  cp ${name}/${name}_vrt.eps plots/${name}_vrt.eps

done < /dev/stdin
