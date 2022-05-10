def convertSepia(red, green, blue, alpha):    
    Red = (0.7 * red) + (0.4 * green) + (0.2 * blue)
    Green = (0.6 * red) + (0.3 * green) + (0.2 * blue)
    Blue = (0.5 * red) + (0.3 * green) + (0.1 * blue)

    if Red > 255:
        Red = 255
    if Green > 255:
        Green = 255
    if Blue > 255:
        Blue = 255
    return int(Red), int(Green), int(Blue), alpha

def sepia(image):
    width, height = image.size
    newimg = Image.new(mode='RGBA', size=(width, height))
    pixels = newimg.load()

    for i in range(0, width, 1):
        for j in range(0, height, 1):
            pix = image.getpixel( (i, j) )
            pixels[i, j] = convertSepia(pix[0], pix[1], pix[2], 255)
    return newimg

def convertGamma(red, green, blue, alpha, avglum):    
    currentLum = (red + blue + green) / 3  

    if avglum > 128:                     # Light images
        if currentLum > (avglum*1.10) and currentLum < 225:   # If the lum is higher than the avg by 60% then leave it (unless pure white)
            temp = currentLum - avglum
            Red = red - (.4*temp)
            Green = green - (.4*temp)
            Blue = blue - (.4*temp)
        else:
            Red = red
            Green = green
            Blue = blue
    elif avglum <= 128:                      # Dark images
        if currentLum < (avglum*0.90) and currentLum > 30:   # If the lum is lower than the avg by 60% do nothing
            temp = avglum - currentLum
            Red = red + (.4*temp)
            Green = green + (.4*temp)
            Blue = blue + (.4*temp)
        else:
            Red = red
            Green = green
            Blue = blue
   
    if Red > 255:
        Red = 255
    if Green > 255:
        Green = 255
    if Blue > 255:
        Blue = 255
    return int(Red), int(Green), int(Blue), alpha

def Gamma(image):
    width, height = image.size
    newimg = Image.new(mode='RGBA', size=(width, height))
    pixels = newimg.load()
    luminance = []    

    for i in range(0, width, 1):
        for j in range(0, height, 1):
            pix = image.getpixel( (i, j) )
            luminance.append((pix[0] + pix[1] + pix[2]) / 3)
    count = 0
    avg = 0
    for num in luminance:
        count += 1
        avg += num
    avg = avg / count       # Get average luminance amount

    for i in range(0, width, 1):
        for j in range(0, height, 1):
            pix = image.getpixel( (i, j) )
            pixels[i, j] = convertGamma(pix[0], pix[1], pix[2], 255, avg)
    return newimg

def convertNegative(red, green, blue, alpha):
    Red = (255 - red)
    Green = (255 - green)
    Blue = (255 - blue)

    if Red > 255:
        Red = 255
    if Green > 255:
        Green = 255
    if Blue > 255:
        Blue = 255
    return int(Red), int(Green), int(Blue), alpha

def negative(image):
    width, height = image.size
    newimg = Image.new(mode='RGBA', size=(width, height))
    pixels = newimg.load()

    for i in range(0, width, 1):
        for j in range(0, height, 1):
            pix = image.getpixel( (i, j) )
            pixels[i, j] = convertNegative(pix[0], pix[1], pix[2], 255)
    return newimg

def convertGrayscale(red, green, blue, alpha):
    Red = (red + green + blue)/3
    Green = (red + green + blue)/3
    Blue = (red + green + blue)/3

    if Red > 255:
        Red = 255
    if Green > 255:
        Green = 255
    if Blue > 255:
        Blue = 255
    return int(Red), int(Green), int(Blue), alpha

def grayscale(image):
    width, height = image.size
    newimg = Image.new(mode='RGBA', size=(width, height))
    pixels = newimg.load()

    for i in range(0, width, 1):
        for j in range(0, height, 1):
            pix = image.getpixel( (i, j) )
            pixels[i, j] = convertGrayscale(pix[0], pix[1], pix[2], 255)
    return newimg