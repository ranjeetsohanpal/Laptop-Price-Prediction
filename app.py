from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the model and data
with open('pipe.pkl', 'rb') as f:
    model = pickle.load(f)
with open('train_df.pkl', 'rb') as f:
    df = pickle.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():

    # GET request
    companies = df['Manufacturer'].unique()
    categories = df['Category'].unique()
    cpus = df['cpu_brand'].unique()
    gpus = df['gpu_brand'].unique()
    oss = df['os'].unique()
    if request.method == 'POST':
        # Extract features from form input
        company = request.form['company']
        category = request.form['category']
        ram = int(request.form['ram'])
        weight = float(request.form['weight'])
        touchscreen = 1 if request.form['touchscreen'] == 'Yes' else 0
        ips = 1 if request.form['ips'] == 'Yes' else 0
        screen_size = float(request.form['screen_size'])
        res_height = int(request.form['res_height'])
        res_width = int(request.form['res_width'])
        cpu = request.form['cpu']
        hdd = int(request.form['hdd'])
        ssd = int(request.form['ssd'])
        gpu = request.form['gpu']
        os = request.form['os']

        # Compute PPI
        ppi = ((res_width**2) + (res_height**2))**0.5 / screen_size

        # Create feature array
        features = np.array([[company,category, ram, weight, touchscreen, ips, ppi, cpu, hdd, ssd, gpu, os]])

        # Predict price
        predicted_price = int(np.exp(model.predict(features)[0]))

        return render_template('index.html', predicted_price=predicted_price, companies=companies, categories=categories, 
                               cpus=cpus, gpus=gpus, oss=oss,selected_company=company, selected_category=category, selected_cpu=cpu,
                               selected_gpu=gpu, selected_os=os,selected_ram = ram,selected_wt = weight,selected_touch = touchscreen,selected_ips = ips
                               ,selected_ss = screen_size,selected_res_ht = res_height,selected_res_wd = res_width,selected_hdd = hdd,
                               selected_ssd = ssd)
    else:
        
        return render_template('index.html', companies=companies, categories=categories, cpus=cpus, gpus=gpus, oss=oss)

if __name__ == '__main__':
    app.run(debug=True)
