from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for, render_template
from flask_table import Table, Col

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/tea'
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.route('/')
def index():
    return render_template('index.html')


# THE BRANDS
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


# THE TYPE
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


# THE INGREDIENTS //TODO
class Ingredients(db.Model):
    ingredient_id = db.Column(db.INTEGER, primary_key=True)
    ingredient = db.Column(db.VARCHAR(300))

    ift_reference = db.relationship('IngredientsForTea')

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


# THE TEA # TODO
class Tea(db.Model):
    tea_id = db.Column(db.INTEGER, primary_key=True)
    brand_id = db.Column(db.INTEGER, db.ForeignKey(Brands.brand_id))
    flavor = db.Column(db.VARCHAR(300))
    infuse_time = db.Column(db.INTEGER)
    is_tea_loose = db.Column(db.VARCHAR(40))
    tea_bags = db.Column(db.INTEGER)
    weight = db.Column(db.INTEGER)
    type_id = db.Column(db.INTEGER, db.ForeignKey(Type.type_id))
    taste = db.Column(db.VARCHAR(300))
    rating = db.Column(db.INTEGER)

    inst_ref = db.relationship('Instances')
    ift_reference = db.relationship('IngredientsForTea')

    def __init__(self, brand_id, flavor, infuse_time, is_tea_loose, tea_bags, weight, type_id, taste, rating):
        self.brand_id = brand_id
        self.flavor = flavor
        self.infuse_time = infuse_time
        self.is_tea_loose = is_tea_loose
        self.tea_bags = tea_bags
        self.weight = weight
        self.type_id = type_id
        self.taste = taste
        self.rating = rating


class TeaTable(Table):
    brand = Col('Brand')
    flavor = Col('Flavor')
    infuse_time = Col('Infuse time (mins)')
    is_tea_loose = Col('Loose tea?')
    tea_bags = Col('Tea bags')
    weight = Col('Weight')
    type = Col('Type')
    taste = Col('Taste')
    rating = Col('Rating')


@app.route('/add_tea', methods=['GET'])
def add_tea():
    all_brands = Brands.query.all()
    all_types = Type.query.all()

    all_tea = Tea.query.join(Brands, Tea.brand_id == Brands.brand_id).join(Type, Type.type_id == Tea.type_id).add_columns(Brands.brand, Tea.flavor, Tea.infuse_time, Tea.is_tea_loose, Tea.tea_bags, Tea.weight, Type.type, Tea.taste, Tea.rating)

    table = TeaTable(all_tea)
    table.border = True
    return render_template('add_tea.html', all_tea=all_tea, all_brands=all_brands, all_types=all_types, table=table)


@app.route('/post_tea', methods=['POST'])
def post_tea():
    tea = Tea(request.form['brand_id'], request.form['flavor'], request.form['infuse_time'],
              request.form['is_tea_loose'], request.form['tea_bags'], request.form['weight'], request.form['type_id'],
              request.form['taste'], request.form['rating'])

    db.session.add(tea)
    db.session.commit()
    return redirect(url_for('add_tea'))


class IFTTable(Table):
    ingredient = Col('ingredient')
    taste = Col('taste')


# THE INGREDIENTS FOR TEA //TODO
class IngredientsForTea(db.Model):
    tea_id = db.Column(db.INTEGER, db.ForeignKey(Tea.tea_id), primary_key=True)
    ingredient_id = db.Column(db.INTEGER, db.ForeignKey(Ingredients.ingredient_id), primary_key=True)

    def __init__(self, tea_id, ingredient_id):
        self.tea_id = tea_id
        self.ingredient_id = ingredient_id


@app.route('/add_ingredients_for_tea', methods=['GET'])
def add_ingredients_for_tea():
    all_tea = Tea.query.all()
    all_ingredients = Ingredients.query.all()

    all_ift = IngredientsForTea.query.join(Tea, IngredientsForTea.tea_id == Tea.tea_id)\
        .join(Ingredients, Ingredients.ingredient_id == IngredientsForTea.ingredient_id)\
        .add_columns(Ingredients.ingredient, Tea.taste)
    table = IFTTable(all_ift)
    table.border = True

    return render_template('add_ingredients_for_tea.html', all_ingredients=all_ingredients, all_tea=all_tea, table=table)


@app.route('/post_ingredients_for_tea', methods=['POST'])
def post_ingredients_for_tea():
    the_ingredients = IngredientsForTea(request.form['tea_id'], request.form['ingredient_id'])
    db.session.add(the_ingredients)
    db.session.commit()
    return redirect(url_for('add_ingredients_for_tea'))


# THE INSTANCES
class Instances(db.Model):
    instance_id = db.Column(db.INTEGER, primary_key=True)
    best_before = db.Column(db.DATE)
    left_weight = db.Column(db.INTEGER)
    left_bags = db.Column(db.INTEGER)
    tea_id = db.Column(db.INTEGER, db.ForeignKey(Tea.tea_id))

    def __init__(self, best_before, left_weight, left_bags, tea_id):
        self.best_before = best_before
        self.left_weight = left_weight
        self.left_bags = left_bags
        self.tea_id = tea_id


class InstancesTable(Table):
    taste = Col('tea taste')
    best_before = Col('best_before')
    left_weight = Col('left_weight')
    left_bags = Col('left_bags')


@app.route('/add_instances', methods=['GET'])
def add_instances():
    some_instances = Instances.query.join(Tea, Instances.tea_id == Tea.tea_id)\
        .filter(((Instances.left_weight > 0) | (Instances.left_bags > 0)) & (Instances.best_before >= date.today()))\
        .add_columns(Tea.taste, Instances.best_before, Instances.left_weight, Instances.left_bags)
    table = InstancesTable(some_instances)
    table.border = True

    no_instances = Instances.query.join(Tea, Instances.tea_id == Tea.tea_id)\
        .filter(~(((Instances.left_weight > 0) | (Instances.left_bags > 0)) & (Instances.best_before >= date.today())))\
        .add_columns(Tea.taste, Instances.best_before, Instances.left_weight, Instances.left_bags)
    table2 = InstancesTable(no_instances)
    table2.border = True

    all_tea = Tea.query.all()

    return render_template('add_instances.html', table=table, table2=table2, all_tea=all_tea)


@app.route('/post_instances', methods=['POST'])
def post_instances():
    the_instances = Instances(request.form['best_before'], request.form['left_weight'],
                              request.form['left_bags'], request.form['tea_id'])
    db.session.add(the_instances)
    db.session.commit()
    return redirect(url_for('add_instances'))


if __name__ == '__main__':
    manager.run()

db.create_all()
