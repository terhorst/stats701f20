import matplotlib.pyplot as plt
import geopandas as gpd

world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres")).to_crs("EPSG:3395")
world = world[world.continent != "Antarctica"]

import pandas as pd

df = pd.read_csv("igsr_populations.tsv", sep="\t")
pops = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(
        df["Population longitude"],
        df["Population latitude"],
    ),
    crs="EPSG:4326",
).to_crs("EPSG:3395")

gdf = gpd.sjoin(world, pops, op="contains")


def plot_loadings(d):
    df = pd.DataFrame.from_dict(
        {"Population code": list(d.keys()), "loading": list(d.values())}
    )
    df = gdf.merge(df, on="Population code")
    fig, ax = plt.subplots(figsize=(8, 10))
    world.plot(ax=ax, color="white", edgecolor="black", linewidth=0.5)
    for i in range(len(d)):
        dd = df.iloc[i:(i+1)]
        dd.plot(ax=ax, color="steelblue", alpha=dd.iloc[0].loading)
