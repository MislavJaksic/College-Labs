import os
from flask import Flask

from python_flask.helpers import IsNone


class FlaskInstance(object):
  def __init__(self, test_config=None):
    self.test_config = test_config
  
    self.module_name = __name__
    self.is_config_relative_to_instance_folder = True
    
    self.secret_random_value = "dev"
    self.instance_folder_config_file = "config.py"
    self.is_ignore_missing_file = True
    
    self.flask = self.__CreateFlask()
    self.__SetConfigFromMapping()
    self.__CreateInstanceFolder()
    
  def __CreateFlask(self):
    return Flask(self.module_name,
                 instance_relative_config=self.is_config_relative_to_instance_folder)
               
  def __SetConfigFromMapping(self):
    self.flask.config.from_mapping(SECRET_KEY=self.secret_random_value)
                                       
    if (IsNone(self.test_config)):
      self.flask.config.from_pyfile(self.instance_folder_config_file,
                                    silent=self.is_ignore_missing_file)
    else:
      self.flask.config.from_mapping(test_config)
  
  def __CreateInstanceFolder(self):
    try:
      os.makedirs(self.flask.instance_path)
    except OSError:
      pass
    
    
    
  def RegisterBlueprint(self, blueprint):
    self.flask.register_blueprint(blueprint)
  
  def AddUrlRule(self, rule, endpoint=None):
    self.flask.add_url_rule(rule, endpoint=endpoint)
    
  def RegisterTeardownFunction(self, function):
    self.flask.teardown_appcontext(function)
  
  def RegisterCommand(self, command):
    self.flask.cli.add_command(command)



