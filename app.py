from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "key"
app.debug = True
toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False


@app.route('/')
def home():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home.html', title=title, instructions=instructions)

@app.route('/questions/<num>')
def survey_questions(num):
    if "responses" not in session:
        flash('Please hit start survey to begin')
        return redirect('/')
    num = int(num)
    if num != len(session["responses"]):
        flash('Unauthorized access to this page please complete the survey')
        return redirect(f'/questions/{len(session["responses"])}')
    if num == len(satisfaction_survey.questions):
        return redirect('/thankyou')
    return render_template('questions.html', num=num, question = satisfaction_survey.questions[num])

@app.route('/answer', methods=["POST"])
def submit_answer():
    res = request.form['answer']
    responses = session["responses"]
    responses.append(res)
    session["responses"] = responses
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thankyou')
    return redirect(f"/questions/{len(responses)}")

@app.route('/thankyou')
def thankyou_page():
    responses = session.get("responses", [])
    if not responses or len(responses) != len(satisfaction_survey.questions):
        flash('Unauthorized access to this page. Please complete the survey.')
        next_question = 0 if not responses else len(responses)
        return redirect(f"/questions/{next_question}")
    
    return render_template('thankyou.html')

@app.route('/startsurvey', methods=["POST"])
def start_survey():
    session['responses'] = []
    return redirect(f'/questions/{len(session["responses"])}')