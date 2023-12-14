import matplotlib.pyplot as plt

def plot_global(arr, name):
    fig = plt.figure()
    ax = plt.axes()
    im = ax.imshow(arr, extent=[-180,180,-90,90], cmap='coolwarm', origin='lower', interpolation='nearest')
    plt.axis('off')
    cax = fig.add_axes([ax.get_position().x1+0.01,ax.get_position().y0,0.02,ax.get_position().height])
    cb = plt.colorbar(im, cax=cax)
    cb.outline.set_visible(False)

    return fig
