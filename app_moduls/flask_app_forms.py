from flask_wtf import FlaskForm
from wtforms import StringField 
from wtforms.validators import DataRequired

class AppForms(FlaskForm):

    siteURL = StringField('siteURL', validators=[DataRequired()])
    element_attribute = StringField('element-attribute', validators=[DataRequired()])
