import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import image as im
import numpy as np
import pandas as pd
import pickle 
from sklearn.neighbors import _dist_metrics
def unique(list1):
    x=np.unique(list1)
    sortedVal=np.sort(x)
    return list(map(str,sortedVal))
#test
# def map_heat():
#     #sns.set_theme(style="white")
#     df=pd.read_csv("./data/data.csv")
#     # Create feature and target arrays
#     signal_output_data = df.values
#     image = im.imread("data/floor_plan.png")
#     loaded_model = pickle.load(open('./model/model.pickle', 'rb'))
#     result = loaded_model.predict(signal_output_data[1:,2:8])
#     palette=sns.color_palette("rocket_r" , n_colors=len(unique(result)))
#     convres = list(map(str,result))
#     #g=sns.kdeplot(x=signal_output_data[:,0], y=signal_output_data[:,1],hue=signal_output_data[:,9],alpha = 1,fill=True,zorder=2, levels=2, palette=palette) #alpha = 0.8,s=100,linewidth=0,hue_order=clarity_ranking,cbar = True
#     g=sns.scatterplot(x=signal_output_data[1:,0], y=signal_output_data[1:,1],hue=convres,hue_order=unique(result),alpha = 1,zorder=2,s=100,linewidth=0,palette=palette)
#     g.imshow(image, zorder=1)
#     plt.show()

#while creating dataset
def map_heat():
    df=pd.read_csv("./data/data.csv")
    signal_output_data = df.values
    image = im.imread("data/floor_plan.png")
    palette=sns.color_palette("rocket_r" , n_colors=len(unique(signal_output_data[1:,9])))
    convres = list(map(str,signal_output_data[1:,9]))
    g=sns.scatterplot(x=signal_output_data[1:,0], y=signal_output_data[1:,1],hue=convres,hue_order=unique(signal_output_data[1:,9]),alpha = 1,zorder=2,s=100,linewidth=0,palette=palette)
    g.imshow(image, zorder=1)
    plt.show()