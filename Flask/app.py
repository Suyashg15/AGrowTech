from flask import Flask, render_template, jsonify, request, Markup,redirect
from model import predict_image
import pickle
import utils
import requests
import config
import numpy as np

app = Flask(__name__)

modelf = pickle.load(open('models/classifier.pkl','rb'))
ferti = pickle.load(open('models/fertilizer.pkl','rb'))

crop_recommendation_model_path = 'models/LGBMClassifier.pkl'
crop_recommendation_model = pickle.load(
    open(crop_recommendation_model_path, 'rb'))

def weather_fetch(city_name):
    """
    Fetch and returns the temperature and humidity of a city
    :params: city_name
    :return: temperature, humidity
    """
    
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    complete_url = base_url + "appid=" + "10436c6acff0c83f9ea4b3a2558ff8a6" + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]

        temperature = round((y["temp"] - 273.15), 2)
        humidity = y["humidity"]
        return temperature, humidity
    else:
        return None

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@ app.route('/crop-recommend')
def crop_recommend():
    title = 'Crop Recommendation'
    return render_template('crop.html', title=title)

@ app.route('/fertilizer')
def fertilizer():
    title = 'Fertilizer '
    return render_template('fertilizer.html', title=title)

@app.route('/fertilizer_result',methods=['POST'])
def fertilize_pred():
    city = str(request.form['city'])
    temp, humi = weather_fetch(city)
    mois = request.form.get('mois')
    soil = request.form.get('soil')
    crop = request.form.get('crop')
    nitro = request.form.get('nitro')
    pota = request.form.get('pota')
    phosp = request.form.get('phos')
    input = [int(temp),int(humi),int(mois),int(soil),int(crop),int(nitro),int(pota),int(phosp)]

    res = ferti.classes_[modelf.predict([input])]

    return render_template('fertilizer_result.html',x = ('Predicted Fertilizer is {}'.format(res)))


@app.route('/irrigation')
def irrigation():
    return render_template('irrigation.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            file = request.files['file']
            img = file.read()
            prediction = predict_image(img)
            print(prediction)
            res = Markup(utils.disease_dic[prediction])
            return render_template('display.html', status=200, result=res)
        except:
            pass
    return render_template('index.html', status=500, res="Internal Server Error")

@ app.route('/crop-predict', methods=['POST'])
def crop_prediction():
    title = 'Crop Recommendation'

    if request.method == 'POST':
        N = int(request.form['nitrogen'])
        P = int(request.form['phosphorous'])
        K = int(request.form['pottasium'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])

        # state = request.form.get("stt")
        city = str(request.form['city'])

        if weather_fetch(city) != None:
            temperature, humidity = weather_fetch(city)
            data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
            my_prediction = crop_recommendation_model.predict(data)
            final_prediction = my_prediction[0]
            if final_prediction=="orange":
                f1="orange ₹75000 per Acre"
                fp2="lentil ₹40000 per Acre"
                fp3=" blackgram ₹8000 per Acre"
            if final_prediction=="lentil":
                f1="lentil ₹40000 per Acre"
                fp2=" blackgram ₹8000 per Acre"
                fp3="maize   ₹15200 per Acre"
            if final_prediction==" blackgram":
                f1=" blackgram ₹8000 per Acre"
                fp2="maize ₹15200 per Acre"
                fp3="mothbeans"
            if final_prediction=="maize":
                f1="maize ₹15200 per Acre"
                fp2="mothbeans ₹20000 per Acre"
                fp3="mungbean ₹7500 per Acre"
            if final_prediction=="mothbeans":
                f1="mothbeans ₹20000 per Acre"
                fp2="mungbean ₹7500 per Acre"
                fp3="cotton ₹69000 per Acre"
            if final_prediction=="mungbean ":
                f1="mungbean ₹7500 per Acre"
                fp2="cotton ₹69000 per Acre"
                fp3="pigeonpeas ₹13000 per Acre"
            if final_prediction=="cotton":
                f1="cotton ₹69000 per Acre"
                fp2="pigeonpeas ₹13000 per Acre"
                fp3="kidneybeans  ₹10100 per Acre"
            if final_prediction=="pigeonpeas":
                f1="pigeonpeas ₹13000 per Acre"
                fp2="kidneybeans  ₹10100 per Acre"
                fp3=" coffee ₹125000 per Acre"
            if final_prediction=="kidneybeans":
                f1="kidneybeans  ₹10100 per Acre"
                fp2=" coffee ₹125000 per Acre"
                fp3="mango  ₹10000 per Acre"
            if final_prediction=="coffee":
                f1="coffee ₹125000 per Acre"
                fp2="mango  ₹10000 per Acre"
                fp3=" coconut ₹60000 per Acre"
            if final_prediction=="mango":
                f1="mango  ₹10000 per Acre"
                fp2=" coconut ₹60000 per Acre"
                fp3="pomegranate ₹200000 per Acre"
            if final_prediction=="coconut":
                f1="coconut ₹60000 per Acre"
                fp2="pomegranate ₹200000 per Acre"
                fp3="jute ₹31000 per Acre"
            if final_prediction=="pomegranate":
                f1="pomegranate ₹200000 per Acre"
                fp2="jute ₹31000 per Acre"
                fp3="rice   ₹25000 per Acre"
            if final_prediction=="chickpea":
                f1="chickpea  ₹11700 per Acre"
                fp2="grapes ₹100000 per Acre"
                fp3="apple   ₹12500 per Acre"
            if final_prediction=="muskmelon":
                f1="muskmelon ₹25000 per Acre"
                fp2="chickpea  ₹11700 per Acre"
                fp3="grapes ₹100000 per Acre"
            if final_prediction=="watermelon":
                f1="watermelon ₹27000 per Acre"
                fp2="muskmelon ₹25000 per Acre"
                fp3="chickpea  ₹11700 per Acre"
            if final_prediction=="papaya":
                f1="papaya ₹40000 per Acre"
                fp2="watermelon ₹27000 per Acre"
                fp3="muskmelon ₹25000 per Acre"
            if final_prediction=="banana":
                f1="banana ₹70000 per Acre"
                fp2="papaya ₹40000 per Acre"
                fp3="watermelon ₹27000 per Acre"
            if final_prediction=="rice":
                f1="rice   ₹25000 per Acre"
                fp2="banana ₹70000 per Acre"
                fp3="papaya ₹40000 per Acre"
            if final_prediction=="jute":
                f1="jute ₹31000 per Acre"
                fp2="rice   ₹25000 per Acre"
                fp3="banana ₹70000 per Acre"
            

                #fp2 second value and fp3 third value
            return render_template('crop-result.html', prediction=f1,prediction2=fp2,prediction3=fp3, title=title)

        else:

            return render_template('try_again.html', title=title)

@ app.route('/gov_schemes')
def gov():
    title = 'Gov Schemes'
    return redirect("https://mpkrishi.mp.gov.in/Englishsite_New/suvidhaye_New.aspx")

@ app.route('/video')
def video():
    title = 'Explaination Video'
    return redirect("https://youtu.be/LFmPQU3UoQg")




if __name__ == "__main__":
    app.run(debug=True)
