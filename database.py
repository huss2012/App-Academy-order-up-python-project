from dotenv import load_dotenv
load_dotenv()

# Regardless of the lint error you receive,
# load_dotenv must run before running this
# so that the environment variables are
# properly loaded.
from app import app, db
from app.models import Employee, Menu, MenuItem, MenuItemType, Table


with app.app_context():
    db.drop_all()
    db.create_all()

    employee = Employee(name="Margot", employee_number=1234, password="password")
    db.session.add(employee)

    beverages  = MenuItemType(name="Beverages")
    entrees = MenuItemType(name="Entrees")
    sides = MenuItemType(name="Sides")
    dinner = Menu(name="Dinner")
    fries = MenuItem(name="French fries", price=3.5, type=sides, menu=dinner)
    drp = MenuItem(name="Dr. Pepper", price=1.0, type=beverages, menu=dinner)
    jambalaya = MenuItem(name="Jambalaya", price=21.98, type=entrees, menu=dinner)

    chicken_kiev = MenuItem(name="Chicken Kiev", price=12.0, type=entrees, menu=dinner)
    deep_fried_onions = MenuItem(name="Deep Fried Oniun", price=3.9, type=sides, menu=dinner)
    tea = MenuItem(name="Tea", price=2.5, type=beverages, menu=dinner)
    db.session.add(dinner) # Add one and SQLAlchemy will handel the adding the rest due to the relationship defined in the model class definetion


    table_data = [(i, i*2) for i in range(1, 11)]
    table_object = [Table(number=tableNum, capacity=tableCapacity) for tableNum, tableCapacity in table_data]
    db.session.add_all(table_object)





    db.session.commit()
