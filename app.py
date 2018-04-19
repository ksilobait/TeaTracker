from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for, render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/tea'
db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')


class Brands(db.Model):
    brand_id = db.Column(db.INTEGER, primary_key=True)
    brand = db.Column(db.VARCHAR(100))
    tea_ref = db.relationship('Tea')

    def __init__(self, brand):
        self.brand = brand


@app.route('/add_brand', methods=['GET'])
def add_brand():
    all_brands = Brands.query.all()
    return render_template('add_brand.html', all_brands=all_brands)


@app.route('/post_brand', methods=['POST'])
def post_brand():
    brand = Brands(request.form['brand'])
    db.session.add(brand)
    db.session.commit()
    return redirect(url_for('add_brand'))


class Type(db.Model):
    type_id = db.Column(db.INTEGER, primary_key=True)
    type = db.Column(db.VARCHAR(50))
    tea_ref = db.relationship('Tea')

    def __init__(self, the_type):
        self.type = the_type


@app.route('/add_type', methods=['GET'])
def add_type():
    all_types = Type.query.all()
    return render_template('add_type.html', all_types=all_types)


@app.route('/post_type', methods=['POST'])
def post_type():
    the_type = Type(request.form['type'])
    db.session.add(the_type)
    db.session.commit()
    return redirect(url_for('add_type'))


class Profile(db.Model):
    tea_id = db.Column(db.INTEGER, primary_key=True)
    taste = db.Column(db.VARCHAR(300))
    rating = db.Column(db.INTEGER)

    def __init__(self, tea_id, taste, rating):
        self.tea_id = tea_id
        self.taste = taste
        self.rating = rating


@app.route('/add_profile', methods=['GET'])
def add_profile():
    all_profiles = Profile.query.all()
    return render_template('add_profile.html', all_profiles=all_profiles)


@app.route('/post_profile', methods=['POST'])
def post_profile():
    the_profile = Profile(request.form['tea_id'], request.form['taste'], request.form['rating'])
    db.session.add(the_profile)
    db.session.commit()
    return redirect(url_for('add_profile'))


class Ingredients(db.Model):
    ingredient_id = db.Column(db.INTEGER, primary_key=True)
    ingredient = db.Column(db.VARCHAR(300))

    def __init__(self, ingredient):
        self.ingredient = ingredient


@app.route('/add_ingredients', methods=['GET'])
def add_ingredients():
    all_ingredients = Ingredients.query.all()
    return render_template('add_ingredients.html', all_ingredients=all_ingredients)


@app.route('/post_ingredients', methods=['POST'])
def post_ingredients():
    the_ingredients = Ingredients(request.form['ingredient'])
    db.session.add(the_ingredients)
    db.session.commit()
    return redirect(url_for('add_ingredients'))


class IngredientsForTea(db.Model):
    tea_id = db.Column(db.INTEGER, primary_key=True)
    ingredient_id = db.Column(db.INTEGER, primary_key=True)

    def __init__(self, tea_id, ingredient_id):
        self.tea_id = tea_id
        self.ingredient_id = ingredient_id


@app.route('/add_ingredients_for_tea', methods=['GET'])
def add_ingredients_for_tea():
    all_ingredients = IngredientsForTea.query.all()
    return render_template('add_ingredients_for_tea.html', all_ingredients=all_ingredients)


@app.route('/post_ingredients_for_tea', methods=['POST'])
def post_ingredients_for_tea():
    the_ingredients = IngredientsForTea(request.form['tea_id'], request.form['ingredient_id'])
    db.session.add(the_ingredients)
    db.session.commit()
    return redirect(url_for('add_ingredients_for_tea'))


class Instances(db.Model):
    instance_id = db.Column(db.INTEGER, primary_key=True)
    best_before = db.Column(db.TIMESTAMP)
    left_weight = db.Column(db.INTEGER)
    left_bags = db.Column(db.INTEGER)
    tea_id = db.Column(db.INTEGER)

    def __init__(self, best_before, left_weight, left_bags, tea_id):
        self.best_before = best_before
        self.left_weight = left_weight
        self.left_bags = left_bags
        self.tea_id = tea_id


@app.route('/add_instances', methods=['GET'])
def add_instances():
    all_instances = Instances.query.all()
    return render_template('add_instances.html', all_instances=all_instances)


@app.route('/post_instances', methods=['POST'])
def post_instances():
    the_instances = Instances(request.form['best_before'], request.form['left_weight'],
                              request.form['left_bags'], request.form['tea_id'])
    db.session.add(the_instances)
    db.session.commit()
    return redirect(url_for('add_instances'))


class RatingsForTea(db.Model):
    tea_id = db.Column(db.INTEGER, primary_key=True)
    website_id = db.Column(db.INTEGER, primary_key=True)

    def __init__(self, tea_id, website_id):
        self.tea_id = tea_id
        self.website_id = website_id


@app.route('/add_ratings_for_tea', methods=['GET'])
def add_ratings_for_tea():
    all_ratings = RatingsForTea.query.all()
    return render_template('add_ratings_for_tea.html', all_ratings=all_ratings)


@app.route('/post_ratings_for_tea', methods=['POST'])
def post_ratings_for_tea():
    the_ratings = RatingsForTea(request.form['tea_id'], request.form['website_id'])
    db.session.add(the_ratings)
    db.session.commit()
    return redirect(url_for('add_ratings_for_tea'))


class Ratings(db.Model):
    website_id = db.Column(db.INTEGER, primary_key=True)
    website_name = db.Column(db.VARCHAR(100))

    def __init__(self, website_name):
        self.website_name = website_name


@app.route('/add_ratings', methods=['GET'])
def add_ratings():
    all_ratings = Ratings.query.all()
    return render_template('add_ratings.html', all_ratings=all_ratings)


@app.route('/post_ratings', methods=['POST'])
def post_ratings():
    the_ratings = Ratings(request.form['website_name'])
    db.session.add(the_ratings)
    db.session.commit()
    return redirect(url_for('add_ratings'))


class Tea(db.Model):
    tea_id = db.Column(db.INTEGER, primary_key=True)
    brand_id = db.Column(db.INTEGER, db.ForeignKey(Brands.brand_id))
    flavor = db.Column(db.VARCHAR(300))
    infuse_time = db.Column(db.TIME)
    is_tea_loose = db.Column(db.VARCHAR(40))
    tea_bags = db.Column(db.INTEGER)
    weight = db.Column(db.INTEGER)
    type_id = db.Column(db.INTEGER, db.ForeignKey(Type.type_id))

    def __init__(self, brand_id, flavor, infuse_time, is_tea_loose, tea_bags, weight, type_id):
        self.brand_id = brand_id
        self.flavor = flavor
        self.infuse_time = infuse_time
        self.is_tea_loose = is_tea_loose
        self.tea_bags = tea_bags
        self.weight = weight
        self.type_id = type_id


@app.route('/add_tea', methods=['GET'])
def add_tea():
    all_tea = Tea.query.all()
    return render_template('add_tea.html', all_tea=all_tea)


@app.route('/post_tea', methods=['POST'])
def post_tea():
    tea = Tea(request.form['brand_id'], request.form['flavor'], request.form['infuse_time'],
              request.form['is_tea_loose'], request.form['tea_bags'], request.form['weight'], request.form['type_id'])
    db.session.add(tea)
    db.session.commit()
    return redirect(url_for('add_tea'))


if __name__ == '__main__':
    app.run()

db.create_all()
