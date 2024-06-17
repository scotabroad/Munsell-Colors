import colour
from colour.plotting import *
from statistics import *
import matplotlib.pyplot as plt
from colour.blindness import matrix_cvd_Machado2009
import numpy as np
from colour.utilities import as_float_array

def sRGB_to_linearRGB(color):
    out = np.zeros_like(color)
    small_mask = color < 0.04045
    large_mask = np.logical_not(small_mask)
    out[small_mask] = color[small_mask] / 12.92
    out[large_mask] = np.power((color[large_mask] + 0.055) / 1.055, 2.4)
    return out

def linearRGB_to_sRGB(color):
    out = np.zeros_like(color)
    # Make sure we're in range, otherwise gamma will go crazy.
    color = np.clip(color, 0., 1.)
    small_mask = color < 0.0031308
    large_mask = np.logical_not(small_mask)
    out[small_mask] = color[small_mask] * 12.92
    out[large_mask] = np.power(color[large_mask], 1.0 / 2.4) * 1.055 - 0.055
    return out

def munsell_colour_to_sRGB(munsell_color):
    xyY = colour.munsell_colour_to_xyY(munsell_color)
    XYZ = colour.xyY_to_XYZ(xyY)
    return colour.XYZ_to_sRGB(XYZ)

def munsell_colour_to_cvd(munsell_color, deficiency, severity):
    M_a = matrix_cvd_Machado2009(deficiency, severity)
    xyY = colour.munsell_colour_to_xyY(munsell_color)
    XYZ = colour.xyY_to_XYZ(xyY)
    RGB = colour.XYZ_to_sRGB(XYZ)
    linear_RGB = sRGB_to_linearRGB(RGB)
    CVD = np.matmul(as_float_array(M_a), as_float_array(linear_RGB))
    return linearRGB_to_sRGB(CVD) 

