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
