import warnings
warnings.filterwarnings('ignore')
import os
import cv2
import tkinter as tk
import threading
from tkinter.filedialog import askopenfilename
from tkinter import PhotoImage
from PIL import ImageTk,Image
#import AnimateGIF
import AnimatedGif
import Fruit_Object_detection
import VolumeDetection

#This is for getting the path of the current folder
CurrentFolderPath = os.getcwd()

#Object from TKinter creates blank window

root = tk.Tk()
root.title("FruitMeter Application")

ProgramIconPath = os.path.join(CurrentFolderPath,'GUI_Elements','ProgramIcon.png')
ProgramIconImg = ImageTk.PhotoImage(Image.open(ProgramIconPath))
root.iconphoto(False,ProgramIconImg)

WidthScreen = root.winfo_screenwidth()
HeightScreen = root.winfo_screenheight()

#The Window size
root.minsize(1316, 668)

x = (WidthScreen/2) - ((WidthScreen-30)/2)
y = (HeightScreen/2) - ((HeightScreen-30)/2)

#Display the window at the center of the screen when it shows up
root.geometry('%dx%d+%d+%d' % (WidthScreen-50, HeightScreen-100, x, y))

#disable the resize option
root.resizable(0,0)


t1 = threading.Thread()
UploadSidePicFlag = False
UploadTopPicFlag = False


#---------------------------------Button Functions-----------------------------------------------


def UploadSideImage():
    global SideViewImagePath,SideViewImgLabel,UploadSidePicFlag
    SideViewImagePath = askopenfilename(filetypes=[("Image File",'.jpg')])
    PIL_SideViewImage = Image.open(SideViewImagePath)
    width, height = PIL_SideViewImage.size
    
    if(height > width):
        PIL_SideViewImage = PIL_SideViewImage.transpose(Image.ROTATE_90)
    
    SideViewImgPIL = PIL_SideViewImage.resize((590, 443), Image.ANTIALIAS)    
    SideViewImgPIL = ImageTk.PhotoImage(SideViewImgPIL)
    UploadSideImgBtn.destroy()
    SideViewImgLabel = tk.Label(root, height=443, width=590, image = SideViewImgPIL)
    SideViewImgLabel.image = SideViewImgPIL
    SideViewImgLabel.place(x = 45,y = 98)   
    UploadSidePicFlag = True


def UploadTopImage():
    global TopViewImagePath,TopViewImgLabel,UploadTopPicFlag
    TopViewImagePath = askopenfilename(filetypes=[("Image File",'.jpg')])
    PIL_TopViewImage = Image.open(TopViewImagePath)
    width, height = PIL_TopViewImage.size
    
    if(height > width):
        PIL_TopViewImage = PIL_TopViewImage.transpose(Image.ROTATE_90)
        
    TopViewImgPIL = PIL_TopViewImage.resize((590, 443), Image.ANTIALIAS)    
    TopViewImgPIL = ImageTk.PhotoImage(TopViewImgPIL)
    UploadTopImgBtn.destroy()
    TopViewImgLabel = tk.Label(root, height=443, width=590, image = TopViewImgPIL)
    TopViewImgLabel.image = TopViewImgPIL
    TopViewImgLabel.place(x = 661,y = 98)
    UploadTopPicFlag = True


