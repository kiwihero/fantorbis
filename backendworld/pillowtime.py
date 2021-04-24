import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
#converts matplotlib figure to PIL image and returns image.
#Test comment
def anothersuggestedfunction(as_plot):
    print("please put in another stackoverflow answer here")


def pillow(as_plot: plt.subplot): #include the thing taking in
    """
    Takes in a matplotlib.pyplot plot, returns the associated PIL image
    :param as_plot: Plot to get image of
    :return: Image of the plot in the form of a PIL image
    """
    import io
    buf = io.BytesIO()
    plt.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img

x = np.arange(-3,3)
plt.plot(x)
fig = plt.gcf()

# img = pillow(fig)
# img = anothersuggestedfunction(fig)
print("Output is type {}".format(type(img)))



# img.show()
