from python_flask.FlaskInstance import FlaskInstance


from python_flask import portal



def application_factory(test_config=None):
  flask_instance = FlaskInstance(test_config)

  flask_instance.RegisterBlueprint(portal.blueprint)

  return flask_instance.flask
