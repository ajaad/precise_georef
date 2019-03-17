#!/bin/bash

### Example of use:
#input_map=maridalen_kart-020.png
#gpcs=$(cat ${input_map}.points | bash load_gcp.sh) 
#gdal_translate -a_srs EPSG:25832 ${gpcs} ${input_map} out_img.tif


# From points from Georeferencer in GDAL to commandline argument

# headers from QGIS
#mapX,mapY,pixelX,pixelY,enable

count_base=0
while read LINE; do
    count_base=$(($count_base + 1))
    if [ "$count_base" -eq 1 ]; then
        #echo ${LINE}
        continue
    fi

    gcp_line=$(echo ${LINE} | tr "," " " )
    mapX=0;mapY=0;pixelX=0;pixelY=0;enable=0
    count_row=0
    for var in ${gcp_line}; do
        count_row=$((${count_row}+1))
        #echo "${count_row}"
        
        case ${count_row} in
            1) mapX=${var}
            ;;
            2) mapY=${var}
            ;;
            3) pixelX=${var}
            ;;
            4) pixelY=$(echo ${var} | tr "-" " ") ## piksellines are absolute values
            ;;
        esac
    done

echo "-gcp" ${pixelX} ${pixelY} ${mapX} ${mapY}



done < /dev/stdin


