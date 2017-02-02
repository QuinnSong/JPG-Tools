"""
compare a list of images agaist base image, return a list of similiar images
input: base image object; a list of sample images
output: a list of similiar images
"""
from PIL import Image
from PIL import ImageStat
from PIL import ImageFilter

def compare (base_image, image_list):
    db = [ [0, 0, pic] for pic in image_list]

    z = [fe(db[i][2]) for i in range(len(db))]
    test_z = fe(base_image)
    for k in range(len(db)):
        for i in range(10):
            for j in range(4):
                db[k][0] += abs(z[k][i][j] - test_z[i][j])
    
    z = [ff(db[i][2]) for i in range(len(db))]
    test_z = ff(base_image)
    for k in range(len(db)):
        for i in range(10):
            db[k][1] += abs(z[k][i] - test_z[i]) * 100.0 / (sum(z[k]) + sum(test_z))
    
    print db
    result = [name for v1, v2, name in db if v1 < 20 and v2 < 10]
    print result


def fe(file_name):
    im = Image.open(file_name)
    im = im.convert('L')
    w, h = 300, 300
    im = im.resize((w, h))
    imst = ImageStat.Stat(im)
    sr = imst.mean[0]
    #def foo(t):
    #    if t < sr * 2 / 3: return 0
    #    if t <= sr: return 1
    #    if t < sr * 4 / 3: return 2
    #    return 3
    im = im.point(lambda t : 0 * ( t < sr * 2/3) + 1 * (t <= sr) + 2 * (t < sr *4/4) )#foo)
    res = [[0] * 4 for i in range(10)]
    for y in range(h):
        for x in range(w):
            k = im.getpixel((x, y))
            res[y / 60][k] += 1
            res[x / 60 + 5][k] += 1
    return res

def ff(file_name):
    im = Image.open(file_name)
    im = im.convert('L')
    w, h = 300, 300
    im = im.resize((w, h))
    im = im.filter(ImageFilter.FIND_EDGES)
    sr = ImageStat.Stat(im).mean[0]
    res = [0] * 10
    for y in range(h):
        for x in range(w):
            if im.getpixel((x, y)) > sr:
                res[y / 60] += 1
                res[x / 60 + 5] += 1
    #im.show()
    return res