def DisplayCalorieResults(FruitObject1,FruitObject2):
    
    #Creating a VolumeDetection object to calculate the calories 
    VolDetector = VolumeDetection.VolumeDetection(SegmentedSideImageBGR, SegmentedTopImageBGR)
    VolDetector.setScaleFactor(FruitObject1.getCoinScaleFactor(), FruitObject2.getCoinScaleFactor())
    
    DetectedFruit = FruitObject1.getFruit()
    DetectedVolume = VolDetector.CalculateFruitVolume(DetectedFruit[0])
    DetectedMass = VolDetector.getFruitMass(DetectedFruit[0])
    DetectedCalories = VolDetector.getFruitCalories()
    
    
    print("The volume of the", DetectedFruit[0], "is :", VolDetector.CalculateFruitVolume(DetectedFruit[0]), "cm3")
    print("The mass of the", DetectedFruit[0], "is :", VolDetector.getFruitMass(DetectedFruit[0]), "grams")
    print("The Calories estimated of the", DetectedFruit[0], "is :", VolDetector.getFruitCalories(), "Kcal")
    
    #Deleting the elements of the previous page
    SegmentedSideLabel.destroy()
    SegmentedTopLabel.destroy()
    NextbtnImgBtn3.destroy()
    SegmentedFruitText.destroy()
    
    CaloriesText = tk.StringVar()
    strCalorie = (("The Calories in the " +  DetectedFruit[0]))
    CaloriesText.set(strCalorie)
    CaloriesTextdisplay = tk.Label(root, font=("Arial", 30), textvariable=CaloriesText)
    CaloriesTextdisplay.place(x = 775,y = 120)
    
    
    CaloriesText = tk.StringVar()
    strCalorie = ((str(DetectedCalories)+" kcal"))
    CaloriesText.set(strCalorie)
    CaloriesTextdisplay = tk.Label(root, font=("Arial", 40), textvariable=CaloriesText)
    CaloriesTextdisplay.place(x = 870,y = 170)
    
    if(DetectedFruit[0] == "Apple"):
        FruitImagePath = os.path.join(CurrentFolderPath,'GUI_Elements','Apple.jpg')
        FruitImg = ImageTk.PhotoImage(Image.open(FruitImagePath))
        FruitImgLabel = tk.Label(root, image = FruitImg)
        FruitImgLabel.image = FruitImg
        FruitImgLabel.place(x = 885,y = 250)
        
    elif(DetectedFruit[0] == "Banana"):
        FruitImagePath = os.path.join(CurrentFolderPath,'GUI_Elements','Banana.jpg')
        FruitImg = ImageTk.PhotoImage(Image.open(FruitImagePath))
        FruitImgLabel = tk.Label(root, image = FruitImg)
        FruitImgLabel.image = FruitImg
        FruitImgLabel.place(x = 885,y = 250)
        
    elif(DetectedFruit[0] == "Orange"):
        FruitImagePath = os.path.join(CurrentFolderPath,'GUI_Elements','Orange.jpg')
        FruitImg = ImageTk.PhotoImage(Image.open(FruitImagePath))
        FruitImgLabel = tk.Label(root, image = FruitImg)
        FruitImgLabel.image = FruitImg
        FruitImgLabel.place(x = 885,y = 250)
    
    elif(DetectedFruit[0] == "Mango"):
        FruitImagePath = os.path.join(CurrentFolderPath,'GUI_Elements','Mango.jpg')
        FruitImg = ImageTk.PhotoImage(Image.open(FruitImagePath))
        FruitImgLabel = tk.Label(root, image = FruitImg)
        FruitImgLabel.image = FruitImg
        FruitImgLabel.place(x = 885,y = 250)   
        
        
    MassText = tk.StringVar()
    strCalorie =(("The mass of the "+ DetectedFruit[0] +" is : "+ str(VolDetector.getFruitMass(DetectedFruit[0])) + " grams"))
    MassText.set(strCalorie)
    MassTextdisplay = tk.Label(root, font=("Arial", 13), textvariable=MassText)
    MassTextdisplay.place(x = 850,y = 545)
    
    
    LineImagePath = os.path.join(CurrentFolderPath,'GUI_Elements','Line.jpg')
    LineImg = ImageTk.PhotoImage(Image.open(LineImagePath))
    LineImgLabel = tk.Label(root, image = LineImg)
    LineImgLabel.image = LineImg
    LineImgLabel.place(x = 725,y = 100)
    


    DetectedSide_im = DetectedSide_im_pil.resize((316, 212), Image.ANTIALIAS) 
    DetectedSide_im2 = ImageTk.PhotoImage(DetectedSide_im)
    DetectedSideLabel1 = tk.Label(root, height=212, width=316, image = DetectedSide_im2)
    DetectedSideLabel1.image = DetectedSide_im2
    DetectedSideLabel1.place(x = 45,y = 100)   
       
    DetectedTop_im = DetectedTop_im_pil.resize((316, 212), Image.ANTIALIAS) 
    DetectedTop_im2 = ImageTk.PhotoImage(DetectedTop_im) 
    DetectedTopLabel1 = tk.Label(root, height=212, width=316, image = DetectedTop_im2)
    DetectedTopLabel1.image = DetectedTop_im2
    DetectedTopLabel1.place(x = 385,y = 100) 
    
    
    ObjectDetectionResultsText = tk.StringVar()
    ObjectDetectionResultsText.set("Object detection Results")
    ObjectDetectionResultsTextdisplay = tk.Label(root, font=("Arial", 15), textvariable=ObjectDetectionResultsText)
    ObjectDetectionResultsTextdisplay.place(x = 260,y = 317)
    
    
    
    
    
    SegmentedSide_im = SegmentedSide_im_pil.resize((316, 212), Image.ANTIALIAS) 
    SegmentedSide_im2 = ImageTk.PhotoImage(SegmentedSide_im)
    SegmentedSideLabel1 = tk.Label(root, height=212, width=316, image = SegmentedSide_im2)
    SegmentedSideLabel1.image = SegmentedSide_im2
    SegmentedSideLabel1.place(x = 45,y = 350)    
    
    
    SegmentedTop_im = SegmentedTop_im_pil.resize((316, 212), Image.ANTIALIAS) 
    SegmentedTop_im2 = ImageTk.PhotoImage(SegmentedTop_im)
    SegmentedTopLabel1 = tk.Label(root, height=212, width=316, image = SegmentedTop_im2)
    SegmentedTopLabel1.image = SegmentedTop_im2
    SegmentedTopLabel1.place(x = 385,y = 350)

    
    SegmentationResultsText = tk.StringVar()
    SegmentationResultsText.set("Segmentation Results")
    SegmentationResultsTextdisplay = tk.Label(root, font=("Arial", 15), textvariable=SegmentationResultsText)
    SegmentationResultsTextdisplay.place(x = 265,y = 568)
        
    
    

    
    


