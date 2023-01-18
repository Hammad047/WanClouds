import datetime
from app import app
from flask_jwt_extended import JWTManager

jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "flask123."
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(seconds=30)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(minutes=1)