#Munsell is HUE VALUE/CHROMA (so 4R 9/3)
#For neutrals, it is N + VALUE (so, N2)
munsell_hue_nom = ['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP'] #here, they use PB instead of BP
munsell_hue_num = ['2.5', '5', '7.5', '10']
munsell_value = ['1.5', '2.0', '3.0', '4.0', '5.0', '6.0', '7.0', '8.0', '9.0', '9.5']
munsell_chroma = {
'9.0': [2, 2, 2, 2, 2, 2, 2, 2, 4, 6, 6, 6, 6, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
'8.0': [6, 6, 6, 6, 6, 6, 8,14,16,14,12,12,12,10,10, 8, 8, 6, 6, 6, 6, 4, 4, 4, 4, 4, 4, 4, 6, 6, 4, 4, 4, 4, 6, 6, 6, 6, 6, 6],
'7.0': [8, 8,10,10,10,14,14,14,12,12,12,12,12,12,10,10,10, 8, 8, 8, 8, 8, 6, 6, 6, 6, 6, 8, 8, 8, 6, 6, 6, 6, 8, 8,10,10, 8, 8],
'6.0': [12,12,12,14,16,12,12,12,10,10,10,10,10,10,12,12,10,10,10,10, 8, 8, 8, 8, 8, 8, 8,10,10,10, 8, 8, 8, 8,10,10,10,10,12,12],
'5.0': [14,14,14,16,14,12,10,10, 8, 8, 8, 8, 8, 8,10,12,12,10,10,10,10, 8, 8, 8, 8, 8, 8,10,12,12,10,10,10,10,10,12,12,12,14,14],
'4.0': [14,14,14,14,10, 8, 8, 6, 6, 6, 6, 6, 6, 6, 8, 8,10,10,10,10, 8, 8, 8, 8, 6, 6, 8, 8,10,10,12,10,10,10,10,10,10,10,10,10],
'3.0': [10,10,12,10, 8, 6, 6, 6, 4, 4, 4, 4, 4, 4, 6, 6, 8, 8,10, 8, 6, 6, 6, 6, 6, 6, 6, 8,10,10,12,10,10,10,10,10,10,10,10,10],
'2.0': [8, 8, 8, 6, 4, 4, 4, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 6, 6, 6, 4, 4, 4, 4, 4, 4, 6, 6, 6, 8,10, 8, 8, 8, 6, 6, 8, 8, 8, 8],
}

#Below will be a list of lists, each row being of the same value
def true_values():
    munsell_colors = []
    for value in munsell_value:
        if value == '9.5' or value == '1.5':
            row = []
            for i in range(41): #runs from 0 to 40, total of 41 times
                RGB = munsell_colour_to_sRGB('N' + value)
                row.append(ColourSwatch(RGB))#, 'N' + value)) #+ str(i)
            munsell_colors.append(row)
        else:
            neutral = 'N' + value
            neutral_RGB = munsell_colour_to_sRGB(neutral)
            row = [ColourSwatch(neutral_RGB)]#, neutral)]
            chroma_row = munsell_chroma[value]
            i = 0
            for nominal in munsell_hue_nom:
                for number in munsell_hue_num:
                    munsell_color = number + nominal + ' ' + value + '/' + str(chroma_row[i])
                    RGB = munsell_colour_to_sRGB(munsell_color)
                    row.append(ColourSwatch(RGB))#, munsell_color))
                    i += 1
            munsell_colors.append(row)

    #munsell_colors is a list of lists... but it should not be. Flatten it
    single_list = munsell_colors[0] + munsell_colors[1] + munsell_colors[2] + munsell_colors[3] + munsell_colors[4] + munsell_colors[5] + munsell_colors[6] + munsell_colors[7] + munsell_colors[8] + munsell_colors[9]
                
    # Images are not responsive in Google Colab, thus reducing the figure size.

    plt.style.use({'figure.figsize': (10.24, 5.76)})
    plot_multi_colour_swatches(single_list, columns=41)

def true_cvd_values(deficiency, severity):
    munsell_colors = []
    for value in munsell_value:
        if value == '9.5' or value == '1.5':
            row = []
            for i in range(41): #runs from 0 to 40, total of 41 times
                RGB = munsell_colour_to_cvd('N' + value, deficiency, severity)
                row.append(ColourSwatch(RGB))#, 'N' + value)) #+ str(i)
            munsell_colors.append(row)
        else:
            neutral = 'N' + value
            neutral_RGB = munsell_colour_to_cvd(neutral, deficiency, severity)
            row = [ColourSwatch(neutral_RGB)]#, neutral)]
            chroma_row = munsell_chroma[value]
            i = 0
            for nominal in munsell_hue_nom:
                for number in munsell_hue_num:
                    munsell_color = number + nominal + ' ' + value + '/' + str(chroma_row[i])
                    RGB = munsell_colour_to_cvd(munsell_color, deficiency, severity)
                    row.append(ColourSwatch(RGB))#, munsell_color))
                    i += 1
            munsell_colors.append(row)

    #munsell_colors is a list of lists... but it should not be. Flatten it
    single_list = munsell_colors[0] + munsell_colors[1] + munsell_colors[2] + munsell_colors[3] + munsell_colors[4] + munsell_colors[5] + munsell_colors[6] + munsell_colors[7] + munsell_colors[8] + munsell_colors[9]
                
    # Images are not responsive in Google Colab, thus reducing the figure size.

    plt.style.use({'figure.figsize': (10.24, 5.76)})
    plot_multi_colour_swatches(single_list, columns=41)

def avg_values():
    munsell_colors = []
    for value in munsell_value:
        if value == '9.5' or value == '1.5':
            row = []
            for i in range(41): #runs from 0 to 40, total of 41 times
                RGB = munsell_colour_to_sRGB('N' + value)
                row.append(ColourSwatch(RGB))#, 'N' + value)) #+ str(i)
            munsell_colors.append(row)
        else:
            neutral = 'N' + value
            neutral_RGB = munsell_colour_to_sRGB(neutral)
            row = [ColourSwatch(neutral_RGB)]#, neutral)]
            chroma_row = int(fmean(munsell_chroma[value]))
            i = 0
            for nominal in munsell_hue_nom:
                for number in munsell_hue_num:
                    munsell_color = number + nominal + ' ' + value + '/' + str(chroma_row)
                    RGB = munsell_colour_to_sRGB(munsell_color)
                    row.append(ColourSwatch(RGB))#, munsell_color))
                    i += 1
            munsell_colors.append(row)

    #munsell_colors is a list of lists... but it should not be. Flatten it
    single_list = munsell_colors[0] + munsell_colors[1] + munsell_colors[2] + munsell_colors[3] + munsell_colors[4] + munsell_colors[5] + munsell_colors[6] + munsell_colors[7] + munsell_colors[8] + munsell_colors[9]
                
    # Images are not responsive in Google Colab, thus reducing the figure size.

    plt.style.use({'figure.figsize': (10.24, 5.76)})
    plot_multi_colour_swatches(single_list, columns=41)

def avg_cvd_values(deficiency, severity):
    munsell_colors = []
    for value in munsell_value:
        if value == '9.5' or value == '1.5':
            row = []
            for i in range(41): #runs from 0 to 40, total of 41 times
                RGB = munsell_colour_to_cvd('N' + value, deficiency, severity)
                row.append(ColourSwatch(RGB))#, 'N' + value)) #+ str(i)
            munsell_colors.append(row)
        else:
            neutral = 'N' + value
            neutral_RGB = munsell_colour_to_cvd(neutral, deficiency, severity)
            row = [ColourSwatch(neutral_RGB)]#, neutral)]
            chroma_row = int(fmean(munsell_chroma[value]))
            i = 0
            for nominal in munsell_hue_nom:
                for number in munsell_hue_num:
                    munsell_color = number + nominal + ' ' + value + '/' + str(chroma_row)
                    RGB = munsell_colour_to_cvd(munsell_color, deficiency, severity)
                    row.append(ColourSwatch(RGB))#, munsell_color))
                    i += 1
            munsell_colors.append(row)

    #munsell_colors is a list of lists... but it should not be. Flatten it
    single_list = munsell_colors[0] + munsell_colors[1] + munsell_colors[2] + munsell_colors[3] + munsell_colors[4] + munsell_colors[5] + munsell_colors[6] + munsell_colors[7] + munsell_colors[8] + munsell_colors[9]
                
    # Images are not responsive in Google Colab, thus reducing the figure size.

    plt.style.use({'figure.figsize': (10.24, 5.76)})
    plot_multi_colour_swatches(single_list, columns=41)

true_values()
avg_values()
true_cvd_values('Protanomaly', 1)
avg_cvd_values('Protanomaly', 1)
