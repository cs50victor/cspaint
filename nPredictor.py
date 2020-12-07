# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
def startPrediction():
    import imageio
    from PIL import Image

    from sklearn.metrics import accuracy_score
    from sklearn.datasets import load_digits
    from sklearn.model_selection import train_test_split
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    # classifiers
    from diffprivlib.models import KMeans
    from sklearn.neighbors import KNeighborsClassifier
    #connect this file to notebook
    import string
    numberSet = load_digits()
    train_features,test_features,train_target,test_target = train_test_split(numberSet.data, numberSet.target, test_size=0.3)
    knModel = KNeighborsClassifier().fit(train_features,train_target)
    kpred = knModel.predict(test_features)
    knnAccuracy = accuracy_score(test_target, kpred)*100
    imageResize = Image.open("JustClickSave.jpg")
    w , h = imageResize.size
    l = (w - 300)/2
    t = (h - 300)/2
    r = (w + 300)/2
    b = (h + 300)/2

    imageResize = imageResize.crop((l, t, r, b)) 
    imageResize.thumbnail((8,8))
    imageResize.save("resizedForPrediction.png")

    #userImage = imageio.imread("resizedForPrediction.png", as_gray=True)

    userImage = imageio.imread("resizedForPrediction.png", as_gray=True)


    finalAdjustment = userImage.flatten().reshape(1,-1) 
    #print(finalAdjustment)
    drawingPrediction = knModel.predict(finalAdjustment)

    digit = str(drawingPrediction)
    digit = digit.translate(str.maketrans('', '', string.punctuation))
    numPred = open("prediction.txt", "w")
    numPred.write(digit)
    numPred.close()


