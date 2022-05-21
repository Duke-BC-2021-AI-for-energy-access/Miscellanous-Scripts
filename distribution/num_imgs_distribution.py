import glob
from statistics import mean, stdev
import os
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.font_manager

def plot_histogram(arr, my_title, x_axis, distribution_type, output_directory, fig_num, bins):
    """[summary]

    Args:
        arr ([type]): [description]
        title ([type]): [description]
        output_directory ([type]): [description]
        fig_num ([type]): [description]
        bins ([type]): [description]
    """
    #Remove duplicates
    plt.figure(num=fig_num, figsize=(7,5))

    #Nice font
    SIZE_DEFAULT = 14
    SIZE_LARGE = 16
    plt.rc('font', family='Roboto')           # controls default font
    plt.rc('font', weight='normal')              # controls default font
    plt.rc('font', size=SIZE_DEFAULT)       # controls default text sizes
    plt.rc('axes', titlesize=SIZE_LARGE)    # fontsize of the axes title
    plt.rc('axes', labelsize=SIZE_LARGE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SIZE_DEFAULT) # fontsize of the tick labels
    plt.rc('ytick', labelsize=SIZE_DEFAULT) # fontsize of the tick labels
    fig = plt.hist(arr, alpha = 0.65)
    #plt.title('{title} Distribution in Real Images: Mean: {u} SD: {sd}'.format(title=title,u=round(mean(arr),3),sd=round(stdev(arr),3)))
    #plt.xlim(xmin=0, xmax = 10)
    plt.xlabel(x_axis)
    plt.ylabel("Number of Images")

    #Removes lines
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.set_title(my_title, pad=20)

    np_arr = np.array(arr)
    # Calculate percentiles
    quant_5, quant_25, quant_50, quant_75, quant_95 = np.quantile(np_arr, 0.05), np.quantile(np_arr, 0.25), np.quantile(np_arr, 0.5), np.quantile(np_arr, 0.75), np.quantile(np_arr, 0.95)

    # [quantile, opacity, length, text]
    quants = [[quant_50, 1, 0.59, "50th"],  [quant_75, 0.8, 0.45, "75th"], [quant_95, 0.6, 0.15, "95th"]]

    # Plot the lines with a loop
    for i in quants:
        ax.axvline(i[0], alpha = i[1], ymax = i[2], linestyle = ":", color='red')
        ax.text(x=i[0]-250, y=i[2]+.02, s=i[3], alpha = 0.8, transform=ax.get_xaxis_transform())

    #ax.text(quant_5-.1, 0.17, "5th", size = 10, alpha = 0.8)
    #ax.text(quant_25-.13, 0.27, "25th", size = 11, alpha = 0.85)
    #ax.text(quant_50-.13, 0.37, "50th", size = 12, alpha = 1)
    #ax.text(quant_75-.13, 0.47, "75th", size = 11, alpha = 0.85)
    #ax.text(quant_95-.25, 0.57, "95th Percentile", size = 10, alpha =.8)

    
    plt.tight_layout()

    #plt.savefig("{output_dir}{title}_distribution.png".format(output_dir=output_directory,title=title))
    plt.savefig(f"{output_directory}{distribution_type}_distribution.png")

def run_distributions(lbl_directory, output_directory, domains):
    """[summary]

    Args:
        lbl_directory ([type]): [description]
        output_directory ([type]): [description]
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    num_images_arr = []
    width_arr = []
    height_arr = []
    area_arr = []

    for domain in domains:
        domain_lbl_dir = f"{lbl_directory}/{domain}/Real/"

        lbl_files = glob.glob(domain_lbl_dir + "*.txt")

        for my_txt_file in lbl_files:

            with open(my_txt_file, "r") as f:
                lst = [float(x) for x in f.read().split()]
            
            out_ht = 608
            out_w = 608

            my_widths = [round(i*out_w) for i in lst[3::5]]
            my_heights = [round(i*out_ht)  for i in lst[4::5]]

            if len(my_widths) != 0:
                num_images_arr.append(len(my_widths))
                width_arr.extend(my_widths)
                height_arr.extend(my_heights)
                area_arr.extend([my_heights[i] * my_widths[i] for i in range(len(my_heights))])
                    

    images_with_turbine_count = len(num_images_arr)

    #plot_histogram(width_arr, "Width", x_axis, "width", output_directory, 1, 20)
    #plot_histogram(height_arr, "Height", x_axis, "height", output_directory, 2, 20)
    
    num_title = "Histogram of Box Sizes for the Real Overhead Imagery"
    num_x_axis = "Number of Turbines In Image"
    plot_histogram(num_images_arr, num_title, num_x_axis, "num_images", output_directory, 3, 8)

    #area_title = "Histogram of Box Sizes for the Real Overhead Imagery"
    #area_x_axis = "Box Area by Pixels ($pixels^2$)"
    #plot_histogram(area_arr, area_title, area_x_axis, "area", output_directory, 4, 50)

lbl_directory = "/scratch/public/jitter/wt/labels"
output_directory = "/scratch/public/distributions/"
domains = ["EM", "NW", "SW"]

run_distributions(lbl_directory, output_directory, domains)