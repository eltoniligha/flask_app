from app import create_app
from flasgger import Swagger

app = create_app()
swagger = Swagger(app)

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
