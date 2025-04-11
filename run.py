print(">>> run.py loaded")

from app import create_app

print(">>> Calling create_app()")
app = create_app()
print(">>> App created")

print(">>> ROUTES REGISTERED:")
print(app.url_map)

if __name__ == "__main__":
    print(">>> Running Flask app...")
    app.run(debug=True)