def SegmentPictures(FruitObject1,FruitObject2):
    global SegmentedSideLabel, SegmentedTopLabel, NextbtnImgBtn3 , SegmentedFruitText
    global SegmentedSideImageBGR,SegmentedTopImageBGR
    
    global SegmentedSide_im_pil,SegmentedSide_im,SegmentedSide_im2
    global SegmentedTop_im_pil,SegmentedTop_im,SegmentedTop_im2
    
    SegmentedSideImageBGR = FruitObject1.segmentAuto()
    SegmentedTopImageBGR= FruitObject2.segmentAuto()
    
    #Converting images to RGB so it is displayed with its real colors in th PIL version of the images
    SegmentedSideImageRGB = cv2.cvtColor(SegmentedSideImageBGR, cv2.COLOR_BGR2RGB)
    SegmentedTopImageRGB = cv2.cvtColor(SegmentedTopImageBGR, cv2.COLOR_BGR2RGB)
    
    
    #Stopping and destroying the thread of the Gif loading pic 
    #l.stop_thread()
    l.destroy()
    
    #Destroying the Please wait text label
    WaitTextdisplay.destroy()
    
    #Displaying the segmented side Image
    SegmentedSide_im_pil = Image.fromarray(SegmentedSideImageRGB)
    SegmentedSide_im = SegmentedSide_im_pil.resize((590, 443), Image.ANTIALIAS) 
    SegmentedSide_im2 = ImageTk.PhotoImage(SegmentedSide_im)
    SegmentedSideLabel = tk.Label(root, height=443, width=590, image = SegmentedSide_im2)
    SegmentedSideLabel.image = SegmentedSide_im2
    SegmentedSideLabel.place(x = 45,y = 98)
    
    
    #Displaying the segmented Top Image
    SegmentedTop_im_pil = Image.fromarray(SegmentedTopImageRGB)
    SegmentedTop_im = SegmentedTop_im_pil.resize((590, 443), Image.ANTIALIAS) 
    SegmentedTop_im2 = ImageTk.PhotoImage(SegmentedTop_im)
    SegmentedTopLabel = tk.Label(root, height=443, width=590, image = SegmentedTop_im2)
    SegmentedTopLabel.image = SegmentedTop_im2
    SegmentedTopLabel.place(x = 665,y = 98) 
    
    #Displaying the next button that proceed to page 4
    NextbtnImagePath3 = os.path.join(CurrentFolderPath,'GUI_Elements','NextButton.png')
    NextbtnImg3 = PhotoImage(file = NextbtnImagePath3)
    NextbtnImgBtn3 = tk.Button(root,image =NextbtnImg3,command = lambda: DisplayCalorieResults(FruitObject1,FruitObject1),highlightthickness = 0, bd = 0)
    NextbtnImgBtn3.image = NextbtnImg3 #VERY IMPOOORTANT!!! # keep a reference!
    NextbtnImgBtn3.place(x = 1040,y = 560)
    
    #Text that says the Segmentation Results
    SegmentedFruitText = tk.StringVar()
    SegmentedFruitText.set("These are the segmentation results of the detected fruit")
    SegmentedFruitText = tk.Label(root, font=("Arial", 13), textvariable=SegmentedFruitText)
    SegmentedFruitText.place(x = 45,y = 560)


