from flask import Flask, render_template, request, redirect, url_for, session, flash
import joblib
import numpy as np
import math
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
# Load your linear regression model
model = joblib.load('decision_tree_regressor_model_new.joblib')

def is_form_filled(form_data):
    # Fungsi ini memeriksa apakah semua elemen dalam form_data sudah terisi atau tidak
    return all(value.strip() for value in form_data.values())

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/product', methods=['GET', 'POST'])
def product_page():
    if request.method == 'POST':
        # Get data from the form and store it in the session
        if is_form_filled(request.form):
            session['NamaProduk'] = request.form['NamaProduk']
            return redirect(url_for('predict_page'))
        else:
            flash('Semua form harus terisi !!!')

    return render_template('predict1.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict_page():
    # Retrieve data from the session
    nama_produk = session.get('NamaProduk', 'No Data')  # Default to 'No Data' if not found

    if request.method == 'POST':
        # Get data from the form and store it in the session
        if is_form_filled(request.form):
            session['JumlahFoto'] = request.form['Jumlah_Foto']
            session['JumlahVideo'] = request.form['Jumlah_Video']
            session['Kategori'] = request.form['Kategori']
            session['Stok'] = request.form['Stok']
            session['HargaAwal'] = request.form['Harga_Awal']
            session['HargaAkhir'] = request.form['Harga_Akhir']
            session['Waktu'] = request.form['Waktu']
            return redirect(url_for('predictcont_page'))
        else:
            flash('Semua form harus terisi !!!')

    return render_template('predict2.html', nama_produk=nama_produk)

@app.route('/predict-cont', methods=['GET', 'POST'])
def predictcont_page():
    print(request.form)
    if request.method == 'POST':
        # Get data from the form and store it in the session
        if is_form_filled(request.form):
            session['Rating'] = request.form['Rating']
            session['Promo_Cashback'] = request.form['cashback']
            session['Promo_Diskon'] = request.form['diskon']
            session['Promo_Gratis_Ongkir'] = request.form['gratis-ongkir']
            session['Jam_Toko_Buka'] = request.form['jam-buka']
            session['Jam_Toko_Tutup'] = request.form['jam-tutup']
            session['Campaign'] = request.form['campaign']
            return redirect(url_for('hasil'))
        else:
            flash('Semua form harus terisi !!!')

    # Retrieve data from the session
    jumlah_foto = session.get('JumlahFoto', 'No Data')
    jumlah_video = session.get('JumlahVideo', 'No Data')
    kategori = session.get('Kategori', 'No Data')
    stok = session.get('Stok', 'No Data')
    harga_awal = session.get('HargaAwal', 'No Data')
    harga_akhir = session.get('HargaAkhir', 'No Data')
    waktu = session.get('Waktu', 'No Data')

    return render_template('predict3.html', jumlah_foto=jumlah_foto, jumlah_video=jumlah_video, kategori=kategori,
                           stok=stok, harga_awal=harga_awal, harga_akhir=harga_akhir, waktu=waktu)

@app.route('/result')
def hasil():
    Kategori = session.get('Kategori')
    # Your data dictionary
    data_dict = {
    'media_foto': session.get('JumlahFoto', 'No Data'),
    'media_video': session.get('JumlahVideo', 'No Data'),
    'price': session.get('HargaAkhir', 'No Data'),
    'original_price': session.get('HargaAwal', 'No Data'),
    'campaign': session.get('Campaign', 'No Data'),
    'stock': session.get('Stok', 'No Data'),
    'shop_rating': session.get('Rating', 'No Data'),
    'waktu_proses': session.get('Waktu', 'No Data'),
    'promo_cashback': session.get('Promo_Cashback', 'No Data'),
    'promo_diskon': session.get('Promo_Diskon', 'No Data'),
    'promo_gratis_ongkir': session.get('Promo_Gratis_Ongkir', 'No Data'),
    'jam_buka': session.get('Jam_Toko_Buka', 'No Data'),
    'jam_tutup': session.get('Jam_Toko_Tutup', 'No Data'),
    'Kategori_Asupan Ibu & Bayi': 1 if session.get('Kategori') == 'Asupan Ibu & Bayi' else 0,
    'Kategori_Berbagai Minuman': 1 if session.get('Kategori') == 'Berbagai Minuman' else 0,
    'Kategori_Busana Anak & Bayi': 1 if session.get('Kategori') == 'Busana Anak & Bayi' else 0,
    'Kategori_Busana Muslim': 1 if session.get('Kategori') == 'Busana Muslim' else 0,
    'Kategori_Busana Pria': 1 if session.get('Kategori') == 'Busana Pria' else 0,
    'Kategori_Busana Wanita': 1 if session.get('Kategori') == 'Busana Wanita' else 0,
    'Kategori_Dapur': 1 if session.get('Kategori') == 'Dapur' else 0,
    'Kategori_Hobi': 1 if session.get('Kategori') == 'Hobi' else 0,
    'Kategori_Kebutuhan Bayi': 1 if session.get('Kategori') == 'Kebutuhan Bayi' else 0,
    'Kategori_Kebutuhan Isi Rumah': 1 if session.get('Kategori') == 'Kebutuhan Isi Rumah' else 0,
    'Kategori_Makanan': 1 if session.get('Kategori') == 'Makanan' else 0,
    'Kategori_Make Up': 1 if session.get('Kategori') == 'Make Up' else 0,
    'Kategori_Otomotif': 1 if session.get('Kategori') == 'Otomotif' else 0,
    'Kategori_Pakaian Olahraga': 1 if session.get('Kategori') == 'Pakaian Olahraga' else 0,
    'Kategori_Perawatan Wajah': 1 if session.get('Kategori') == 'Perawatan Wajah' else 0,
    'Kategori_Snack & Camilan': 1 if session.get('Kategori') == 'Snack & Camilan' else 0
}
    # Convert data_dict values to a numpy array for prediction
    input_data = np.array(list(data_dict.values())).reshape(1, -1)
    # Convert to numeric
    input_data = input_data.astype(float)

    # Make prediction using the loaded model
    hasil_prediksi = model.predict(input_data)
    hasil_prediksi = math.ceil(hasil_prediksi)
    print(hasil_prediksi)

    if session.get('Kategori') == 'Asupan Ibu & Bayi':
        img1= "static/assets/img/foto.png"
        v1="FOTO"
        s1="Tampilkan lebih dari 3 foto"

        img2="static/assets/img/campaign.png"
        v2="CAMPAIGN"
        s2="Sertakan produk Anda dalam campaign"

        img3="static/assets/img/price-ori.png"
        v3="ORIGINAL PRICE"
        s3="Tetapkan harga awal produk diatas Rp54.750"

    elif session.get('Kategori') == 'Berbagai Minuman':
        img1= "static/assets/img/foto.png"
        v1="FOTO"
        s1="Tampilkan lebih dari 3 foto"

        img2="static/assets/img/price-after.png"
        v2="PRICE"
        s2="Tetapkan harga akhir produk dibawah Rp71.400"

        img3="static/assets/img/open.png"
        v3="JAM BUKA"
        s3="Buka toko Anda sebelum pukul 09:00 WIB"

    elif session.get('Kategori') == 'Busana Anak & Bayi':
        img1= "static/assets/img/foto.png"
        v1="FOTO"
        s1="Tampilkan lebih dari 4 foto"

        img2="static/assets/img/tutup.png"
        v2="JAM TUTUP"
        s2="Jadwalkan Jam Tutup toko sebelum pukul 20:00 WIB"

        img3="static/assets/img/campaign.png"
        v3="CAMPAIGN"
        s3="Sertakan produk Anda dalam campaign"

    elif session.get('Kategori') == 'Busana Muslim':
        img1= "static/assets/img/campaign.png"
        v1="CAMPAIGN"
        s1="Sertakan produk Anda dalam campaign"

        img2="static/assets/img/stok.png"
        v2="STOCK"
        s2="Pastikan produk Anda memiliki stok kurang dari 39 pcs"

        img3="static/assets/img/tutup.png"
        v3="JAM TUTUP"
        s3="Jadwalkan Jam Tutup toko setelah pukul 19:00 WIB"

    elif session.get('Kategori') == 'Busana Pria':
        img1= "static/assets/img/campaign.png"
        v1="CAMPAIGN"
        s1="Sertakan produk Anda dalam campaign"

        img2="static/assets/img/stok.png"
        v2="STOCK"
        s2="Pastikan produk Anda memiliki stok lebih dari 69 pcs"

        img3="static/assets/img/price-after.png"
        v3="PRICE"
        s3="Tetapkan harga akhir produk diatas Rp152.450"

    elif session.get('Kategori') == 'Busana Wanita':
        img1= "static/assets/img/ongkir.png"
        v1="PROMO GRATIS ONGKIR"
        s1="Tidak perlu memberikan promo gratis ongkir pada produk ini"

        img2="static/assets/img/diskon.png"
        v2="PROMO DISCOUNT"
        s2="Berikan promo diskon khusus untuk produk ini"

        img3="static/assets/img/price-ori.png"
        v3="ORIGINAL PRICE"
        s3="Tetapkan harga awal produk di bawah Rp184.000"

    elif session.get('Kategori') == 'Dapur':
        img1= "static/assets/img/campaign.png"
        v1="CAMPAIGN"
        s1="Tidak perlu ikut campaign. Fokus pada keunikan produk"

        img2="static/assets/img/vidio.png"
        v2="VIDEO"
        s2="Tambahkan video pada katalog produk"

        img3="static/assets/img/price-after.png"
        v3="PRICE"
        s3="Tetapkan harga akhir produk dibawah Rp300.174"

    elif session.get('Kategori') == 'Hobi':
        img1= "-"
        v1="-"
        s1="-"

        img2="-"
        v2="-"
        s2="-"

        img3="-"
        v3="-"
        s3="-"

    elif session.get('Kategori') == 'Kebutuhan Bayi':
        img1= "static/assets/img/campaign.png"
        v1="CAMPAIGN"
        s1="Sertakan produk Anda dalam campaign"

        img2="static/assets/img/vidio.png"
        v2="VIDEO"
        s2="Tidak perlu menyertakan video dalam katalog produk. Fokus pada gambar dan deskripsi yang menarik & informatif"

        img3="static/assets/img/cashback.png"
        v3="PROMO CASHBACK"
        s3="Berikan promo cashback khusus untuk produk ini"

    elif session.get('Kategori') == 'Kebutuhan Isi Rumah':
        img1= "static/assets/img/ongkir.png"
        v1="PROMO GRATIS ONGKIR"
        s1="Berikan promo gratis ongkir untuk produk ini"

        img2="static/assets/img/price-ori.png"
        v2="ORIGINAL PRICE"
        s2="Tetapkan harga awal produk dibawah Rp1.087.500"

        img3="static/assets/img/stok.png"
        v3="STOCK"
        s3="Pastikan produk Anda memiliki stok kurang dari 97 pcs"

    elif session.get('Kategori') == 'Makanan':
        img1= "static/assets/img/campaign.png"
        v1="CAMPAIGN"
        s1="Sertakan produk Anda dalam campaign"

        img2="static/assets/img/tutup.png"
        v2="JAM TUTUP"
        s2="Jadwalkan Jam Tutup toko sebelum pukul 16:00 WIB"

        img3="static/assets/img/diskon.png"
        v3="PROMO DISCOUNT"
        s3="Berikan promo diskon khusus untuk produk ini"

    elif session.get('Kategori') == 'Make Up':
        img1= "static/assets/img/foto.png"
        v1="FOTO"
        s1="Tampilkan lebih dari 4 foto"

        img2="static/assets/img/tutup.png"
        v2="JAM TUTUP"
        s2="Jadwalkan Jam Tutup toko setelah pukul 20:50 WIB"

        img3="static/assets/img/diskon.png"
        v3="PROMO DISCOUNT"
        s3="Berikan promo diskon khusus untuk produk ini"

    elif session.get('Kategori') == 'Otomotif':
        img1= "static/assets/img/price-after.png"
        v1="PRICE"
        s1="Tetapkan harga akhir produk diatas Rp97.061"

        img2="static/assets/img/stok.png"
        v2="STOCK"
        s2="Pastikan produk Anda memiliki stok lebih dari 1 pcs"

        img3="static/assets/img/foto.png"
        v3="FOTO"
        s3="Tampilkan lebih dari 1 foto"

    elif session.get('Kategori') == 'Pakaian Olahraga':
        img1= "static/assets/img/stok.png"
        v1="STOCK"
        s1="Pastikan produk Anda memiliki stok kurang dari 218 pcs"

        img2="static/assets/img/proses.png"
        v2="WAKTU PROSES"
        s2="Pastikan waktu proses produk Anda lebih dari 5 hari"

        img3="static/assets/img/campaign.png"
        v3="CAMPAIGN"
        s3="Sertakan produk Anda dalam campaign"

    elif session.get('Kategori') == 'Perawatan Wajah':
        img1= "static/assets/img/tutup.png"
        v1="JAM TUTUP"
        s1="Jadwalkan Jam Tutup toko sebelum pukul 17:50 WIB"

        img2="static/assets/img/stok.png"
        v2="STOCK"
        s2="Pastikan produk Anda memiliki stok kurang dari 675 pcs"

        img3="static/assets/img/diskon.png"
        v3="PROMO DISCOUNT"
        s3="Berikan promo diskon khusus untuk produk ini"

    elif session.get('Kategori') == 'Snack & Camilan':
        img1= "static/assets/img/foto.png"
        v1="FOTO"
        s1="Tampilkan kurang dari 3 foto"

        img2="static/assets/img/price-ori.png"
        v2="ORIGINAL PRICE"
        s2="Tetapkan harga awal produk diatas Rp10.965"

        img3="static/assets/img/campaign.png"
        v3="CAMPAIGN"
        s3="Sertakan produk Anda dalam campaign"



    

    return render_template('result-1.html', hasil_prediksi=hasil_prediksi,img1=img1,img2=img2,img3=img3,s1=s1,s2=s2,s3=s3,v1=v1,v2=v2,v3=v3)

if __name__ == '__main__':
    app.run(debug=True)
