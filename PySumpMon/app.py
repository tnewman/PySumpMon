from PySumpMon.controllers import app


def run():
    app.run(host='0.0.0.0', debug=True, use_reloader=False)

if __name__ == '__main__':
    run()
