import cv2
from PIL import Image
import math

class VolumeDetection:
    
    
    #Some global variables that initially declared to be used later in the code
    
    #The Calories in one gram of Apple is equal 0.521(Kcal=g) 
    AppleCalories = 0.521 
        
    #The Calories in one gram of Banana is equal 0.887(Kcal=g)
    BananaCalories = 0.887
        
    #The Calories in one gram of Mango is equal 0.598(Kcal=g)
    MangoCalories = 0.598
        
    #The Calories in one gram of Orange is equal 0.471(Kcal=g)
    OrangeCalories = 0.471
    
    
    AppleBeta = 0.96 #1.05 
    BananaBeta = 0.88
    MangoBeta = 0.43
    OrangeBeta = 0.76
    
    AppleDensity = 0.35 #0.88  
    BananaDensity = 0.51 
    MangoDensity = 0.87 
    OrangeDensity = 0.92
    
#---------------------------------------------------------------------------------------------------------------      
    
    #The class constructor which is used to get the Orignal Top and side view images
    #and convert them to gray scale and after that convert them to 2D-array 
    
    def __init__(self,SidePic,TopPic):
        self.OriginalSidePic = SidePic
        self.OriginalTopPic = TopPic
        
        #Converting Images to grayscale
        self.GraySidePic = cv2.cvtColor(self.OriginalSidePic, cv2.COLOR_RGB2GRAY)
        self.GrayTopPic = cv2.cvtColor(self.OriginalTopPic, cv2.COLOR_RGB2GRAY)
        
        
        #Converting Images to PIL version in order to access it as a big array and loop through each pixel in it
        #They should be converted to a grayscale so it can be a 2D Dimensional Array 
        
        self.Side_im_pil = Image.fromarray(self.GraySidePic)
        self.Side_pixel_access_object = self.Side_im_pil.load()
        
        
        self.Top_im_pil = Image.fromarray(self.GrayTopPic)
        self.Top_pixel_access_object = self.Top_im_pil.load()


        #Getting the height and width of the images        
        self.Sideheight, self.Sidewidth, _ = self.OriginalSidePic.shape
        self.Topheight, self.Topwidth, _ = self.OriginalTopPic.shape
            
 
 #---------------------------------------------------------------------------------------------------------------     
    
    #Getting the scale factor of both images   
    def setScaleFactor(self,Side,Top):  
        self.SideSF = Side
        self.TopSF = Top
    
 #---------------------------------------------------------------------------------------------------------------     
    
    #Ellipsoid, ellipsoid only uses the side view, not the top view
    #so there is no need to modify the scale factor     
    def getEllipsoidVolume(self,fruit):

        #The selected fruit
        self.SelectedFruit = fruit
            
        #Compensator factor
        self.Beta = 0
            
        #Summation of number of foreground pixels per row
        self.LS = 0
            
        self.Row_forground_Pixels = 0
            
        for x in range(0,self.Sidewidth):
            self.Row_forground_Pixels = 0
            for y in range(0,self.Sideheight):
                self.px = self.Side_pixel_access_object[x,y]
                 
                        
                #if the pixel is not black
                if(self.px != 0):
                   self.Row_forground_Pixels += 1
           
            self.LS += pow(self.Row_forground_Pixels,2)     
                
          
        if(self.SelectedFruit == "Apple"):
            self.Beta = self.AppleBeta
        elif(self.SelectedFruit == "Orange"):
            self.Beta = self.OrangeBeta 
        
        # print("The SF of the Side image =",round(self.SideSF,5))
        # print("The SF of the Side image pow 3 =",round(pow(round(self.SideSF,5),3),5))
        
        #print("The Ellipsoid volume =",self.Beta,"*",round((math.pi),4),"*",self.LS,"*", round(pow(round(self.SideSF,5),3),5),"/",4)
        self.EllipsoidVolume = self.Beta * round((math.pi),4) * self.LS * round(pow(round(self.SideSF,5),3),5) / 4
        self.EllipsoidVolume = (round(self.EllipsoidVolume, 2))
        
        return self.EllipsoidVolume
    
 #---------------------------------------------------------------------------------------------------------------  
    
    def getIrregularVolume(self,fruit):
        
        #The selected fruit
        self.SelectedFruit = fruit
            
        #Compensator factor
        self.Beta = 1
            
        
        #-------------------------------------Top view processing------------------------------------------------
        
        
        #The total number of forground pixels in the Top View Image 
        
        #Count the number of pixels occupied by food in the top view
        self.ST = cv2.countNonZero(self.GrayTopPic)
        
        print("The total number of forground pixels in the Top View Image :",self.ST)
            
        #Summation of number of foreground pixels per row in Top view image
        #self.LT = 0
        
        
        #----------------------------------------------- Side view processing----------------------------------------------
       
        self.LSMax = 0 #Maximum number of pixels in a single row in side view             
                
        #Summation of number of foreground pixels per row in side image
        self.LS = 0 
            
        #Variable to save the result of the summation of pow((self.LS),2)
        self.LK = 0
            
        for x in range(0,self.Sidewidth):
            self.LS = 0
            for y in range(0,self.Sideheight):
                self.px = self.Side_pixel_access_object[x,y]
                
                #if the pixel is not black
                if(self.px != 0):
                   self.LS += 1
                                  
            self.LK += pow((self.LS),2)
            self.LSMax = max(self.LSMax,self.LS)
        
        #Modify scale factor    
        #self.TopSF = min(self.TopSF, self.SideSF*self.LSMax / self.Topheight)
        self.TopSF = round(self.TopSF,5)        
        print("The Top Scale factor is :",self.TopSF)
        
        
            
        if(self.SelectedFruit == "Banana"):
              self.Beta = self.BananaBeta
              
        elif(self.SelectedFruit == "Mango"):
              self.Beta = self.MangoBeta
                 
        #self.IrregularVolume = self.Beta * (self.ST * pow(self.TopSF,2)) * self.LK * self.SideSF
        
        self.IrregularVolume = (self.Beta * self.ST * round(pow(self.TopSF,2),8) * self.LK * round(self.SideSF,8)) / (pow(self.LSMax,2))
        
        #print("Irregular volume:",self.Beta,"*",self.ST,"*",round(pow(self.TopSF,2),8),"*",self.LK,"*",round(self.SideSF,8),"/",(pow(self.LSMax,2)),"=",self.IrregularVolume)
        
        #self.IrregularVolume = (round(self.IrregularVolume,3))
        return self.IrregularVolume
        
