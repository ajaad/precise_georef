#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import matplotlib.pyplot as plt
from matplotlib.patches import CirclePolygon
from pathlib import Path

__author__ = "Anders Johan Konnestad"
__project__ = "NOA Georeferencing"



def sterr(liste):
    val = 0
    for i in liste:
        val += (i)**2
    return ((val)**0.5)/(len(liste)-1)**0.5


def drms_plot(input_val, navn):
    DRMS, drms_in, t_drms, t_drms_in, CEP, cep_in, x_list, y_list = input_val
    
    line_w = 1
    
    
    fig, ax = plt.subplots()
    
    title_string = navn + " ( n = " + str(len(x_list)) + " ) " 
    plt.title(title_string)
    
    line_w_cir = 1.3
    
    
    t_drms_obj = ax.add_patch(CirclePolygon((0,0),
                               t_drms,
                               resolution=40,
                               color="blue",
                               linestyle="--",
                               fill=False,
                               linewidth=line_w_cir))
    
    drms_obj = ax.add_patch(CirclePolygon((0,0),
                               DRMS,
                               resolution=20,
                               color="red",
                               linestyle="--",
                               fill=False,
                               linewidth=line_w_cir))
    
    cep_obj = ax.add_patch(CirclePolygon((0,0),
                               CEP,
                               resolution=20,
                               color="green",
                               linestyle="--",
                               fill=False,
                               linewidth=line_w_cir))
    
    colors="black"
    punkt = ax.scatter(x_list, y_list, c=colors, alpha=1, label='Punkter')
    
    ax.legend([cep_obj, drms_obj, t_drms_obj], ["CEP", "DRMS","2DRMS"])
    
    bredde = -2.5,2.5
    
    ax.set_xlim(bredde)
    ax.set_ylim(bredde)
    x0,x1 = ax.get_xlim()
    y0,y1 = ax.get_ylim()
    ax.set_aspect(abs(x1-x0)/abs(y1-y0))
    
    ax.axhline(y=0, xmin=-2, xmax=2, color="black", linestyle='--', linewidth=line_w)
    ax.axvline(x=0, ymin=-2, ymax=2, color="black", linestyle='--', linewidth=line_w)
    
    plt.xlabel('X (meters)')
    plt.ylabel('Y (meters)')
    
    ramme = [-2,-1,0,1,2] # sett lappene!
    
    plt.xticks(ramme,ramme)
    plt.yticks(ramme,ramme)
    
    
    drms_string = "DRMS = " + str(round(DRMS,2)) + " meters" + "\n"+ \
        "(Inside = " +  str(int(round(drms_in,2)*100)) + "%)"
    
    
    ax.text(0,-0.25, drms_string, size=10, ha="left", 
         transform=ax.transAxes)
    
    t_drms_string = "2DRMS = " + str(round(t_drms,2)) + " meters" + "\n"+ \
        "(Inside = " +  str(int(round(t_drms_in,2)*100)) + "%)"
        
    ax.text(0,-0.40, t_drms_string, size=10, ha="left", 
         transform=ax.transAxes)
    ###
    # CEP
    cep_string = "CEP = " + str(round(CEP,2)) + " meters" + "\n"+ \
        "(Inside = " +  str(int(round(cep_in,2)*100)) + "%)" + "\n"+ \
        r"($\dot{\sigma}_y$ / $\dot{\sigma}_y$ = " + \
        str(round((sterr(y_list)/sterr(x_list)),2)) + ")"
    
    ax.text(0.55,-0.33, cep_string, size=10, ha="left", 
         transform=ax.transAxes)
    

    
    fig_name = navn + "/" + navn + ".eps"

    
    # If this file exists, the worldfile is already assessed    
    my_file = Path(fig_name)
    if my_file.exists():
        fig_name = navn + "/" + navn + "_vrt" + ".eps"
    
    plt.savefig(fig_name, bbox_inches = "tight")

############################################################################################
#initialize like this : $  

for i in enumerate(sys.stdin):
    ref_doc, fit_doc = i[1].replace("\n","").split(" ")


print(ref_doc)
print(fit_doc)

ref = open(ref_doc,"r")
fit = open(fit_doc,"r")


x_list = []
y_list = []
distance_list = []

for i, j in zip(ref, fit):
    ref_coords = [ float(x) for x in i.replace("\n","").split(" ") ]
    fit_coords = [ float(x) for x in j.replace("\n","").split(" ")[0:2] ]
    
    x_delta = ref_coords[0] - fit_coords[0]
    y_delta = ref_coords[1] - fit_coords[1]
    
    x_list.append(x_delta)
    y_list.append(y_delta)
    
    distance_list.append(((y_delta**2) + (x_delta**2))**0.5)
    
    
    
if True: #presisjon
    #####
    CEP = sterr(y_list)*0.62 + sterr(x_list)*0.56
    val = 0
    for i in distance_list:
        if CEP > i:
            val += 1
            
    cep_in = val / len(distance_list)
    
    
    print("CEP;",CEP)
    if sterr(y_list)/sterr(x_list) > 0.3:
        print("CEP_is_valid;", sterr(y_list)/sterr(x_list))
    else:
        print("CEP_cant_be_used;", sterr(y_list)/sterr(x_list))
    print("CEP_hit_ratio;",cep_in)
    
        
    val = 0
    for i in distance_list:
        if CEP > i:
            val += 1
            
    cep_in = val / len(distance_list)
        
    #####
    DRMS = (sterr(y_list)**2 + sterr(x_list)**2)**0.5

    
    
    ## DRMS treff / ikke treff
    val = 0
    for i in distance_list:
        if DRMS > i:
            val += 1
            
    drms_in = val / len(distance_list)
    ####
    val = 0
    for i in distance_list:
        if 2*DRMS > i:
            val += 1
            
    t_drms_in = val / len(distance_list)
    
    print("DRMS;",DRMS)
    print("DRMS_hit_ratio;",drms_in)
    print("2DRMS;",2*DRMS)
    print("2DRMS_hit_ratio;",t_drms_in)
    
    

if True: #Plot
    navn = ref_doc.split("/")[0] 
    input_val = [DRMS, drms_in, DRMS*2, t_drms_in, CEP, cep_in, x_list, y_list ]
    
    drms_plot(input_val, navn)
    
