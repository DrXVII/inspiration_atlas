#!/usr/bin/python3

#this script reads all images he finds in the img directory (recursive)
#and creats a html document containing a grid of found images with the ability
#to view the entire image

from os import walk
import sys

#TODO it would be nicer if the image would be displayed as an overlay, not a new page

version = "v1.1"

def print_help():
	print("********** usage **********")
	print("for help: gen.py -h")
	print("general: gen.py [output filename] [path to images] [<set thumbnail width> <and height>]")
	print("***************************")
	exit()

#defaults that can be overriden via command line arguments
img_dir = "img/"
img_w = 100
img_h = 100
outp_filename = "outp.html"

#reding arguments or leaving defaults
if len(sys.argv) > 1 and (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
	print_help()

if len(sys.argv) > 1: outp_filename = sys.argv[1]

if len(sys.argv) > 2: img_dir = sys.argv[2] + "/"

if len(sys.argv) > 4:
	img_w = sys.argv[3]
	img_h = sys.argv[4]

grid_div_nm = "grid_div"

info_header = (
    "<!--" + "\n" +
    "this file was generated using gen.py version " + version + " with the following parameters" + "\n" +
    "local path to images: " + img_dir + "\n" +
    "thumbnail width: " + str(img_w) + "\n" +
    "thumbnail height: " + str(img_h) + "\n" +
    "output filename: " + outp_filename + "\n" +
    "-->" + "\n" +
    "\n")

start_of_file = (
    "<!DOCTYPE html>\n" + 
    "<html>\n" + 
    "\n" + 
    "<head>\n" + 
    "</head>\n" + 
    "\n" + 
    "<style>")

animations_css = (
    "\n" +
    "\t." + grid_div_nm + ":hover {\n" +
    "\t\tanimation-name: zoom;\n" +
    "\t\tanimation-duration: 0.5s;\n" +
    "\t\tanimation-fill-mode: forwards;\n" +
    "\t}\n" +
    "\t\n" +
    "\t@keyframes zoom {\n" +
    "\t\tfrom {transform: scale(1);}\n" +
    "\t\tto {transform: scale(1.2);}\n" +
    "\t}\n" +
    "" +
    ""
    )

img_names = []
div_names = []


for (dir_path, dir_names, file_names) in walk(img_dir):
    img_names.extend(file_names)

outp_file = open(outp_filename, "w")

outp_file.write(info_header)
outp_file.write(start_of_file)
outp_file.write(animations_css)

i = 0;
for line in img_names:
    div_name = "cropped_img_" + str(i)
    div_names.append(div_name)
    outp_file.write("\t." + div_name + " {\n")
    outp_file.write('\t\tbackground-image: url("' + img_dir + line  + '");\n')

    outp_file.write("\t\twidth: " + str(img_w) + "px;" + '\n')
    outp_file.write("\t\theight: " + str(img_h) + "px;" + '\n')
    outp_file.write("\t\tbackground-position: center;" + '\n')
    outp_file.write("\t\tbackground-size: cover; /*cover the area of the div*/" + '\n')
    outp_file.write("\t\tfloat: left;" + '\n')
    outp_file.write("\t\tmargin: 1px;" + '\n')
    outp_file.write("\t}" + '\n')

    i += 1

#close style and open body tags
outp_file.write("</style>\n");
outp_file.write("\n");
outp_file.write("<body>\n");

i = 0
for name in div_names:
    #putting the div inside a link to make the entire div clickable
    outp_file.write('\t<a href="' + img_dir + img_names[i] + '">\n')
    outp_file.write('\t\t<div class="' + grid_div_nm + " " + name + '"></div>\n')
    outp_file.write('\t</a>\n')
    i += 1

#close body and html tags
outp_file.write("</body>\n")
outp_file.write("\n")
outp_file.write("</html>\n")

outp_file.close()

exit()
