from flask import Flask,render_template,jsonify,request,send_file
from src.exception import CustomException
from src.logger import logging as lg
import os,sys


from src.pipeline.train_pipeline import TrainingPipeline
from src.pipeline.predict_pipeline import PredictionPipeline


app = Flask(__name__)

@app.route("/")
def home():
    return "welcome to my application"

@app.route("/train")
def train_route():
    try:
        train_pipeline = TrainingPipeline
        train_pipeline.run_pipeline()


        return "training completed"
    except Exception as e:
        raise CustomException(e,sys)
    
@app.route("/predict",methods=['POST',"GET"])
def upload():

    try:


        if request.method=='POST':
            # it is a object of prediction pipeline
            Prediction_Pipeline= PredictionPipeline(request)

            # now we are running this run pipeline method
            prediction_file_detail =  Prediction_Pipeline.run_pipeline


            lg.info("prediction completed .Downloading prediction file.")
            return send_file(prediction_file_detail.prediction_file_path,
                             download_name=prediction_file_detail.prediction_file_name,
                             as_attachment=True)
        
        else:
            return render_template("upload_file.html")
    except Exception as e:
        raise CustomException
    

if __name__== "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)