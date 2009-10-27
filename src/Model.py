'''
Created on 24 Oct 2009

@author: shami
'''

from google.appengine.ext import db

class Project(db.Model):
    name = db.StringProperty(default="", required=True)
    
class Story(db.Model):
    name = db.StringProperty(default="Empty", required=True)
    project = db.ReferenceProperty(Project, collection_name='storyList')
    starPoint = db.IntegerProperty(default = 0)
    status = db.StringProperty(default="Not Done")
    
class Task(db.Model):
    name = db.StringProperty(default="name", required=True)
    story = db.ReferenceProperty(Story, collection_name='taskList')
    status = db.StringProperty(default="Not Started")
    estimate = db.StringProperty(default='0')