def ProceedToPage3(FruitObject1,FruitObject2):
    global l,WaitTextdisplay
    
    #Deleting all the labels and buttons of the previous page
    DetectedFruitTextLabel.destroy()
    DetectedSideLabel.destroy()
    DetectedTopLabel.destroy()
    NextbtnImgBtn2.destroy()
    
    
    ImagePath = os.path.join(CurrentFolderPath,'GUI_Elements','loader.gif')
    # l = AnimateGIF.AnimatedGIF(root, ImagePath)
    l = AnimatedGif.AnimatedGif(root, ImagePath, 0.02)
    l.start_thread()
    l.pack()
    l.place(x = 535,y = 150)  
   
    
    #Displaying the Please wait text label
    WaitText = tk.StringVar()
    WaitText.set("Please wait, The segmentation will take few seconds...")
    WaitTextdisplay = tk.Label(root, font=("Arial", 13), textvariable=WaitText)
    WaitTextdisplay.place(x = 465,y = 400)
    
    
    t2 = threading.Thread(target=SegmentPictures, args =(FruitObject1,FruitObject2))
    t2.start()
    
    
    


def the_process_function():
        global Img1,Img2,DetectedSideLabel,DetectedTopLabel,NextbtnImgBtn2,DetectedFruitTextLabel
        global DetectedSide_im_pil,DetectedSide_im,DetectedSide_im2
        global DetectedTop_im_pil,DetectedTop_im,DetectedTop_im2
        
        StopThread = False
        
        #Running the detection process on both pictures on a thread
        while StopThread is False:
            FO1 = Fruit_Object_detection.FruitObjectDetection()
            FO1.uploadImage(SideViewImagePath)
            FO1.getCoordinates()
            Img1 = FO1.getDetectedImage() 
            FO2 = Fruit_Object_detection.FruitObjectDetection()
            FO2.uploadImage(TopViewImagePath)
            FO2.getCoordinates()
            Img2 = FO2.getDetectedImage()
            StopThread = True
        
        
       #Stopping and destroying the thread of the Gif loading pic 
        l.stop_thread()
        l.destroy()
               
       #Destroying the Please wait text label
        WaitTextdisplay.destroy()
        
        
       #Displaying the Side view image after being detected
        DetectedSideimg = cv2.cvtColor(Img1, cv2.COLOR_BGR2RGB)
        DetectedSide_im_pil = Image.fromarray(DetectedSideimg)
        DetectedSide_im = DetectedSide_im_pil.resize((590, 443), Image.ANTIALIAS) 
        DetectedSide_im2 = ImageTk.PhotoImage(DetectedSide_im)
        DetectedSideLabel = tk.Label(root, height=443, width=590, image = DetectedSide_im2)
        DetectedSideLabel.image = DetectedSide_im2
        DetectedSideLabel.place(x = 45,y = 98)   
       
        
        #Displaying the Top view image after being detected
        DetectedTopimg = cv2.cvtColor(Img2, cv2.COLOR_BGR2RGB)
        DetectedTop_im_pil = Image.fromarray(DetectedTopimg)
        DetectedTop_im = DetectedTop_im_pil.resize((590, 443), Image.ANTIALIAS) 
        DetectedTop_im2 = ImageTk.PhotoImage(DetectedTop_im) 
        DetectedTopLabel = tk.Label(root, height=443, width=590, image = DetectedTop_im2)
        DetectedTopLabel.image = DetectedTop_im2
        DetectedTopLabel.place(x = 661,y = 98) 
        
        #Making Sure that both pictures hold the same kind of fruit  
        DetectedFruitSide = FO1.getFruit()
        DetectedFruitTop = FO2.getFruit()
        
        print(DetectedFruitSide)
        print(DetectedFruitTop)
        
        if(DetectedFruitSide == [] and DetectedFruitTop != []):
             DetectedFruitText = tk.StringVar()
             DetectedFruitText.set("Error: *Can't Detect Fruit in the first image")
             DetectedFruitTextLabel = tk.Label(root, font=("Arial", 13), textvariable=DetectedFruitText)
             DetectedFruitTextLabel.config(fg="red")
             DetectedFruitTextLabel.place(x = 45,y = 560)
        
        elif(DetectedFruitSide != [] and DetectedFruitTop == [] ):
             DetectedFruitText = tk.StringVar()
             DetectedFruitText.set("Error: *Can't Detect Fruit in the second image")
             DetectedFruitTextLabel = tk.Label(root, font=("Arial", 13), textvariable=DetectedFruitText)
             DetectedFruitTextLabel.config(fg="red")
             DetectedFruitTextLabel.place(x = 45,y = 560)
        
        elif(DetectedFruitSide == [] and DetectedFruitTop == []):
             DetectedFruitText = tk.StringVar()
             DetectedFruitText.set("Error: *Can't Detect Fruit in both images")
             DetectedFruitTextLabel = tk.Label(root, font=("Arial", 13), textvariable=DetectedFruitText)
             DetectedFruitTextLabel.config(fg="red")
             DetectedFruitTextLabel.place(x = 45,y = 560)
             
    
        elif(DetectedFruitSide[0] == DetectedFruitTop[0]):
            
            if(FO1.CheckCoinAvailability() == False and FO2.CheckCoinAvailability() == True):
                 DetectedFruitText = tk.StringVar()
                 DetectedFruitText.set("The detected fruit is " +DetectedFruitSide[0] + " but there is no coin in the first picture" )
                 DetectedFruitTextLabel = tk.Label(root, font=("Arial", 13), textvariable=DetectedFruitText)
                 DetectedFruitTextLabel.config(fg="red")
                 DetectedFruitTextLabel.place(x = 45,y = 560)
            
            
            elif(FO1.CheckCoinAvailability() == True and FO2.CheckCoinAvailability() == False):
                 DetectedFruitText = tk.StringVar()
                 DetectedFruitText.set("The detected fruit is " +DetectedFruitSide[0] + " but there is no coin in the second picture" )
                 DetectedFruitTextLabel = tk.Label(root, font=("Arial", 13), textvariable=DetectedFruitText)
                 DetectedFruitTextLabel.config(fg="red")
                 DetectedFruitTextLabel.place(x = 45,y = 560)
            
            
            elif(FO1.CheckCoinAvailability() == False and FO2.CheckCoinAvailability() == False):
                 DetectedFruitText = tk.StringVar()
                 DetectedFruitText.set("The detected fruit is " +DetectedFruitSide[0] + " but there is no coin both pictures" )
                 DetectedFruitTextLabel = tk.Label(root, font=("Arial", 13), textvariable=DetectedFruitText)
                 DetectedFruitTextLabel.config(fg="red")
                 DetectedFruitTextLabel.place(x = 45,y = 560)
            
            else:
            
               StrDetectedFruit = ("The detected fruit in the two pictures is " + DetectedFruitSide[0])
               #Displaying the text that tells the detected fruit in both pictures
               
               DetectedFruitText = tk.StringVar()
               DetectedFruitText.set(StrDetectedFruit)
               DetectedFruitTextLabel = tk.Label(root, font=("Arial", 13), textvariable=DetectedFruitText)
               DetectedFruitTextLabel.place(x = 45,y = 560)
               
               
               
               #Displaying the next button that navigate to page 3
               NextbtnImagePath2 = os.path.join(CurrentFolderPath,'GUI_Elements','NextButton.png')
               NextbtnImg2 = PhotoImage(file = NextbtnImagePath2)
               NextbtnImgBtn2 = tk.Button(root,image =NextbtnImg2,command = lambda: ProceedToPage3(FO1,FO2),highlightthickness = 0, bd = 0)
               NextbtnImgBtn2.image = NextbtnImg2 #VERY IMPOOORTANT!!! # keep a reference!
               NextbtnImgBtn2.place(x = 1040,y = 560)
           
        else:
            
            DetectedFruitText = tk.StringVar()
            DetectedFruitText.set("Error: *The type of fruit in the top and side picture is unmatched")
            DetectedFruitTextLabel = tk.Label(root, font=("Arial", 13), textvariable=DetectedFruitText)
            DetectedFruitTextLabel.config(fg="red")
            DetectedFruitTextLabel.place(x = 45,y = 560)
    
          
        if(t1.isAlive()):
            print("Thread is live")
        else:
            print("Thread is dead")
    
        


