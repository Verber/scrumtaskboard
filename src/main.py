from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from Model import Project
from taskboard import TaskboardPage
from backlog import BacklogPage

class MainPage(webapp.RequestHandler):
    
    
    def get(self):
        user = users.get_current_user()

        if user:
            greeting = ('Hello %s <a href="%s">Sign out</a><br/>Project list' % 
                (user.nickname(), users.create_logout_url("/")))
            projectList = Project.all()
            projectView = "<table>"
            for project in projectList:
                projectView += ('<tr><div><td><a href="/project/%s/taskboard">%s</a> <a href="/main/deleteProject/%s">X</a></td></div></tr>' % (project.name, project.name, project.name))
            projectView += '</table>'
            form = """<form action="/main" method="post"> 
                <table>
                <tr>
                <div><td>Project Name</td><td><input type="text" name="projectName"></td></div> 
                </tr>
                </table>
                <div><input type="submit" value="Add project"></div>
                </form>"""
            self.response.out.write("<html><body>%s<br/>%s<br/>%s</body></html>" % (greeting, projectView, form))    
        else:
            self.redirect(users.create_login_url(self.request.uri))

    def post(self):
        projectName = self.request.get('projectName')
        project = Project(name=projectName)
        project.put()
        self.redirect("/project/%s/backlog"%projectName)
        
class DeleteProjectHandler(webapp.RequestHandler):
    def get(self, projectName):
        Project.gql(("WHERE name = '%s'" % projectName)).get().delete()
        self.redirect("/main")

application = webapp.WSGIApplication([('/', MainPage),
                                        ('/main', MainPage),
                                        #('/project/([^\/]*?)/backlog', BacklogPage),
                                        #('/project/([^\/]*?)/taskboard', Taskboard),
                                        ('/main/deleteProject/(.*?)', DeleteProjectHandler)
                                        ],
                                       debug=True)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
