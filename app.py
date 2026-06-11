from flask import Flask, render_template, request, redirect, session, send_from_directory, send_file
import mydict, random
from random import randint


app = Flask(__name__)
app.secret_key = 'J$9a8*VgRm#fLp$5hQ7yT!sN3eX6wB4dO0Zu1cE2iGv'


@app.route("/home/")
@app.route("/")

def index():
	return render_template("index.html")


@app.route("/translate/")

def translate ():
	session['to_code'] = False
	return render_template('translate.html')



@app.route("/translate_to_code/")

def translate_to_code ():
	session['to_code'] = True
	return render_template('translate_to_code.html')



@app.route('/translation/',methods = ['POST', 'GET'])
def translation():
	# Mode switch: text → morse or morse → text based on session state
	to_code = session.get('to_code', False)


	result = request.form.to_dict(flat=False)
	result = (result['translation'])
	result =  "".join(result)
	result = result.upper()
	text_transl = ""
	character = ""
	char_in_dict = ""
	space = False
	error = False

	var_warning = False

	# Convert Morse code sequence into characters using lookup dictionary
	dictionary1 = mydict.morsedictionary
	

	if to_code == False:
		if len(result) == 0:
			var_warning = True
			return render_template("translate.html",var_warning = True)

		else:
			# Translation: Morse Code  to  Text
			# Parse Morse input:
			# - "." "-" build a character
			# - "/" separates letters or words
			# Ignore Spaces & Catching Errors

			for i in result:
				if i == "-" or i == ".":
					character = character + i
					space = False
				elif i == "/":
					if space == True:
						text_transl = text_transl+" "
						character = ""
					else:
						try:
							char_in_dict = dictionary1[character]
						except:
							error = True

						text_transl = text_transl + char_in_dict
						character = ""
					space = True
				elif i == " ":
					continue
				else:
					error = True
			if error == False:
				try:
					char_in_dict = dictionary1[character]
					text_transl = text_transl+char_in_dict
					character = ""
					result = text_transl
					return render_template("translation.html",result = result, to_code = False)
				except:
					return render_template("error.html", to_code = False)
			else:
				return render_template("error.html", to_code = False)

	else:

		dictionary2 = {value : key for (key, value) in dictionary1.items()}

		if len(result) == 0:
			var_warning = True
			return render_template("translate_to_code.html",var_warning = True)
		else:
			# Translation: Text to Morse Code
			code_transl = ""
			for k in result:
				if k == " ":
					code_transl = code_transl + "/ "
				else:
					try:
						char2_in_dict = dictionary2[k]
						code_transl = code_transl + "/"+ char2_in_dict
					except:
						error = True
			code_transl = "*" + code_transl
			code_transl = code_transl.replace('*/', '')



			if error == True:
				return render_template("error.html", to_code = True)
			else:
				to_code = True
				result = code_transl
				return render_template("translation.html", result = result , to_code = True)


@app.route('/training/')
def training():
	return render_template("training.html")



@app.route('/training/easy/', methods = ['POST', 'GET'])

def easy():

	if request.method == 'GET':

		# Randomly choose between normal and reversed dictionary for training variation
		dictchoice = randint(1,10)

		if dictchoice % 2 == 0:
			wordsdictionary = mydict.wordsdictionary
		else:
			wordsdictionary = mydict.wordsdictionaryopposite

		word = (random.choice(list(wordsdictionary.keys())))
		code = (wordsdictionary[word])

		session['word'] = word

		return render_template("easy.html", code = code)
	
	elif request.method == 'POST':

		result = request.form
		result = "".join(result.to_dict(flat=False)['wordtextarea'])
		result = result.upper()
		word = session.get('word')
		if result == word:
			return redirect("/training/easy/correct/")
		else:
			return redirect("/training/easy/wrong/")



@app.route('/training/hard/', methods = ['POST', 'GET'])

def hard():
	if request.method == 'GET':

		# Randomly choose between normal and reversed dictionary for training variation
		dictchoice_h = randint(1,10)
		
		if dictchoice_h % 2 == 0:
			wordsdictionary_h = mydict.wordsdictionaryhard
		else:
			wordsdictionary_h = mydict.wordsdictionaryhardopposite

		word_h = (random.choice(list(wordsdictionary_h.keys())))
		code_h = (wordsdictionary_h[word_h])

		session['word_h'] = word_h

		return render_template("hard.html", code = code_h)
	elif request.method == 'POST':

		result = request.form
		result = "".join(result.to_dict(flat=False)['wordtextarea_h'])
		result = result.upper()

		word_h = session.get('word_h')

		if result == word_h:
			return redirect("/training/hard/correct/")
		else:
			return redirect("/training/hard/wrong/")


@app.route('/lessons/1/')
def lesson_1():
	return render_template("lesson_1.html")

@app.route('/lessons/2/')
def lesson_2():
	return render_template("lesson_2.html")

@app.route('/lessons/3/')
def lesson_3():
	return render_template("lesson_3.html")

@app.route('/exercise/1/', methods = ['POST', 'GET'])
def exercise1():

	if request.method == 'GET':
		return render_template("exercise1.html")
	elif request.method == 'POST':
		anwser = request.form
		anwser = "".join(anwser.to_dict(flat=False)['exercise1'])
		anwser = anwser.upper()
		if anwser == "ADDITION":
			return render_template("exercise1.html", success = True)
		else:
			return render_template("exercise1.html", success = False)

@app.route('/lessons/4/')
def lesson_4():
	return render_template("lesson_4.html")

@app.route('/lessons/5/')
def lesson_5():
	return render_template("lesson_5.html")

@app.route('/lessons/6/')
def lesson_6():
	return render_template("lesson_6.html")

@app.route('/exercise/2/', methods = ['POST', 'GET'])
def exercise2():

	if request.method == 'GET':
		return render_template("exercise2.html")
	elif request.method == 'POST':
		anwser2 = request.form
		anwser2 = "".join(anwser2.to_dict(flat=False)['exercise2'])
		anwser2 = anwser2.upper()
		if anwser2 == "THE STUDENT TOLD THE TEACHER THAT 28,7+51,3=80. HE ANSWERED HIM: WELL DONE!":
			return render_template("exercise2.html", success = True)
		else:
			return render_template("exercise2.html", success = False)
@app.route('/dictionary/')
def dictionary():
	return render_template("dictionary.html")

@app.route('/contact/')
def contact():
	return render_template("contact.html")

@app.route('/about_us/')
def about_us():
	return render_template("about_us.html")

@app.route('/training/easy/correct/')
def correcteasy():
	return render_template("correct_easy.html")

@app.route('/training/easy/wrong/')
def wrongeasy():
	return render_template("wrong_easy.html")

@app.route('/training/hard/correct/')
def correcthard():
	return render_template("correct_hard.html")

@app.route('/training/hard/wrong/')
def wronghard():
	return render_template("wrong_hard.html")


@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')

@app.route('/history/')
def history():
	return render_template("history.html")

@app.route('/download/')
def download():
	return render_template("download.html")


@app.route('/download/download_file/')
def download_file():
	appversion = "morsecodelearn-1.2.apk"
	return send_file(appversion)


if __name__ == "__main__":
	app.run(debug=True)