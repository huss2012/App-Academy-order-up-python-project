from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app.models import Employee, Table, Order, Menu, MenuItem, MenuItemType
from app.forms import AssingTableForm, CloseTableForm, AddToOrderForm
from sqlalchemy import case
from wtforms import StringField
bp = Blueprint('orders',__name__, url_prefix="")

@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    from app import db

    form = AssingTableForm()
    close_table_form = CloseTableForm()
    add_to_order_form = AddToOrderForm()

    employees = Employee.query.all()
    tables = Table.query.all()
    orders = Order.query.all()
    menu = Menu.query.all()
    custom_name_order = case({"Entrees": 1, "Sides": 2, "Beverages": 3}, value= MenuItemType.name)
    menu_item_type = MenuItemType.query.order_by(custom_name_order).all()
    menu_item = MenuItem.query.all()


    #Loop through the MenuItemType to create dynamic StringField
    for menuItemType in menu_item_type:
        field_name = f"{menuItemType.name}"
        setattr(add_to_order_form, field_name, StringField(field_name))

    form.table.choices = [('', "Open Table")] + [(table.id, f"Table {table.number}") for table in tables]
    form.employee.choices= [('', "Server")] + [(employee.id, employee.name) for employee in employees]


    if form.validate_on_submit() and form.assing.data:
        selected_table = form.table.data
        selected_employee = form.employee.data
        return redirect(url_for('orders.assignTable', table_id=selected_table, employee_id=selected_employee))

    return render_template("orders.html",
                           form=form,
                           close_table_form=close_table_form ,
                           add_to_order_form=add_to_order_form,
                           orders=orders,
                           menu=menu,
                           menu_item_type=menu_item_type,
                           menu_item=menu_item
                           )


@bp.route("/<int:table_id><int:employee_id>", methods=['GET', "POST"])
@login_required
def assignTable(table_id, employee_id):
    from app import db

    table = Table.query.get(table_id)
    employee = Employee.query.get(employee_id)

    if not table or not employee:
        flash("Invalid table or employee selection", "danger")
        return redirect(url_for('prders.index'))

    open_order = Order.query.filter_by(table_id=table_id, finished=False).first()
    if open_order:
        flash(f"Table {table.number} is already assainged to another order.", "warning")
        return redirect(url_for('orders.index'))

    new_order = Order(employee_id=employee_id, table_id=table_id)

    db.session.add(new_order)
    db.session.commit()
    flash(f"Order succssfully assigned to Table {table.number} for {employee.name}", "success")
    return redirect(url_for('orders.index'))


@bp.route("/<int:order_id>", methods=["GET", "POST"])
@login_required
def claseTable(order_id):
    from app import db
    #search the database by primary key
    order= Order.query.get(order_id)
    if not order:
        flash("Order not found", "danger")
        return redirect(url_for('orders.index'))
    #mark the order finished to True
    order.finished = True
    #commit the change
    db.session.commit()
    flash(f"Order for Table {order.table.number} has been marked as sinished", "success")
    #redirect to orders.index
    return redirect(url_for('orders.index'))


@bp.route("/<int:order_id>", methods=["GET", "POST"])
@login_required
def addToOrder(order_id):
    from app import db
    #will take order_id & multible menu item ids:
    #Create OrderDetails object: for each menu item:
    #Save the change to the database:
    #Commit the changes to the database:
    #Return to the orders.index page:
    pass
