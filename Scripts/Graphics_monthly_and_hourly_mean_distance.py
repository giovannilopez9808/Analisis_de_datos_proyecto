import matplotlib.pyplot as plt
from Functions import *
from pylab import *

parameters = {"path data": "../Output/",
              "file data": "Hourly_mean_distance.csv",
              "path graphics": "../Graphics/",
              "file graphics": "monthly_hourly_mean_distance.png"}

data = read_data(parameters["path data"],
                 parameters["file data"])
data["Date"] = pd.to_datetime(data["Date"])
data["Date"] = data["Date"].apply(lambda x: x.replace(year=2016))
data.index = pd.to_datetime(data["Date"])
data_mean = data.resample("MS").mean()
xticks = np.arange(-0.5, 23.5-6+2, 2)
yticks = np.linspace(-0.5, 11.5, 13)
yticks = np.delete(yticks, -1)
xlabels = xticks+0.5+6
xlabels = [int(xlabel) for xlabel in xlabels]
ylabels = ["Ene", "Feb", "Mar", "Abril", "May",
           "Jun", "Jul", "Ago", "Sept", "Oct", "Nov", "Dec"]
data_mean = data_mean.drop(columns=[str(i) for i in range(6)])
data_mean = data_mean.drop(columns="23")
data_mean = np.array(data_mean)
cmap = cm.get_cmap('magma', 10)
plt.xticks(xticks,
           xlabels)
plt.yticks(yticks+0.5,
           ylabels)
plt.xlabel("Hora local (h)")
plt.grid(ls="--",
         color="#ffffff",
         alpha=0.5,
         lw=1.5,
         axis="x")
plt.imshow(data_mean,
           origin="lower",
           cmap=cmap,
           vmin=0.6,
           vmax=1.1,
           aspect="auto")
for ytick in yticks:
    plt.plot([xticks[0], 16.5],
             [ytick, ytick],
             ls="--",
             color="#ffffff",
             alpha=0.5,
             lw=1.5)
cbar = plt.colorbar(ticks=np.round(np.linspace(0.6, 1.1, 11), 2))
cbar.set_label("Distancia promedio por viaje (km)",
               rotation=-90,
               labelpad=20)
plt.tight_layout()
plt.savefig("{}{}".format(parameters["path graphics"],
                          parameters["file graphics"]),
            dpi=400)
