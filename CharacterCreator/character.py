from flask import *
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# route for home page
@app.route('/', methods = ['GET', 'POST'])
def home_page():
    # display home page
    return render_template("home_page.html")

# route for character form
@app.route('/character_form.html', methods = ['GET', 'POST'])
def character_form():
    if request.method == 'POST':
        # Parse form data    
        c_name = request.form['name']
        c_race = request.form['race']
        c_class = request.form['class']
        c_background = request.form['background']
        c_alignment = request.form['alignment']

        c_age = request.form['age']
        c_hgt = request.form['hgt']
        c_wgt = request.form['wgt']
        c_eye = request.form['eye']
        c_skin = request.form['skin']
        c_hair = request.form['hair']

        c_str = request.form['str']
        c_dex = request.form['dex']
        c_con = request.form['con']
        c_int = request.form['int']
        c_wis = request.form['wis']
        c_cha = request.form['cha']

        # with sqlite3.connect('quiz.db') as con:
        #     try:
        #         cur = con.cursor()

        #         # update last row
        #         sql = ''' UPDATE quiz 
        #         SET qArray = qArray || ?, 
        #         optionArray = optionArray || ? 
        #         WHERE quizId = (SELECT MAX(quizId) FROM quiz)'''
        #         cur.execute(sql, (question, optArray))
        #         con.commit()
        #     except:
        #         con.rollback()
        # con.close()

        # redirct to test post
        return render_template("test_post.html", c_name=c_name, c_race=c_race, c_class=c_class, c_background=c_background, c_alignment=c_alignment, 
        c_age=c_age, c_hgt=c_hgt, c_wgt=c_wgt, c_eye=c_eye, c_skin=c_skin, c_hair=c_hair, c_str=c_str, c_dex=c_dex, c_con=c_con,
        c_int=c_int, c_wis=c_wis, c_cha=c_cha)    
    
    else:
        # display the character form
        return render_template("character_form.html")

# route for test post
@app.route('/test_post.html', methods = ['GET', 'POST'])
def test_post():
    # display the test post
    return render_template("test_post.html")

if __name__ == '__main__':
    app.run(debug=True)