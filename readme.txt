If you want to use multiple video formats such as mp4, currently you must install the application with python (1).
Otherwise, skip to (2) for advice on using the stand alone application.

(1)
First install the codec basic pack from this link:
https://codecguide.com/download_k-lite_codec_pack_basic.htm
(You need this because windows does not support some video formats by default)


Next, ensure you have python3.7 installed. 

Next, Clone the directory onto your pc. Using git clone or by downloading and extracting manually.

Next, create a virtual environmet for the application
This can be done by install virtualenv and typing 'virtualenv venv' in the directory
of your application.

Next, activate your virtual environment. On windows you can do this by navigating into 
your new virtual env called venv, then to Scripts, then run 'activate'.

Next, install all required python packages into your virtualenv.
To do this you can type 'pip install -r requirements' while in the dynamic state tracker folder.
(If this fails then install each package mentioned there individually)

Finally to run the application type 'python main.py' while in the dynamic state tracker directory.


(2)
To use the stand alone application, you must unzip the file into the directory you want the program. Ensure that the application (main)
is in the same directory as the saves and exports folder. When using the stand alone application you must use the wmv video format. You can convert
other formats to wmv using this website : https://www.online-convert.com



----------------------------------------------------

Ensure that you have the folders 'saves\Form_layout', 'saves\Questions_layout' and  'exports' in the directory of the program!