def ProceedToPage2():
    global Img1,Img2,l,WaitTextdisplay,ErrorText,ErrorTextdisplay
    
    if(UploadSidePicFlag == False and UploadTopPicFlag == True):    
        ErrorTextdisplay.destroy()
        ErrorText.set("*Please upload the side View picture")
        ErrorTextdisplay = tk.Label(root, font=("Arial", 13), textvariable=ErrorText)
        ErrorTextdisplay.config(fg="red")
        ErrorTextdisplay.place(x = 45,y = 590)
        
    elif(UploadSidePicFlag == True and UploadTopPicFlag == False):    
        ErrorTextdisplay.destroy()
        ErrorText.set("*Please upload the Top View picture")
        ErrorTextdisplay = tk.Label(root, font=("Arial", 13), textvariable=ErrorText)
        ErrorTextdisplay.config(fg="red")
        ErrorTextdisplay.place(x = 45,y = 590)
        
    elif(UploadSidePicFlag == False and UploadTopPicFlag == False):
        ErrorTextdisplay.destroy()
        ErrorText.set("*There is no pictures uploaded")
        ErrorTextdisplay = tk.Label(root, font=("Arial", 13), textvariable=ErrorText)
        ErrorTextdisplay.config(fg="red")
        ErrorTextdisplay.place(x = 45,y = 590)
        
    elif(UploadSidePicFlag == True and UploadTopPicFlag == True):
        #Deleting all the labels of Page1
        ErrorTextdisplay.destroy()
        NextbtnImgBtn.destroy()
        TopViewImgLabel.destroy()
        SideViewImgLabel.destroy()
        TipsTextdisplay.destroy()
        
        ImagePath = os.path.join(CurrentFolderPath,'GUI_Elements','loader.gif')
        # l = AnimateGIF.AnimatedGIF(root, ImagePath)
        l = AnimatedGif.AnimatedGif(root, ImagePath, 0.02)
        l.start_thread()
        l.pack()
        l.place(x = 535,y = 150)  
       
        

        #Displaying the Please wait text label
        WaitText = tk.StringVar()
        WaitText.set("Please wait, The detection will take few seconds...")
        WaitTextdisplay = tk.Label(root, font=("Arial", 13), textvariable=WaitText)
        WaitTextdisplay.place(x = 465,y = 400)
          
        t1 = threading.Thread(target=the_process_function)
        t1.start()



