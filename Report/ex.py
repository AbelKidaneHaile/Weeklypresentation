from PIL import Image
from Weeklypresentation.Report.prediction import prediction
from Weeklypresentation.Report.prediction import pre_image
from Weeklypresentation.Report.prediction import load_model
from Weeklypresentation.Report.prediction import predict
from Weeklypresentation.Report.prediction import annotate

import gradio as gr
import cv2
import onnxruntime
import matplotlib.pyplot as plt
import fire

model = load_model(model_path="best_re_final.onnx")

# def greet(temperature):
#     # salutation = "Good morning" if is_morning else "Good evening"
#     # greeting = f"{salutation} {name}. It is {temperature} degrees today"
#     celsius = (temperature - 32) * 5 / 9
#     return  round(celsius, 2)




def predict_gradio(image,Confidence):
   
    conf = Confidence /100
    input_I= pre_image(image, model[1]) #path and input shape is passed
    predictions = predict(image, model[0], input_I, conf)  #image, ort_session, and input tensor is passed
    annotatedImage = annotate(image, predictions[0], predictions[1], predictions[2]) #boxes, and scores are passed
    annotatedImage =  cv2.cvtColor(annotatedImage, cv2.COLOR_BGR2RGB)

    return (annotatedImage,Confidence)



demo = gr.Interface(  fn=predict_gradio,
    inputs=[
        "image",gr.Slider(0, 100),
    ],
    outputs=["image","number"],
    title="Head Detection",
    css=".gradio-container { background-color: grey; }"
                    )
demo.launch()