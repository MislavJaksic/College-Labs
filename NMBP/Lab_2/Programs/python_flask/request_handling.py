from flask import request



def ExtractComment():
  return request.form["comment"]

def IsMethodPOST():
  if (request.method == "POST"):
    return True
  return False