#--------------------------------Page1 in the program--------------------------------------------
    
#Displaying the nav bar at the top of the app window
NavBarImagePath = os.path.join(CurrentFolderPath,'GUI_Elements','HomeLogoBar.png')
NavBarImg = ImageTk.PhotoImage(Image.open(NavBarImagePath))
panel = tk.Label(root, image = NavBarImg)
panel.pack(side = "top", fill = "both", expand = "no")


#Displaying the Side Image Upload Button on the left of the window
UploadSideImagePath = os.path.join(CurrentFolderPath,'GUI_Elements','UploadSidePic.png')
UploadSideImg = ImageTk.PhotoImage(Image.open(UploadSideImagePath))
UploadSideImgBtn = tk.Button(root,image=UploadSideImg, command = UploadSideImage, highlightthickness = 0, bd = 0)
UploadSideImgBtn.image = UploadSideImg
UploadSideImgBtn.place(x = 45,y = 100)


#Displaying the Top Image Upload Button on the right of the window
UploadTopImagePath = os.path.join(CurrentFolderPath,'GUI_Elements','UploadTopPic.png')
UploadTopImg = ImageTk.PhotoImage(Image.open(UploadTopImagePath))
UploadTopImgBtn = tk.Button(root,image=UploadTopImg, command = UploadTopImage, highlightthickness = 0, bd = 0)
UploadTopImgBtn.image = UploadTopImg
UploadTopImgBtn.place(x = 665,y = 100)


