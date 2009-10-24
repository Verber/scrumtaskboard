'''
Created on 24 oct. 2009

@author: verber
'''
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from Model import Project, Task, Story
import os


class Taskboard(webapp.RequestHandler):
    '''
    classdocs
    '''
    def get(self, projectName):
        #self.response.headers['Content-Type'] = 'text/plain'
        #self.response.out.write('Hello, '+proj_name)
        
        project = Project.gql(("WHERE name = '%s'" % projectName)).get()
        
        template_values = {
            'proj_name':   projectName,
            'stories':     project.storyList
        }
        
        path = os.path.join(os.path.dirname(__file__), 'taskboard', 'index.html')
        self.response.out.write(template.render(path, template_values))
        
        def post(self, projectName):
            taskName = self.request.post('taskName')
            currentStory = Story.get(self.request.post('storyKey'))
            task = Task(name=taskName, story = currentStory)
            task.put()
            
        
application = webapp.WSGIApplication(
                                     [('/project/(.*?)/taskboard', Taskboard)],
                                     debug=True)
    

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()