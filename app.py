from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:ontrobait@localhost/tea'
db = SQLAlchemy(app)


class Tea(db.Model):
    tea_id = db.Column(db.Integer, primary_key=True)
    brand_id = db.Column(db.INTEGER)
    flavor = db.Column(db.VARCHAR(300))
    infuse_time = db.Column(db.TIME)
    is_tea_loose = db.Column(db.BOOLEAN)
    tea_bags = db.Column(db.INTEGER)
    weight = db.Column(db.INTEGER)
    type_id = db.Column(db.INTEGER)
    # total_tea_trigger = db.Column(db.INTEGER)

    def __init__(self, brand_id, flavor, infuse_time, is_tea_loose, tea_bags, weight, type_id):
        self.brand_id = brand_id
        self.flavor = flavor
        self.infuse_time = infuse_time
        self.is_tea_loose = is_tea_loose
        self.tea_bags = tea_bags
        self.weight = weight
        self.type_id = type_id

    def __repr__(self):
        return self.tea_id


@app.route('/')
def index():
    return render_template('add_tea.html')


@app.route('/post_tea', methods=['POST'])
def post_tea():
    return "help"


if __name__ == '__main__':
    app.run()

db.create_all()