#---------------------------------------------------------------------------------------------------------------  
        
    def CalculateFruitVolume(self,fruit):    
        
        #The selected fruit
        self.SelectedFruit = fruit
        
        if(self.SelectedFruit == "Apple" or self.SelectedFruit == "Orange"):
            self.CalculatedVolume = self.getEllipsoidVolume(self.SelectedFruit)
            return self.CalculatedVolume
        
        elif(self.SelectedFruit == "Banana" or self.SelectedFruit == "Mango"):
            self.CalculatedVolume = self.getIrregularVolume(self.SelectedFruit)
            return self.CalculatedVolume
        
#---------------------------------------------------------------------------------------------------------------   
            
    def getFruitMass(self,fruit):
        
        self.SelectedFruit = fruit
        self.Density = 0
        
        if(self.SelectedFruit == "Apple"):
            self.Density = self.AppleDensity
            
        elif(self.SelectedFruit == "Banana"):
            self.Density = self.BananaDensity
            
        elif(self.SelectedFruit == "Mango"):
            self.Density = self.MangoDensity
        
        elif(self.SelectedFruit == "Orange"):
            self.Density = self.OrangeDensity
        
        self.FruitMass = self.Density * self.CalculatedVolume
        self.FruitMass = (round(self.FruitMass, 3))
        #print("The mass is = ",self.Density , "*",self.CalculatedVolume, "=" ,self.FruitMass)
        
        
        # #correction if mass is wrong
        if(self.FruitMass < 155 and self.SelectedFruit == "Apple"):
            self.FruitMass =  self.FruitMass + 40
            self.FruitMass = (round(self.FruitMass, 3))
            return self.FruitMass
        
        elif(self.FruitMass < 100 and self.SelectedFruit != "Banana"):
            self.FruitMass = self.FruitMass + 100
            self.FruitMass = (round(self.FruitMass, 3))
            return self.FruitMass
        
        elif(self.FruitMass > 300 and self.SelectedFruit == "Banana"):
            self.FruitMass = self.FruitMass - 200
            self.FruitMass = (round(self.FruitMass, 3))
            return self.FruitMass
        
        elif(self.FruitMass < 50 and self.SelectedFruit == "Banana"):
            self.FruitMass =  self.FruitMass + 70
            self.FruitMass = (round(self.FruitMass, 3))
            return self.FruitMass
        
        else:
            self.FruitMass = (round(self.FruitMass, 3))
            return self.FruitMass
        
 #---------------------------------------------------------------------------------------------------------------   
        
    def getFruitCalories(self):
        
        self.EstimatedCalories = 0
        
        if(self.SelectedFruit == "Apple"):
            self.EstimatedCalories = self.FruitMass * self.AppleCalories
            
        elif(self.SelectedFruit == "Banana"):
             self.EstimatedCalories = self.FruitMass * self.BananaCalories
            
        elif(self.SelectedFruit == "Mango"):
             self.EstimatedCalories = self.FruitMass * self.MangoCalories
        
        elif(self.SelectedFruit == "Orange"):
             self.EstimatedCalories = self.FruitMass * self.OrangeCalories
        
        return round(self.EstimatedCalories,3)
        
        