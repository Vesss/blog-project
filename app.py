import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)

app.config["MONGO_DBNAME"] = "blog_project"
app.config["MONGO_URI"] = "mongodb+srv://root:maniac93@myfirstcluster-ilypv.mongodb.net/blog_project?retryWrites=true&w=majority"

mongo = PyMongo(app)

@app.route("/")
def index():
	return render_template("index.html", sportspage=mongo.db.sports.find(), generalnewspage=mongo.db.general_news.find(), technologypage=mongo.db.technology.find(), healthpage=mongo.db.health.find(), travelpage=mongo.db.travel.find())
	
@app.route("/about")
def about():
	return render_template("about.html", about=mongo.db.about_information.find())
	
@app.route("/contact")
def contact():
	return render_template("contact.html")

	
@app.route("/post", methods=["GET", "POST"])
def post():
	if request.method == 'POST':
		#get all the data sent up
		data = request.form.to_dict()
		#print it out to see it got sent properly
		print(data)
		# will look at adding to database next if data is sent up ok
		
		# dict to store new entry to database  
		# will need to use keys you have in collection .. i named them title category etc
		new_item = {
			'title': request.form.get('title'),
			'author': request.form.get('author'),
			'url': request.form.get('url'),
			'content': request.form.get('content')
		}
		print(new_item)
		# need to get the category so can create the database string below
		category=request.form.get('category')
		print("category", category)
		# this should insert into the right collection eg sport health
		# if not will have to use if statements or switch
		mongo.db[category].insert_one(new_item)
		
		return redirect('/')
	else:
		return render_template('post.html')
	
@app.route("/articles")
def articles():
	return render_template("articles.html")
	
@app.route("/sports_page")
def sports_page():
	return render_template("sports_page.html", posts = mongo.db.sports.find())
	
@app.route("/general_news_page")
def general_news_page():
	return render_template("general_news.html", posts = mongo.db.general_news.find())

@app.route("/technology_page")
def technology_page():
	return render_template("technology_page.html", posts = mongo.db.technology.find())
	
@app.route("/travel_page")
def travel_page():
	return render_template("travel_page.html", posts = mongo.db.travel.find())

@app.route("/health_page")
def health_page():
	return render_template("health_page.html", posts = mongo.db.health.find())
	
if __name__ == "__main__":
	app.run(host=os.environ.get("IP"),
			port=int(os.environ.get("PORT")),
			debug=False)

