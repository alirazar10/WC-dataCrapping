from flask import Flask, render_template, request
from app_moduls.flask_app_forms import AppForms
from app_moduls.scrapping import ScrapWebPage

app = Flask(__name__)
app.secret_key = 'development key'

@app.route("/")
def home():
    app_form = AppForms()
    return render_template('index.html', form=app_form)

@app.route('/scrap', methods=['GET', 'POST'])
def scrap():
    scrap = ScrapWebPage()
    page_URL = request.form['siteURL']
    product_links = scrap.get_product_links(page_URL)
    return scrap.get_product_info(product_links)
    return 'hello scraping'

if __name__ == "__main":
    app.run(debug=True)

