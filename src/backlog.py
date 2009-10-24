'''
Created on 24 oct 2009

@author: shami
'''
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from Model import Story, Project

class BacklogPage(webapp.RequestHandler):
    
    
    def get(self, projectName):
        user = users.get_current_user()

        if user:
            greeting = ('Hello %s <a href="%s">Sign out</a><br/><a href="/main">Projects</a><br/> Backlog for %s' % 
                (user.nickname(), users.create_logout_url("/"), projectName))
            project = Project.gql(("WHERE name = '%s'" % projectName)).get()
            storyView = "<table><tr><div><th>Name</th><th>Story Points</th></div></tr>"
            for story in project.storyList:
                storyView += ('<tr><div><td>%s</td><td>%s</td></div></tr>' % (story.name, story.starPoint))
            storyView += '</table>'
            form = ("""<form action="/project/%s/backlog" method="post"> 
                <table>
                <tr>
                <div><td>Stroy Name</td><td><input type="text" name="storyName"></td></div> 
                </tr>
                <tr>
                <div><td>Star Proint</td><td><input type="text" name="starPoint"></td></div> 
                </tr>
                
                </table>
                <div><input type="submit" value="Add story"></div>
                </form>""" % projectName)
            self.response.out.write("<html><body>%s<br/>%s<br/>%s</body></html>" % (greeting, storyView, form))    
        else:
            self.redirect(users.create_login_url(self.request.uri))

    def post(self, projectName):
        storyName = self.request.get('storyName')
        starPoints = self.request.get('starPoint')
        currentProject = Project.gql(("WHERE name = '%s'" % projectName)).get()
        story = Story(name=storyName, starPoint=int(starPoints), project = currentProject)
        story.put()
        self.redirect("/project/%s/backlog"%projectName)

application = webapp.WSGIApplication([('/project/(.*?)/backlog', BacklogPage)],
                                       debug=True)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
