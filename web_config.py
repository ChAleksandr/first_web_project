def apply_config(app):
    app.config['SECRET_KEY'] = 'eclipse_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = r"sqlite:///D:\Python\eclipse\project eclipse\eclipse\db\blogs.db"
    app.config['CSRF_ENABLED'] = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'  # use the free broker from HIVEMQ
    app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
    app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
    app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
    app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 2 seconds
    app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes
