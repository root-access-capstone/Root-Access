from flask import Flask
import router

app = Flask(__name__)
app.secret_key="iuhdhsiuleafiueafwaiulgelubuwealegiuhuawefliu"
app.register_blueprint(router.router)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')