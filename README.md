# Blood Group Identification Web App

This web application uses image processing techniques 

to identify a person's blood group based on an uploaded ABD test cell image. 

The application leverages OpenCV for preprocessing and analysis of the image.

## Features
Upload an image of an ABD test cell.

Processes the uploaded image using morphological operations.

Detects the blood group (A, B, AB, or O) and the Rh factor (Positive or Negative).

Displays the original and processed images along with the detected blood group on the frontend.

## Technologies Used
Backend: Python with Django Framework

Image Processing: OpenCV

Frontend: HTML, CSS, Django Templates

## Installation Instructions

Clone the Repository

git clone <repository-url>
cd <repository-folder>
Set Up a Virtual Environment

python -m venv env
source env/bin/activate # Linux/macOS
env\Scripts\activate # Windows

## Install Dependencies

pip install -r requirements.txt

Run Database Migrations
python manage.py migrate

Run the Development Server
python manage.py runserver

Access the Application Open a browser and navigate to:
http://127.0.0.1:8000/

### How It Works

1. Image Upload:
   Users upload an ABD test cell image through the provided form.
2. Image Preprocessing:
   The uploaded image is converted to grayscale.
   Noise is reduced using Gaussian blur.
   Contrast is enhanced using histogram equalization.
   Thresholding and morphological operations (opening and closing) are applied to isolate agglutination regions.
3. Region Segmentation:
   The image is divided into three regions:
   Region A: Indicates Type A blood.
   Region B: Indicates Type B blood.
   Region D: Indicates Rh factor (Positive/Negative).
4. Agglutination Analysis:
   The number of connected components in each region is calculated.
   Based on the results:
   Blood type is determined (A, B, AB, or O).
   Rh factor is determined (Positive or Negative).
5. Results Display:
   The original image, processed image, and detected blood group are displayed on the frontend.

# Code Overview
## Backend
The logic is implemented in the views.py file:

> Image Preprocessing:
Grayscale conversion, Gaussian blur, histogram equalization, and thresholding.
> >Morphological Operations:
Structuring element (ellipse) is used for morphological opening and closing.
> Blood Group Determination:
Agglutination in specific regions indicates the blood group and Rh factor.

## Frontend
A simple HTML form for uploading images.
Displays the original and processed images along with the detected blood group.

# Usage

1. Navigate to the application in your browser.
2. Upload an ABD test cell image via the form.
3. Click the Check for Blood Group button.
4. View the results:
   Original image
   Processed (morphological) image
   Detected blood group and Rh factor

## File Structure

project/

├── app_name/

│ ├── migrations/

│ ├── static/

│ ├── templates/

│ │ └── profile.html

│ ├── views.py

│ ├── models.py

│ └── urls.py

├── manage.py

├── requirements.txt

└── README.md

## Requirements
Python 3.x

Django

OpenCV

NumPy

Install these using:
pip install -r requirements.txt

## SCREENSHOTS 
### HOME PAGE
![image](https://github.com/user-attachments/assets/467ac829-0f7a-4d38-b164-c80fb107886e)

### LOGIN PAGE :
![image](https://github.com/user-attachments/assets/a3403fe0-c723-45b3-a90c-4491212249e4)

### REGISTRATION PAGE :
![image](https://github.com/user-attachments/assets/5baa2973-5a2a-4a25-80fe-0a39d093a8bc)

### PROFILE PAGE :
![image](https://github.com/user-attachments/assets/8f50b3bb-301e-45e6-b6c4-429f2bc788be)

### INPUT AND OUTPUT:
![image](https://github.com/user-attachments/assets/663fd878-ff5e-429d-bf5b-1fe769a00b98)


ABOUT THE PROFILE PAGE LOGIC :

      if(request.method=="POST"):
      if(request.FILES.get('abd')):
      img_name = request.FILES['abd']

            #create a variable for FileSystem
            fs = FileSystemStorage()
            # need to save the image to the files
            filename = fs.save(img_name.name,img_name)
            #create the url
            img_url = fs.url(filename)
            # we need to find the path location
            # path() -> which is used to return the exact full path of our implementation
            img_path = fs.path(filename)
            # read the image
            img = cv2.imread(img_path)

            #convert it into grayscale
            gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            # filename = fs.save('gray.jpg',gray_img)
            # img_url = fs.url(filename)

            #apply gaussian blue to reduce the noise in the images
            blur_img = cv2.GaussianBlur(gray_img,(5,5),0)
            # cv2.imshow('gaussian',blur_img)
            #to enchance the contrast of the images
            enhance_img = cv2.equalizeHist(blur_img)

            #threshold calculation
            var, bin_img = cv2.threshold(enhance_img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

            #main imp step is of follows
            #morphological operations
            # s1 - kernel implementation
            kernel_imp = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
            # convert the threshold image intp morphological structured image
            bin_img = cv2.morphologyEx(bin_img,cv2.MORPH_OPEN,kernel_imp)
            bin_img = cv2.morphologyEx(bin_img,cv2.MORPH_CLOSE,kernel_imp)

            hei,wid = bin_img.shape
            mid_wid = wid//3

            region_A = bin_img[0:mid_wid]
            region_B = bin_img[mid_wid:2*mid_wid]
            region_D = bin_img[2*mid_wid:]

            # calculate the default formula for our blood group. that is agglutination
            def cal_agg(region):
                num_labels,labels,stats,var = cv2.connectedComponentsWithStats(region,connectivity=8)
                return num_labels-1

            num_region_A = cal_agg(region_A)
            num_region_B = cal_agg(region_B)
            num_region_D = cal_agg(region_D)

            print(num_region_A,num_region_B,num_region_D)

            obj=""

            '''
            Task for the day:
            1.
            if(A>0 && B==0)
                obj = A
            if(A==0 && B>0)
                obj = B
            if(A>0 && B>0)
                obj = AB
            if(A==0 && B==0)
                obj = O
            otherwise, blood type = unknown

            2.
            if num_region_D is greater than 0, then the blood is of positive type
                obj+='Positive'
            if num_region_D is less than or equal 0, then the blood is of negative type
                obj+='Negative'
            '''

            #convert the morphological bin_img into base64 img
            var, img = cv2.imencode('.jpg',bin_img)
            mor_img = base64.b64encode(img).decode('utf-8')
            mor_img_url = f"data:image/jpeg;base64,{mor_img}"



            return render(request,'profile.html',{'img':img_url,'mor_img':mor_img_url,'obj':obj})
            
   ```
