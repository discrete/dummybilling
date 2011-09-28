import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from django.utils import simplejson

class Transaction(db.Model):
    """
    """
    account=db.StringProperty(required = True)
    when = db.DateTimeProperty(auto_now_add=True)
    amount = db.StringProperty(required = True)

    def to_dict(self):
        return dict([(p, unicode(getattr(self, p))) for p in self.properties()])

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
        self.response.out.write(simplejson.dumps([transaction.to_dict() for transaction in transactions]))

class BalanceHandler(webapp.RequestHandler):
    """
    """
    def get(self):
        """
        
        Arguments:
        - `self`:
        """
        balance = 0
        account = self.request.get('account')
        transactions = db.GqlQuery('SELECT * FROM Transaction WHERE account = :1 ORDER BY when ASC', account)
        #balances = db.GqlQuery('SELECT * FROM Transaction ORDER BY when ASC')
        self.response.headers['Content-Type'] = 'text/plain'
        for transaction in transactions:
        	balance = balance + int(transaction.amount)
        self.response.out.write(balance)

class TestHandler(webapp.RequestHandler):
    """
    """
    def get(self):
        """
        
        Arguments:
        - `self`:
        """
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write("100")

def main():
    app = webapp.WSGIApplication([
            ('/', MainHandler),
            ('/api/transaction', TransactionHandler),
            ('/api/bankbook', BankbookHandler),
            ('/api/balance', BalanceHandler),
            ('/api/test', TestHandler)
            ], debug = True)
    wsgiref.handlers.CGIHandler().run(app)

if __name__ == '__main__':
    main()
