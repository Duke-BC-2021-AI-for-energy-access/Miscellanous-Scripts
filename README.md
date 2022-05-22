# Key Scripts

This is an overview of the utility scripts that were made to facilitate our data preprocessing and experimentation pipeline throughout research. 

## Image Preprocessing Scripts

### background_cropper- 
Given a directory of images, crops images in directory to given height/width and outputs to new folder; can crop middle or top left of image

## Image Augmentation Scripts

### shadow_parser- 

plot_shadows and plot_unmatched uses the functions of bounding_boxs to plot the regular and shadow labels of an image.

In order to complete our image augmentation, we wanted to crop real wind turbines and then put them onto a white canvas and blend them into a background. In doing so, we created YOLO labels that included just the turbine for feeding into YOLO, as well as labels of the wind turbine and the shadow for the image augmentation. This is because the shadow provides useful context for the turbine and when taking the time to label- this does not greatly increase
the time cost. 

crop_shadows goes through the real and shadow labels uses the shadow labels to crop out turbines, with additional checks to ensure the object is not too close to the image border and ensures that it geometrically contains a turbine label within it. This is because in order to create labels for synthetic imagery, we need the information as to where a turbine is relative to the entire crop with the shadow. By ensuring a one to one match, the relevant calculations are made to determine relative label. 

## Various Checks and

### bounding_boxs- 
Plots bounding boxes for images given directories holding images and directory holding their corresponding YOLO label directories

### create_empty_lbl_files.py- 
Reads in files without a txt file (images with no turbine), creates a empty txt file to serve as a lbl for each image. This makes training with supplemental background images easier while following the name convention (although other techniques can be used such as creating one blank label file that all background images reference to). This was used for our background vs synthetic imagery experiment

### distribution and extraneous/real_distribution.py- 
Takes in a label directory and the domains within the directory and then creates a histogram and can display the distribution of things such as the number of objects per image or the area of the objects within the dataset. Takes advantage of matplotlib features to make a more aesthetic histogram (for presentations, websites)

### mask_tester- 
Given a directory holding images/masks, it uses the bitwise and command to output and show what the image looks like in the context of the mask (the parts of the image corresponding to the white sections of the mask). This allows you to tell how well the mask maps an image before running it through GP-GAN.

### map_retriever- 
Given an experimental output directory, it creates a CSV holding source domain, target domain, trial number, and average precision for each trial (for easier data entry into main excel). This is based on the output of test_results.txt from the YOLO run.


## Extraneous Scripts

### get_files_annotate.py- 
Given a txt file holding the images you are to annotate, it copies the files to a separate directory (so they can be downloaded all at once in a directory 

### repro_bass_updater- 
Used to update file names in directories and scripts before version control was working (can be used when codebase is changed- was only necessary when absolute pathing was used)

### txt_file_generator- 
Generalizable script meant for generating YOLO txt files for both training and validation for an experimental setup containing various domain combinations with baseline/supplementary imagery
