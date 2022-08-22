import numpy as np
import cv2 as cv
import base64

GaussianBlurSize = (3,3)

resSobel = 'static/resultSobel.jpg'
resPrewitt = 'static/resultPrewitt.jpg'
resCanny = 'static/resultCanny.jpg'

def Sobel(blurred):
  scale = 1
  delta = 0
  ddepth = -1
  
  
#   gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
#   blurred = cv.GaussianBlur(gray,GaussianBlurSize,0)

  Sx = cv.Sobel(blurred, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)
  Sy = cv.Sobel(blurred, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)

  return cv.addWeighted(Sx,1, Sy, 1, 0),Sx,Sy

def Prewitt(blurred):
   ddepth = -1

#    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
#    blurred = cv.GaussianBlur(gray,GaussianBlurSize,0)

   Px = np.array([[-1, 0, 1],
                       [-1, 0, 1],
                       [-1, 0, 1]], dtype=np.float32)
   
   Py = np.array([[-1, -1, -1],
                       [0, 0, 0],
                       [1, 1, 1]], dtype=np.float32)
   
   prewittx = cv.filter2D(blurred, kernel = Px, ddepth = ddepth)
   prewitty = cv.filter2D(blurred, kernel = Py, ddepth = ddepth)
   
   
   return cv.addWeighted(prewittx,1, prewitty, 1, 0)

def Canny(blurred):

  img_outsobel,Sx,Sy = Sobel(blurred)
  H, W = img_outsobel.shape[:2]

  theta = np.arctan2(Sx, Sy)
  angle = theta * 180. / np.pi
  angle[angle < 0] += 180

  Z = np.zeros((H, W))

  # 3. Maximum supression
  for i in range(1, H - 1):
      for j in range(1, W - 1):
          try:
              q = 255
              r = 255
              # angle 0
              if (0 <= angle[i, j] < 22.5) or (157.5 <= angle[i, j] <= 180):
                  q = img_outsobel[i, j + 1]
                  r = img_outsobel[i, j - 1]
              # angle 45
              elif (22.5 <= angle[i, j] < 67.5):
                  q = img_outsobel[i + 1, j - 1]
                  r = img_outsobel[i - 1, j + 1]
              # angle 90
              elif (67.5 <= angle[i, j] < 112.5):
                  q = img_outsobel[i + 1, j]
                  r = img_outsobel[i - 1, j]
              # angle 135
              elif (112.5 <= angle[i, j] < 157.5):
                  q = img_outsobel[i - 1, j - 1]
                  r = img_outsobel[i + 1, j + 1]

              if (img_outsobel[i, j] >= q) and (img_outsobel[i, j] >= r):
                  Z[i, j] = img_outsobel[i, j]
              else:
                  Z[i, j] = 0
          except IndexError as e:
              pass
  img_N = Z.astype("uint8")
  

# 4. Hysterisis Thresholding
  weak = 150
  strong = 255
  for i in np.arange(H):
      for j in np.arange(W):
          a = img_N.item(i, j)
          if (a > weak):
              b = weak
              if (a > strong):
                  b = 255
          else:
              b = 0
          img_N.itemset((i, j), b)
  img_H1 = img_N.astype("uint8")

# 5. Hysteresis Thresholding eliminasi titik tepi lemah jika tidak terhubung dengan tetangga tepi kuat
  strong = 255
  if i in range(1, H - 1):
      for j in range(1, W - 1):
          if (img_H1[i, j] == weak):
              try:
                  if ((img_H1[i + 1, j - 1] == strong) or (img_H1[i + 1, j] == strong) or
                          (img_H1[i + 1, j + 1] == strong) or (img_H1[i, j - 1] == strong) or
                          (img_H1[i, j + 1] == strong) or (img_H1[i - 1, j - 1] == strong) or
                          (img_H1[i - 1, j] == strong) or (img_H1[i - 1, j + 1] == strong)):
                      img_H1[i, j] = strong
                  else:
                      img_H1[i, j] = 0
              except IndexError as e:
                  pass
  img_H2 = img_H1.astype("uint8")

  return img_H2

def load_prepro(src):
    image = cv.imread(src)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray,GaussianBlurSize,0)

    return blurred

def load_prepro64(src):
    npimg = np.frombuffer(src, dtype=np.uint8)
    cvImg = cv.imdecode(npimg,1)
    gray = cv.cvtColor(cvImg, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray,GaussianBlurSize,0)
    return blurred

def verdict(std,stdThreshold):
    return "Positive Crack" if std > stdThreshold else "Negative Crack"

    

def saves_image(src):
    blurredImg = load_prepro(src)

    img_outsobel,Sx,Sy = Sobel(blurredImg)
    prewitt = Prewitt(blurredImg)
    canny = Canny(blurredImg)

    sobelStd = img_outsobel.std()
    prewittStd = prewitt.std()
    cannyStd = canny.std() 

    cv.imwrite(resSobel, img_outsobel)
    cv.imwrite(resPrewitt, prewitt)
    cv.imwrite(resCanny, canny)

    verdic_data =[
    {
        'name':'Sobel',
        'std': str(sobelStd),
        'verdict': verdict(sobelStd,9.08),
    },
    {
        'name': 'Prewitt',
        'std': str(prewittStd) ,
        'verdict' : verdict(prewittStd,8.35)
    },
    {
        'name': 'Canny',
        'std': str(cannyStd) ,
        'verdict' : verdict(cannyStd,2.07)
    }
    ]

    return verdic_data



def saves_image64(src):
    blurredImg = load_prepro64(src)

    img_outsobel,Sx,Sy = Sobel(blurredImg)
    prewitt = Prewitt(blurredImg)
    canny = Canny(blurredImg)
    
    sobelStd = img_outsobel.std()
    prewittStd = prewitt.std()
    cannyStd = canny.std() 

    cv.imwrite(resSobel, img_outsobel)
    cv.imwrite(resPrewitt, prewitt)
    cv.imwrite(resCanny, canny)

    

    with open(resSobel, "rb") as image_file:
        sobel64 = base64.b64encode(image_file.read())
    with open(resPrewitt, "rb") as image_file:
        prewitt64 = base64.b64encode(image_file.read())
    with open(resCanny, "rb") as image_file:
        canny64 = base64.b64encode(image_file.read())
    
    verdic_data =[
    {
        'name':'Sobel',
        'std': str(sobelStd),
        'verdict': verdict(sobelStd,9.08),
    },
    {
        'name': 'Prewitt',
        'std': str(prewittStd) ,
        'verdict' : verdict(prewittStd,8.35)
    },
    {
        'name': 'Canny',
        'std': str(cannyStd) ,
        'verdict' : verdict(cannyStd,2.07)
    },
    {
            "sobelImg" : str(sobel64) ,
            "prewittImg" :str(prewitt64),
            "cannyImg" : str(canny64),
            "statusImg":"success",
        }
    ]

    return verdic_data
    



