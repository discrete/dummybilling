import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class Transaction(db.Model):
    """
    """
    account=db.StringProperty(required = True)
    when = db.DateTimeProperty(auto_now_add=True)
    amount = db.StringProperty(required = True)

class MainHandler(webapp.RequestHandler):
    """
    """
    def get(self):
        """
        
        Arguments:
        - `self`:
        """
        transactions = db.GqlQuery('SELECT * FROM Transaction ORDER BY when ASC')
        values = {
            'transactions': transactions
            }
        self.response.out.write(template.render('main.html', values))
        #self.response.headers['Content-Type'] = 'text/plain'
        #self.response.out.write(transactions.account)


    def post(self):
        """
        """
        transaction = Transaction(
            amount=self.request.get('amount'),
            account = self.request.get('account')
            )
        transaction.put()
        self.redirect('/')


class TransactionHandler(webapp.RequestHandler):
    """
    """
    def get(self):
        """
        
        Arguments:
        - `self`:
        """
        transaction = Transaction(
            amount=self.request.get('amount'),
            account = self.request.get('account')
            )
        transaction.put()
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(transaction.amount)

class BankbookHandler(webapp.RequestHandler):
    """
    """
    def get(self):
        """
        
        Arguments:
        - `self`:
        """
        transactions = db.GqlQuery('SELECT * FROM Transaction ORDER BY when ASC')
        self.response.headers['Content-Type'] = 'text/plain'
        for transaction in transactions:
        	self.response.out.write(transaction.account + " balance:" + transaction.amount)


def main():
    app = webapp.WSGIApplication([
            ('/', MainHandler),
            ('/transaction/', TransactionHandler),
            ('/bankbook/', BankbookHandler),
            ], debug = True)
    wsgiref.handlers.CGIHandler().run(app)

if __name__ == '__main__':
    main()
