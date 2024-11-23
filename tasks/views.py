import base64
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate
import cv2
import numpy as np
import base64
from django.shortcuts import render

# Create your views here.
# def home(request):
#     return render(request, 'home_page.html')
# def login(request):
#     return render(request, 'login.html')
# def signup(request):
#     return render(request, 'signup.html')

# Create your views here.
def home(request):
    # request is used to navgate the command to our html page
    # for navigation we need to use a keyword called as "render"
    return render(request,'home_page.html')
 
def login(request):
    if(request.user.is_authenticated):
        return redirect('/')
    if(request.method == "POST"):
        un = request.POST['username']
        pw = request.POST['password']
        user = authenticate(request,username=un,password=pw)
        #authenticate() used to check for the valid statements given or not by linking with database automatically.
        #if the values are matched, then it will return the username
        #if the values are not matched, then it will return the 'None'
        if(user is not None):
            return redirect('/profile')
        else:
            msg = 'Error in login. Invalid username/password'
            form = AuthenticationForm()
            # used to create a basic login page with username and password conditions
            return render(request,'login.html',{'form':form,'msg':msg})
    else:
        form = AuthenticationForm()
        # used to create a basic login page with username and password conditions
        return render(request,'login.html',{'form':form})
 
def register(request):
    if(request.user.is_authenticated):
        return redirect('/')
    if(request.method == "POST"):
        form = UserCreationForm(request.POST)
        if(form.is_valid()):
            form.save()
            un = form.cleaned_data.get('username')
            pw = form.cleaned_data.get('password1')
            user = authenticate(username=un,password=pw)
            return redirect('/login')
        else:
            return render(request,'signup.html',{'form':form})
    else:
        form = UserCreationForm()
        return render(request,'signup.html', {'form':form})
import cv2
import numpy as np
import base64
from django.shortcuts import render

# def profile(request):
#     if request.method == "POST":
#         if request.FILES.get('abd'):
#             # Read the uploaded image
#             img_file = request.FILES['abd'].read()
#             np_arr = np.frombuffer(img_file, np.uint8)
#             img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

#             # Convert to grayscale
#             gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#             # Apply Gaussian blur
#             blur_img = cv2.GaussianBlur(gray_img, (5, 5), 0)

#             # Enhance contrast
#             enhance_img = cv2.equalizeHist(blur_img)

#             # Apply thresholding
#             _, bin_img = cv2.threshold(enhance_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

#             # Morphological operations
#             kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
#             bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, kernel)
#             bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_CLOSE, kernel)

#             # Split into regions for A, B, and D
#             height, width = bin_img.shape
#             region_width = width // 3
#             region_A = bin_img[:region_width, :]
#             region_B = bin_img[region_width:2 * region_width, :]
#             region_D = bin_img[2 * region_width:, :]

#             # Calculate agglutination
#             def calculate_agglutination(region):
#                 if region.size == 0 or cv2.countNonZero(region) == 0:
#                     return 0
#                 _,binary_region = cv2.threshold(region, 0, 255, cv2.THRESH_BINARY)
#                 num_labels, _, _, _ = cv2.connectedComponentsWithStats(binary_region, connectivity=8)
#                 return num_labels - 1

#             num_A = calculate_agglutination(region_A)
#             num_B = calculate_agglutination(region_B)
#             num_D = calculate_agglutination(region_D)

#             # Determine blood group
#             blood_group = "Unknown"
#             if num_A > 0 and num_B == 0:
#                 blood_group = "A"
#             elif num_A == 0 and num_B > 0:
#                 blood_group = "B"
#             elif num_A > 0 and num_B > 0:
#                 blood_group = "AB"
#             elif num_A == 0 and num_B == 0:
#                 blood_group = "O"

#             if num_D > 0:
#                 blood_group += " Positive"
#             else:
#                 blood_group += " Negative"

#             # Encode morphological image to Base64 for display
#             _, buffer = cv2.imencode('.jpg', bin_img)
#             mor_img = base64.b64encode(buffer).decode('utf-8')
#             mor_img_url = f"data:image/jpeg;base64,{mor_img}"

#             # Render results to the template
#             return render(request, 'profile.html', {
#                 'img': f"data:image/jpeg;base64,{base64.b64encode(cv2.imencode('.jpg', img)[1]).decode('utf-8')}",
#                 'mor_img': mor_img_url,
#                 'obj': blood_group
#             })

#     return render(request, 'profile.html')
def profile(request):
    if request.method == "POST":
        if request.FILES.get('abd'):
            # Read the uploaded image
            img_file = request.FILES['abd'].read()
            np_arr = np.frombuffer(img_file, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            # Convert to grayscale
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Apply Gaussian blur
            blur_img = cv2.GaussianBlur(gray_img, (5, 5), 0)

            # Enhance contrast
            enhance_img = cv2.equalizeHist(blur_img)

            # Apply thresholding
            _, bin_img = cv2.threshold(enhance_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Morphological operations
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, kernel)
            bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_CLOSE, kernel)

            # Split into regions for A, B, and D
            height, width = bin_img.shape
            region_width = width // 3

            # Ensure regions are not empty
            assert region_width > 0, "Region width must be greater than zero."
            region_A = bin_img[:region_width, :]
            region_B = bin_img[region_width:2 * region_width, :]
            region_D = bin_img[2 * region_width:, :]

            # Calculate agglutination
            def calculate_agglutination(region):
                if region.size == 0 or cv2.countNonZero(region) == 0:
                    return 0
                try:
                    _, binary_region = cv2.threshold(region, 0, 255, cv2.THRESH_BINARY)
                    binary_region = binary_region.astype(np.uint8)  # Ensure correct type
                    num_labels, _, _, _ = cv2.connectedComponentsWithStats(binary_region, connectivity=8)
                    return num_labels - 1
                except cv2.error as e:
                    print(f"OpenCV error: {e}")
                    return 0

            num_A = calculate_agglutination(region_A)
            num_B = calculate_agglutination(region_B)
            num_D = calculate_agglutination(region_D)

            # Determine blood group
            blood_group = "Unknown"
            if num_A > 0 and num_B == 0:
                blood_group = "A"
            elif num_A == 0 and num_B > 0:
                blood_group = "B"
            elif num_A > 0 and num_B > 0:
                blood_group = "AB"
            elif num_A == 0 and num_B == 0:
                blood_group = "O"

            if num_D > 0:
                blood_group += " Positive"
            else:
                blood_group += " Negative"

            # Encode morphological image to Base64 for display
            _, buffer = cv2.imencode('.jpg', bin_img)
            mor_img = base64.b64encode(buffer).decode('utf-8')
            mor_img_url = f"data:image/jpeg;base64,{mor_img}"

            # Render results to the template
            return render(request, 'profile.html', {
                'img': f"data:image/jpeg;base64,{base64.b64encode(cv2.imencode('.jpg', img)[1]).decode('utf-8')}",
                'mor_img': mor_img_url,
                'obj': blood_group
            })

    return render(request, 'profile.html')