# coding:utf-8
import os
import time
from datetime import timedelta

import cv2
from demo import predicts
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

# 设置允许的文件格式

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)


@app.route('/resnet', methods=['POST', 'GET'])
# @app.route('/', methods=['POST', 'GET'])  # 添加路由
def upload():
    if request.method == 'POST':
        f = request.files['file']

        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001,
                            "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})

        user_input = request.form.get("name")

        basepath = os.path.dirname(__file__)  # 当前文件所在路径

        upload_path = os.path.join(
            basepath,
            'static/images',
            secure_filename(
                f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        # upload_path = os.path.join(basepath, 'static/images','test.jpg')
        # #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)

        # 使用Opencv转换一下图片格式和名称
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)
        pres, pro = predicts(upload_path)
        print(upload_path)

        return render_template(
            'upload_ok.html',
            userinput=user_input,
            classresult=pres,
            classpro=pro,
            val1=time.time())

    return render_template('upload.html')


if __name__ == '__main__':
    # app.debug = True
    app.run(host='127.0.0.1', port=5000, debug=True)
