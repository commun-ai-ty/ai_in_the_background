from website import create_app

app = create_app()

if __name__ == "__main__":
    # Set threaded=True so a slow image-generation request doesn't block the whole server
    app.run(host="localhost", port=8094, debug=True, threaded=True)
