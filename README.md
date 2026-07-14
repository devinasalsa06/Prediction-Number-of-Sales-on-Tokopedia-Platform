# Prediction-Number-of-Sales-on-Tokopedia-Platform
The project focuses on developing a machine learning-based forecasting system to help estimate product sales volumes on Tokopedia. The stages of this project include:

1. Cleaning the dataset and identifying predictor variables, such as the number of photos, the number of videos, product category, inventory, price, rating, promotions, free shipping, store hours, and campaigns.

2. Building a predictive model using the Decision Tree Regressor algorithm with the Pandas and Scikit-learn libraries, then evaluating model using the Mean Squared Error (MSE) metric. The model is exported in Joblib/Pickle format for integration into the web application.

3. Developing the frontend, which involves designing and building the website interface using HTML, CSS, and JavaScript.

4. Integrate the backend with Flask such as connect the machine learning model to the web application using Flask as the backend, build routing for POST requests from user form, process input, generate sales quantity predictions, and display recommendations based on product categories.

5. Deploy the website to PythonAnywhere, upload all program files to the created environment, and configure the WSGI file so that the Flask application can run.
