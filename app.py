from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "key"
app.debug = True
toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False

responses = []

@app.route('/')
def home():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home.html', title=title, instructions=instructions)

@app.route('/questions/<num>')
def survey_questions(num):
    numQ = len(responses)
    if numQ != int(num):
        flash('Unauthorized access to this page please complete the survey')
    if numQ == len(satisfaction_survey.questions):
        print(responses)
        return redirect('/thankyou')
    return render_template('questions.html', num=numQ, question = satisfaction_survey.questions[numQ])

@app.route('/answer', methods=["POST"])
def submit_answer():
    answer = request.form['answer']
    print(answer)
    responses.append(answer)
    if len(responses) == len(satisfaction_survey.questions):
        print(responses)
        return redirect('/thankyou')
    return redirect(f"/questions/{len(responses)}")

@app.route('/thankyou')
def thankyou_page():
    if len(responses) != len(satisfaction_survey.questions):
        flash('Unauthorized access to this page please complete the survey')
        return redirect(f"/questions/{len(responses)}")
    return render_template('thankyou.html')