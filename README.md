
![alt text](Dri-Age_Logo.png)

# **Age Verification based on ID-Cards**

Dri-Age was developed as a group project during the SHSG Summer School 2022. The developer team includes Dom, Mario, Luca, Pat and Jon. 


#### The original case prompt was as follows: 
* Build a mobile or web application
* The application should detect the date of birth from an image of the ID card (manually uploaded or taken with the camera)
* An administrator should be able to configure up to two limits (e.g. 16 and 18 years) and the application shall visualize the respective limit after scanning


#### Background:
Nowadays, age verification when buying alcohol and cigarettes, entering a club, or buying a drink at a bar, is done manually. Employees check the age on an ID or equivalent and then compare the photo with the face of the customer. This process is slow and prone to errors. Busy nights, often hectic, and employees can be tempted to reduce the precision of their verification process. This again opens a bigger margin for errors and compromises on youth protection. To speed up the process and at the same time reduce the error margin an app that checks the age of guests and customers can be a handy tool. 

Dri-Age uses the purpose-built and internationally standardised information in the machine-readable zone [MRZ] of ID documents. The standard is set out in [ICAO Doc 9303](https://www.icao.int/publications/Documents/9303_p4_cons_en.pdf).


#### Software Versions:
The desktop version is optimized for MacOS, it also works on Windows but the design elements are less polished. The desktop version is fully functional offline. 
The mobile iOS version needs to be connected to the internet as the image processing is done on a server, a neccessary workaround because the kivy-io offers no recipe for tesseract as of now.

A portation to Android is technically possible, but would most likely also negatively impact design elements. 


#### Acknowledgements: 
Our solution utilizes multiple libraries and externally written code. The most important ones are [tesseract OCR](https://github.com/tesseract-ocr/tesseract), [OpenCV](https://github.com/opencv/opencv), [Kivy](https://github.com/kivy), [tessdata_ocrb](https://github.com/Shreeshrii/tessdata_ocrb) and [detect-MRZ](https://github.com/zhangluustb/detect-MRZ). 
