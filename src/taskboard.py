'''
Created on 24 oct. 2009

@author: verber
'''
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from Model import Project, Task, Story
from django.utils import simplejson
import os


class TaskboardPage(webapp.RequestHandler):
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
        try:
            task = Task(name=self.request.get('name'),
                        estimate=self.request.get('estimate'),
                        story=Story.get(self.request.get('storyKey')))
            task.put()
            result = {
                'success':  True,
                'message':  'Task created',
                'task_key': str(task.key())
            }
        except:
            result = {
                'success': False,
                'message': sys.exc_info()[0]
            }
        self.response.out.write(simplejson.dumps(result))


class TaskboardJSONRPC(webapp.RequestHandler):

    def post(self):
        try:
            task = Task.get(self.request.get('key'))
            task.status = self.request.get('status')
            task.put()
            result = {
                'success':  True,
                'message':  'Task\'s status changed'
            }
        except:
            result = {
                'success': False,
                'message': sys.exc_info()[0]
            }
        self.response.out.write(simplejson.dumps(result))

            
        
application = webapp.WSGIApplication(
                                     [
                                        ('/project/(.*?)/taskboard', TaskboardPage),
                                        ('/taskboard/set_status', TaskboardJSONRPC)
                                     ],
                                     debug=True)
    

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()