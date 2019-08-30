# coding:utf-8

from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from image_process import ImageProcess, client_id, client_secret

from datetime import timedelta

# 设置允许的文件格式
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'JPG', 'PNG', 'bmp'}
PROCESS_TYPE = {'1': '无损放大',
                '2': '去雾',
                '3': '对比度增强',
                '4': '黑白图像上色',
                '5': '拉伸图像恢复',
                '6': '图像风格转换'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)

ip_obj = ImageProcess(client_id, client_secret)


@app.route('/', methods=['POST', 'GET'])  # 添加路由
def upload():
    filename = '3efe5cc3e397933216ed48f99ad43e02.png'
    if request.method == 'POST':
        file = request.files['file']
        if not (file and allowed_file(file.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
        base_path = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(base_path, 'static/images')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(upload_path, filename))
        return redirect(url_for('show_button', img_name=filename))
    return render_template('pages/upload_img.html', img_name=filename)


@app.route('/show_button/?<string:img_name>', methods=['POST', 'GET'])  # 添加路由
def show_button(img_name):
    if request.method == 'POST':
        process_type = request.form.get('process_type')
        img = './static/images/' + img_name
        with open(img, 'rb') as f:
            img_data = f.read()
        if process_type == "1":
            res = ip_obj.image_quality_enhance(img_data)
            res_base64 = res['image']
        elif process_type == "2":
            res = ip_obj.dehaze(img_data)
            res_base64 = res['image']
        elif process_type == "3":
            res = ip_obj.contrast_enhance(img_data)
            res_base64 = res['image']
        elif process_type == "4":
            res = ip_obj.colorize(img_data)
            res_base64 = res['image']
        elif process_type == "5":
            res = ip_obj.stretch_restore(img_data)
            res_base64 = res['image']
        elif process_type == "6":
            audio_con = request.form.get('inlineRadioOptions')
            options = {'option': audio_con}
            res = ip_obj.style_trans(img_data, options)
            res_base64 = res['image']

        return render_template('pages/img_process.html',
                               img_name=img_name,
                               img_base64=res_base64,
                               pro_type=process_type,
                               op_dict=PROCESS_TYPE)

    return render_template('pages/show_button.html', img_name=img_name, op_dict=PROCESS_TYPE)


@app.route('/upload_event/', methods=['POST', 'GET'])
def upload_event():
    filename = '3efe5cc3e397933216ed48f99ad43e02.png'
    if request.method == 'POST':
        file = request.files['file']
        if not (file and allowed_file(file.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
        base_path = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(base_path, 'static/images')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(upload_path, filename))
        return redirect(url_for('show_button', img_name=filename))
    return render_template('pages/upload_img.html', img_name=filename)


if __name__ == '__main__':
    # app.debug = True
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug=True)
