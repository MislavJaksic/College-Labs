import pymongo
from flask import Blueprint, render_template, url_for, redirect

from python_flask.request_handling import IsMethodPOST, ExtractComment
from python_flask.sql_queries import GetArticles, AddCommentById
from python_flask.helpers import IsNone



blueprint_name = "portal"
module_name = __name__
blueprint = Blueprint(blueprint_name,
                      module_name)



@blueprint.route("/", methods=("GET", "POST"))
def Index():
  template_path = "portal/articles.html"
  articles = GetArticles()
  return render_template(template_path, articles=articles)

@blueprint.route("/<string:id>/comment", methods=("GET", "POST"))
def Comment(id):
  if IsMethodPOST():
    comment = ExtractComment()
    
    error = CheckComment(comment)

    if IsNone(error):
      AddCommentById(comment, id)
      url = GetEndpointUrl("portal.Index")
      return redirect(url)
  
  template_path = "portal/comment.html"
  return render_template(template_path)



def CheckComment(comment):
  error = None

  if IsNone(comment):
    error = "No comment"
  
  return error



def GetEndpointUrl(endpoint):
  return url_for(endpoint)

