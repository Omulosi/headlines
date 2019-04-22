from flask import Flask, render_template
from config import Config


def create_app(config=Config):

	app = Flask(__name__)
	app.config.from_object(config)

	from headlines.main import bp as main_bp
	app.register_blueprint(main_bp)

	@app.route('/index')
	def index():
		return render_template('base.html')

	return app
