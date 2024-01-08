from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Record
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .forms import SignUpForm, AddRecordForm  # Import your form classes

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    records = Record.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", user=current_user, records=records)

@views.route('/customer-record/<int:pk>', methods=['GET'])
@login_required
def customer_record(pk):
    customer_record = Record.query.get_or_404(pk)
    if customer_record.user_id == current_user.id:
        return render_template("record.html", user=current_user, customer_record=customer_record)
    else:
        flash('You do not have permission to view this record.', category='error')
        return redirect(url_for('views.home'))

@views.route('/delete-record/<int:pk>', methods=['POST'])
@login_required
def delete_record(pk):
    record = Record.query.get_or_404(pk)
    if record.user_id == current_user.id:
        db.session.delete(record)
        db.session.commit()
        flash('Record deleted successfully!', category='success')
    else:
        flash('You do not have permission to delete this record.', category='error')
    return redirect(url_for('views.home'))

@views.route('/add-record', methods=['GET', 'POST'])
@login_required
def add_record():
    form = AddRecordForm()  # Create an instance of your form class
    if form.validate_on_submit():
        new_record = Record(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, phone=form.phone.data, address=form.address.data, city=form.city.data, state=form.state.data, country=form.country.data, pincode=form.pincode.data, user_id=current_user.id)
        db.session.add(new_record)
        db.session.commit()
        flash('Record added successfully!', category='success')
        return redirect(url_for('views.home'))
    return render_template("add_record.html", user=current_user, form=form)  # Pass the form to the template

@views.route('/update-record/<int:pk>', methods=['GET', 'POST'])
@login_required
def update_record(pk):
    record = Record.query.get_or_404(pk)
    if record.user_id == current_user.id:
        form = AddRecordForm(obj=record)  # Create a form instance with the record data
        if request.method == 'POST':
            if form.validate_on_submit():
                form.populate_obj(record)  # Update the record with the form data
                db.session.commit()
                flash('Record updated successfully!', category='success')
                return redirect(url_for('views.home'))
        return render_template("update_record.html", user=current_user, record=record, form=form)  # Pass the form to the template
    else:
        flash('You do not have permission to update this record.', category='error')
        return redirect(url_for('views.home'))
