from website import create_app

app = create_app()

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('website/static', filename='uploads/' + filename), code=301)


if __name__ == "__main__":
    app.run(debug=True)