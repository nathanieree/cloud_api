from flask import Flask
from routes import home_bp, pokemon_bp, weather_bp, spotify_bp, wikipedia_bp

app = Flask(__name__, template_folder='template', static_folder='static')





# Register Blueprints
app.register_blueprint(home_bp)
app.register_blueprint(pokemon_bp)
app.register_blueprint(weather_bp)
app.register_blueprint(spotify_bp)
app.register_blueprint(wikipedia_bp)



if __name__ == '__main__':
    app.run(debug=True)
