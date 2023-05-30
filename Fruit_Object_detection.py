import os
import cv2
import numpy as np
import tensorflow as tf
import sys
import matplotlib
matplotlib.use('Agg')

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")
from utils import label_map_util
from utils import visualization_utils as vis_util


class FruitObjectDetection:
    
    #Some global variables that initially declared to be used later in the code
    
    ImagePath = ''
    boxes = []
    scores = []
    classes = []
    num = 0
    CoinAvailable = False
    
#---------------------------------------------------------------------------------------------------------------    
    
    #The Constuctor of this Class
    #It is used for connecting with the trained folder and loading the tensorflow into memory
    
    def __init__(self):
        CurrentFolderPath = os.getcwd()
        
        self.DetectedFruit = []

        #The Whole path to the detection file
        self.FruitDetectionFile = os.path.join(CurrentFolderPath,'inference_graph','frozen_inference_graph.pb')
        
        # Path to label map file
        self.LabelsFile = os.path.join(CurrentFolderPath,'training','labelmap.pbtxt')
        
        #The number of classes that can be detected
        self.NumOfClasses = 5
        
        # Load the label map.
        # Label maps map indices to category names, so that when our convolution
        # network predicts `5`, we know that this corresponds to `coin`.
        # Here we use internal utility functions, but anything that returns a
        # dictionary mapping integers to appropriate string labels would be fine
        
        label_map = label_map_util.load_labelmap(self.LabelsFile)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=self.NumOfClasses, use_display_name=True)
        self.category_index = label_map_util.create_category_index(categories)
        
        
        # Load the Tensorflow model into memory.
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.compat.v1.GraphDef()
            with tf.io.gfile.GFile(self.FruitDetectionFile, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
        
            self.sess = tf.compat.v1.Session(graph=detection_graph)
            
         
        # Define input and output tensors (i.e. data) for the object detection classifier
        # Input tensor is the image
        self.image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        
        # Output tensors are the detection boxes, scores, and classes
        # Each box represents a part of the image where a particular object was detected
        self.detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        
        # Each score represents level of confidence for each of the objects.
        # The score is shown on the result image, together with the class label.
        self.detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        self.detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
        
        # Number of objects detected
        self.num_detections = detection_graph.get_tensor_by_name('num_detections:0')    


#--------------------------------------------------------------------------------------------------------------        
    
    #Checking the size of the image, if it is large then set it to 816 x 612 dimensions
    #The program spend more detection time if the image is large and it can produce un wanted results
    
    def CheckImageSize(self,Img):
        self.ImgHeight, self.ImgWidth, _ = Img.shape
        
        #Rotate the image if the height is more than the width
        if(self.ImgHeight > self.ImgWidth):
            self.Img = cv2.rotate(self.Img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)

          
        #The default Image size that the image should be resized to
        self.dim = (816,612) 
        self.ResizedImg = cv2.resize(Img,self.dim,interpolation = cv2.INTER_AREA)
        
        return self.ResizedImg
        
#----------------------------------------------------------------------------------------------------------        
        
    def uploadImage(self,path):
        
        self.ImagePath = path
        self.Image = cv2.imread(self.ImagePath)
        
        #We use the function that wrote before to edit the image size
        self.Image = self.CheckImageSize(self.Image)
        
        #Convert the image to RGB format
        self.Image_rgb = cv2.cvtColor(self.Image, cv2.COLOR_BGR2RGB)
        self.Image_expanded = np.expand_dims(self.Image_rgb, axis=0)
        (self.boxes, self.scores, self.classes, self.num) = self.sess.run(
        [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
        feed_dict={self.image_tensor: self.Image_expanded})
        
#----------------------------------------------------------------------------------------------------------    
        
    def getCoordinates(self):
         
        #We get an array holding the coordinates of the detected bounding boxs in which 
        #the object detector is sure about them by minmium percentage of 60%
        
        self.coordinates = vis_util.visualize_boxes_and_labels_on_image_array(
        self.Image,
        np.squeeze(self.boxes),
        np.squeeze(self.classes).astype(np.int32),
        np.squeeze(self.scores),
        self.category_index,
        use_normalized_coordinates=True,
        line_thickness=5,
        min_score_thresh=0.60) #0.60
        
        #We use this part to check the coordinates of each box and write 
        #which coordinate belong to which object in the console.
        #We create an Array called DetectedFruit, and we append the names of the detected fruits in it
        
        for i in self.coordinates:
            if "Apple" in i[0]:
                FruitCoordinates = i
                
                self.startingPoint_x = FruitCoordinates[1]
                self.startingPoint_y = FruitCoordinates[2]
                self.endingPoint_x = FruitCoordinates[3]
                self.endingPoint_y = FruitCoordinates[4]
                

                self.DetectedFruit.append("Apple")
                print("The coordinates of the Apple is : (",self.startingPoint_x,",",self.startingPoint_y,",",self.endingPoint_x,",",self.endingPoint_y,")")
                
            if "Banana" in i[0]:
                FruitCoordinates = i
                
                self.startingPoint_x = FruitCoordinates[1]
                self.startingPoint_y = FruitCoordinates[2]
                self.endingPoint_x = FruitCoordinates[3]
                self.endingPoint_y = FruitCoordinates[4]
                

                self.DetectedFruit.append("Banana")
                
                print("The coordinates of the Banana is : (",self.startingPoint_x,",",self.startingPoint_y,",",self.endingPoint_x,",", self.endingPoint_y,")")
            
            if "Orange" in i[0]:
                FruitCoordinates = i
                
                self.startingPoint_x = FruitCoordinates[1]
                self.startingPoint_y = FruitCoordinates[2]
                self.endingPoint_x = FruitCoordinates[3]
                self.endingPoint_y = FruitCoordinates[4]
                

                self.DetectedFruit.append("Orange")
                
                print("The coordinates of the Orange is : (",self.startingPoint_x,",",self.startingPoint_y,",",self.endingPoint_x,"," ,self.endingPoint_y,")")
                
            
            if "Mango" in i[0]:
                FruitCoordinates = i
                
                self.startingPoint_x = FruitCoordinates[1]
                self.startingPoint_y = FruitCoordinates[2]
                self.endingPoint_x = FruitCoordinates[3]
                self.endingPoint_y = FruitCoordinates[4]
                
                self.DetectedFruit.append("Mango")
                
                print("The coordinates of the Mango is : (",self.startingPoint_x,",",self.startingPoint_y,",",self.endingPoint_x,",",self.endingPoint_y,")")
                
                
            if "Coin" in i[0]:
                FruitCoordinates = i  
                self.CoinAvailable = True
                
                self.Coin_startingPoint_x = FruitCoordinates[1]
                self.Coin_startingPoint_y = FruitCoordinates[2]
                self. Coin_endingPoint_x = FruitCoordinates[3]
                self. Coin_endingPoint_y = FruitCoordinates[4]
                print("The coordinates of the Coin is : (",self.Coin_startingPoint_x,",",self.Coin_startingPoint_y,",",self.Coin_endingPoint_x,",",self.Coin_endingPoint_y,")")
    
#----------------------------------------------------------------------------------------------------------      
    #Checking if the coin is available or not in the image
    def CheckCoinAvailability(self):
        if(self.CoinAvailable == True):
            return True
        else:
            return False

#----------------------------------------------------------------------------------------------------------          
    
    def getFruit(self):
        return self.DetectedFruit

#----------------------------------------------------------------------------------------------------------             

    def getDetectedImage(self):
        return self.Image

#----------------------------------------------------------------------------------------------------------      
    
    def getCoinScaleFactor(self):
        self.CoinWidth = self.Coin_endingPoint_x - self.Coin_startingPoint_x
        self.CoinHeight = self.Coin_endingPoint_y - self.Coin_startingPoint_y
        
        self.ScaleFactor = 2.5/((self.CoinWidth+self.CoinHeight)/2)
        #self.ScaleFactor = (round(self.ScaleFactor,5))
        
        return self.ScaleFactor
 
#----------------------------------------------------------------------------------------------------------      
    
    def segmentAuto(self):
        
        #getting the original Image again
        self.Image2 = cv2.imread(self.ImagePath)
        
        #We use the function that wrote before to edit the image size
        self.Image2 = self.CheckImageSize(self.Image2)
        
        
        self.mask = np.zeros(self.Image2.shape[:2],np.uint8)
        self.bgdModel = np.zeros((1,65),np.float64)
        self.fgdModel = np.zeros((1,65),np.float64)
        
        
        #Creating a rectange with the dimensions of the bounding box 
        self.rect = (self.startingPoint_x, self.startingPoint_y, self.endingPoint_x, self.endingPoint_y)
        
        
        cv2.grabCut(self.Image2,self.mask,self.rect,self.bgdModel,self.fgdModel,8,cv2.GC_INIT_WITH_RECT)
    
        self.mask2 = np.where((self.mask==2)|(self.mask==0),0,1).astype('uint8')
        self.Image2 = self.Image2*self.mask2[:,:,np.newaxis]
        
        #crop the fruit portion segmentation and ignore the other parts in the image that is far away from the fruit
        self.crop_image =  self.Image2[self.startingPoint_y:self.endingPoint_y, self.startingPoint_x:self.endingPoint_x]
        
        #getting the actual height and width of the image
        self.h, self.w, _ = self.Image2.shape
        
        #creating a new black image with the same dimensions of the original image
        self.ClearBlackOutput = np.zeros((self.h, self.w, 3), dtype = "uint8") 
        
        #adding the cropped fruit to the same area of the black image
        self.ClearBlackOutput[self.startingPoint_y:self.endingPoint_y, self.startingPoint_x:self.endingPoint_x] = self.crop_image
        

        #For Enhancing the automatic grabCut, This code is made to remove the white remaining background
        #We convert the image into HSV format and then we give a color range that if a pixel color
        #exist in this color range, it is converted to black. 
        
        #Since some fruits have bright colors, it may lose some pixels because it can be found in the 
        #range, thats why we give a color range for each fruit color to keep the colored pixels of the fruit
        
        hsv = cv2.cvtColor(self.ClearBlackOutput, cv2.COLOR_BGR2HSV)
        
        if(self.DetectedFruit[0] == "Apple"):
            lower_blue = np.array([0, 0, 85])
            upper_blue = np.array([180, 56, 255])
        
        elif(self.DetectedFruit[0] == "Banana"):
            lower_blue = np.array([0, 0, 85])
            upper_blue = np.array([180, 85, 255])
            
        elif(self.DetectedFruit[0] == "Orange"):
            lower_blue = np.array([0, 0, 85])
            upper_blue = np.array([180, 66, 255])  
            
        elif(self.DetectedFruit[0] == "Mango"):
            lower_blue = np.array([0, 0, 85])
            upper_blue = np.array([180, 66, 255])      
            
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        result = cv2.bitwise_and(self.ClearBlackOutput, self.ClearBlackOutput, mask=mask)
        b, g, r = cv2.split(result)  
        filter = g.copy()
        
        #We apply the thresholding technique to remove the pixels that are in the color range
        ret,mask = cv2.threshold(filter,10,255, 1)
        
        self.ClearBlackOutput[mask == 0] = 0
        
        
        #we out put the image after the segmentation
        return self.ClearBlackOutput
    
    
   
        

































