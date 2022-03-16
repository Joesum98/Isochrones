from pandas import read_csv, DataFrame
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sb


def txt_to_df(file_name: str) -> DataFrame:
    """Take isochrone-table text file and create DataFrame object"""

    # fmt: off
    field_names = [
        "Zini", "MH", "logAge", "Mini", "int_IMF", "Mass",
        "logL", "logTe", "logg", "label", "McoreTP", "C_O",
        "period0", "period1", "period2", "period3", "period4",
        "pmode", "Mloss", "tau1m", "X", "Y", "Xc", "Xn", "Xo", "Cexcess", "Z",
        "mbolmag", "Umag", "Bmag", "Vmag", "Rmag", "Imag", "Jmag", "Hmag", "Kmag"
    ]
    # fmt: on

    # Read text file and delimit any number of whitespaces
    data = read_csv(file_name, delim_whitespace=True, dtype=str)

    # Delte last column as column names were offset by 1
    data.drop(data.columns[-1], axis=1, inplace=True)

    # Reset column names
    data = data.set_axis(field_names, axis=1)

    # Delete rows that are repeat column headers leftover from text file
    data.drop(data[data.MH == "Zini"].index, inplace=True)

    # Parse into floats
    data = data.astype(float)

    # turn logTe & logAge into T_eff & Age + change column name
    data.logTe = 10 ** data.logTe
    data = data.rename(columns={"logTe": "Teff"})

    data.logAge = ((10 ** data.logAge * 10e-10).round(0)).astype(int)
    data = data.rename(columns={"logAge": "Age"})

    # Add Color columns (U-B, B-V, V-I, & J-K)
    data["U-B"] = data["Umag"] - data["Bmag"]
    data["B-V"] = data["Bmag"] - data["Vmag"]
    data["V-I"] = data["Vmag"] - data["Imag"]
    data["I-J"] = data["Imag"] - data["Jmag"]
    data["J-K"] = data["Jmag"] - data["Kmag"]

    return data


def get_metallicity(df: DataFrame, m: float) -> DataFrame:
    """Take DataFrame created by txt_to_df and pick out data of only [M/H] = m"""
    return df[df.MH == m]


def get_age(df: DataFrame, a: float) -> DataFrame:
    """Take DataFrame created by txt_to_df and pick out data of only Age = a Gyr"""
    return df[df.Age == a]


def plotly_isochrone(
    df: DataFrame,
    filt1: str,
    filt2: str,
    color: str,
    cmin: int,
    cmax: int,
    n: float,
):
    """
    Create a isochrone plot in color magnitude space with color1-color2 vs color1 magnitude
    -- filt1/2 sets color axes [e.g. isochrone(df, U, B, ...) gives plot in U-B color]
    -- color sets the color of the dot and cmin/cmax set the bounds of the color scale
        [i.e. Age should have a cmin=1 and cmax=12, and MH should go from -2.2 to .6]
    """

    col = filt1 + "-" + filt2
    mag = filt1 + "mag"

    fig = px.scatter(
        df,
        x=col,
        y=mag,
        color=color,
        width=600,
        height=400,
        hover_data={col: False, mag: False, color: True},
    )

    fig.update_layout(
        title="Solar Metalicity ({})".format(col),
        paper_bgcolor="LightSteelBlue",
        margin=dict(l=20, r=20, t=50, b=20),
    )

    fig.update_xaxes(title="{}".format(col), range=[-0.5, 7])
    fig.update_yaxes(title="Magnitude", range=[25, -10])
    fig.update_coloraxes(
        colorbar_title=color,
        cmin=cmin,
        cmax=cmax,
        colorbar_dtick=n,
        colorscale="Spectral",
        reversescale=True,
    )
    return fig


def isochrone(
    df: DataFrame,
    filt1: str,
    filt2: str,
    color: str
):
    """
    Create a isochrone plot in color magnitude space with color1-color2 vs color1 magnitude
    -- Filter1/2 sets color axes [e.g. isochrone(df, U, B, ...) gives plot in U-B color]
    -- color sets the color of the dot and cmin/cmax set the bounds of the color scale
        [i.e. Age should have a cmin=1 and cmax=12, and MH should go from -2.2 to .6]
    """
    col = filt1 + "-" + filt2
    mag = filt1 + "mag"

    figure = plt.figure(figsize=(5, 5), dpi=200)
    sb.set_theme(style="darkgrid", context="notebook")
    fig = sb.scatterplot(
        data=df,
        x=col,
        y=mag,
        hue=color,
        palette="Spectral",
        s=10,
    )
    plt.xlim(-0.5, 7)
    plt.ylim(25, -10)

    return figure
