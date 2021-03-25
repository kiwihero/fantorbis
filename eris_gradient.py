from PIL import Image, ImageDraw
def gradientDraw(X,Y,startColor,endColor,steps):
    im = Image.new(mode="RGB", size=(X, Y))
    draw = ImageDraw.Draw(im)



    startX = 0
    startY = 0
    len = int(X / steps)
    endX = len
    endY = 200
    draw.rectangle([startX, startY, endX, endY], fill=(R, G, B), outline=None, width=0)

    full_gradient = make_gradient(startColor, endColor, steps)
    for i in range(0, steps):
        startX = endX
        endX += len
        print("full gradient {}: {}".format(i, full_gradient[i]))
        draw.rectangle([startX, startY, endX, endY], fill=full_gradient[i], outline=None, width=0)



    im.show()

def make_gradient(startColor,endColor,steps):
    full_gradient = []
    # print("start {}, end {}".format(startColor,endColor))
    R = startColor[0]
    G = startColor[1]
    B = startColor[2]
    if steps == 0:
        return [(R,G,B)]

    Rdif = abs(startColor[0] - endColor[0])
    Rstep = int(Rdif / steps)
    Gdif = abs(startColor[1] - endColor[1])
    Gstep = int(Gdif / steps)
    Bdif = abs(startColor[2] - endColor[2])
    Bstep = int(Bdif / steps)
    for i in range(0,steps):
        if startColor[0]<endColor[0]:
            R +=Rstep
        elif startColor[0]>endColor[0]:
            R -= Rstep
        if startColor[1]<endColor[1]:
            G +=Gstep
        elif startColor[1] > endColor[1]:
            G -= Gstep
        if startColor[2] < endColor[2]:
            B += Bstep
        elif startColor[2] > endColor[2]:
            B -= Bstep
        # print("new r {}, g {}, b {}".format(R,G,B))
        full_gradient.append((R,G,B))
        # print("full gradient new {}".format(full_gradient[-1]))
    return full_gradient


R=130
G=245
B=0
startColor = (R,G,B)

endR =244
endG =0
endB =245
endColor = (endR,endG,endB)

X = 800
Y = 200
steps = 20


# gradientDraw(X,Y,startColor,endColor,steps)
