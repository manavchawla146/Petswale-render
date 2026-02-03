from PetPocket import create_app
from PetPocket.config import DevelopmentConfig

app = create_app(DevelopmentConfig)

if __name__ == "__main__":
    app.run(debug=True)
