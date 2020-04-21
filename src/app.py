from flask import Flask

from internal.blueprint import blueprint as InternalBlueprint
from faiss_index.blueprint import blueprint as FaissIndexBlueprint

app = Flask(__name__)
app.config['INDEX_PATH'] = '../resources/cnn_index.index'
app.config['IDS_VECTORS_PATH'] = '../resources/vectors.pkl'

app.register_blueprint(InternalBlueprint)
app.register_blueprint(FaissIndexBlueprint)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
