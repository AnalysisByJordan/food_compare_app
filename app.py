from flask import Flask, render_template, request, flash, url_for, redirect, session
from fetch import get_foods, get_food_list, get_food_nutrients, get_food_name
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

app = Flask(__name__)
app.config['SECRET_KEY'] = '81565977645e6138e56f590d1213b437537f9ebaa171e8f6'


@app.route('/')
def index():
   session['reload_flag'] = False
   logging.info(f"session['food1'] = {session['food1']}")
   if session['food1']:
      food1 = session['food1']
   else:
      food1 = ''
   if session['food2']:
      food2 = session['food2']
   else:
      food2 = ''
   return render_template('index.html', food1=food1, food2=food2)

@app.route('/about')
def about():
   return render_template('about.html')

@app.route('/comparison', methods = ['GET', 'POST'])
def comparison():
   if request.method == 'POST':
      if not session['reload_flag']:
         session['food1'] = request.form.get('food1')
         session['food2'] = request.form.get('food2')
         if not (request.form.get('food1') and request.form.get('food2')):
            flash("Please fill in all food fields")
            return redirect('/')
      logging.info(f"Loading page with session['reload_flag] = {session['reload_flag']}")
      food1_dict = get_foods(session['food1'])
      food2_dict = get_foods(session['food2'])
      food1_list = get_food_list(food1_dict)
      food2_list = get_food_list(food2_dict)
      if not (request.form.get('food1_select') and request.form.get('food1_select')):
         food1_nutrients = food2_nutrients = 'Please select a specific food then hit "Go"'
         food1_id = food2_id = None
         session['reload_flag'] = True
      if request.form.get('food1_select'):
         logging.info(f"Trying to find nutrients for {get_food_name(food1_dict, request.form.get('food1_select'))} - {request.form.get('food1_select')} and {get_food_name(food2_dict, request.form.get('food2_select'))} - {request.form.get('food2_select')}")
         food1_nutrients = get_food_nutrients(food1_dict, request.form.get('food1_select'))
         food2_nutrients = get_food_nutrients(food2_dict, request.form.get('food2_select'))
         food1_id = int(request.form.get('food1_select'))
         food2_id = int(request.form.get('food2_select'))
         logging.info(f"food1_id = {food1_id}, food2_id = {food2_id}")
   return render_template('comparison.html', food1 = session['food1'], food2 = session['food2'], food1_list = food1_list, food2_list = food2_list, \
   food1_nutrients=food1_nutrients, food2_nutrients=food2_nutrients, food1_id = food1_id, food2_id = food2_id)

if __name__ == '__main__':
   app.run()