#Displaying the Next Button at the bottom of the window
NextbtnImagePath = os.path.join(CurrentFolderPath,'GUI_Elements','NextButton.png')
NextbtnImg = ImageTk.PhotoImage(Image.open(NextbtnImagePath))
NextbtnImgBtn = tk.Button(root,height=70, width=212, image=NextbtnImg, command = ProceedToPage2, highlightthickness = 0, bd = 0)
NextbtnImgBtn.image = NextbtnImg
NextbtnImgBtn.place(x = 1040,y = 560)


#Displaying the Text at the bottom of the window
TipsText = tk.StringVar()
TipsText.set(" Please upload the first picture and the second picture")
TipsTextdisplay = tk.Label(root, font=("Arial", 13), textvariable=TipsText)
TipsTextdisplay.place(x = 45,y = 560)


#Displaying the Error Text at the bottom of the window
ErrorText = tk.StringVar()
ErrorText.set("")
ErrorTextdisplay = tk.Label(root, font=("Arial", 13), textvariable=ErrorText)


DetectedFruitText = tk.StringVar()
DetectedFruitText.set("")
DetectedFruitTextLabel = tk.Label(root, font=("Arial", 13), textvariable=DetectedFruitText)
DetectedFruitTextLabel.place(x = 45,y = 560)



#For keeping the window running and not to be closed immedietly 
root.mainloop()