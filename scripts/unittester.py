import requests
import json
import argparse

token = ''
url = ''

def check_params(paramlist, args):
    if "auction" in paramlist and args.auction == None:
        print("No auction specified") 
        exit(0)
    if "message" in paramlist and args.message == None:
        print("No Message specified")
        exit(0)
    if "amount" in paramlist and args.amount == None:
        print("No amount specified")
        exit(0)
    if "email" in paramlist and args.email == None:
        print("No email specified")
        exit(0)
    if "password" in paramlist and args.password == None:
        print("No password specified")
        exit(0)
    if "username" in paramlist and args.username == None:
        print("No username specified")
        exit(0)
    if "file" in paramlist and args.file == None:
        print("No filename specified")
        exit(0)
    if "amount" in paramlist and args.amount == None:
        print("No amount specified")
        exit(0)
    return True


def make_request(url, type, payload):
    headers = {'content-type': 'application/json'}
    if type == 'PUT':
        return requests.put(url, data=payload, headers=headers)
    if type == 'POST':
        return requests.post(url, data=payload, headers=headers)
    if type == 'GET':
        return requests.get(url, data=payload, headers=headers)
    return None

def get_login(username, password, filename):
    if filename is None:
        filename = 'token.tkn'
    payload = '{"username": "%s", "password" : "%s"}' % (username, password)
    r = make_request(url + f'/user', 'PUT', payload)
    try:
        tkn = r.json()["token"]
        with open(filename, "w") as f:
            f.write(tkn)
    except:
        return r
    return r

def create_user(username, password, email):
    payload = '{"username": "%s", "password" : "%s", "email" : "%s"}' % (username, password, email)
    return make_request(url + f'/user', 'POST', payload)
   

def make_bid(auction, amount):
    payload = '{"token": "%s", "price" : "%s"}' % (token,amount)
    return make_request(url + f'/licitation/{auction}', 'POST', payload)

def read_inbox():
    payload = '{"token": "%s"}' % token
    return make_request(url + f'/user/inbox', 'PUT', payload)

#Auction Operations
def create_auction():
    pass


def list_auctions():
    payload = '{"token": "%s"}' % token
    return make_request(url + f'/auctions', 'GET', payload)

def filter_auctions(keyword):
    payload = '{"token": "%s"}' % token
    return make_request(url + f'/auctions/{keyword}', 'GET', payload)

def post_mural(auction, message):
    payload = '{"token": "%s", "message" : "%s"}' % (token,message)
    return make_request(url + f'/auction/{auction}/mural', 'POST', payload)

def list_mural(auction):
    payload = '{"token": "%s"}' % token
    print(url + f'/auction/{auction}/mural')
    return make_request(url + f'/auction/{auction}/mural', 'PUT', payload)

#Admin Operations

def cancel_auction(id):
    payload = '{"token": "%s", "id" = "%s"}' % (token, id)
    return make_request(url + f'/admin/cancel', 'POST', payload)

def ban_user(id):
    payload = '{"token": "%s", "id" = "%s"}' % (token, id)
    return make_request(url + f'/admin/ban', 'POST', payload)

def get_stats():
    payload = '{"token": "%s"}' % token
    return make_request(url + f'/admin/stats', 'GET', payload)


    
def main():
    global token
    global url
    parser = argparse.ArgumentParser(description='Unit tester for the DB API')
    parser.add_argument('-l','--login', help='Defines the token',action='store_true')
    parser.add_argument('-tf','--tokenfile', help='Defines the token file path',action='store')
    parser.add_argument('-t','--token', help='Defines the token',action='store')
    parser.add_argument('-c','--createuser', help='Creates a new user in the db',action='store_true')
    parser.add_argument('-u','--username', help='Defines the username',action='store')
    parser.add_argument('-pw','--password', help='Defines the password',action='store')
    parser.add_argument('-e','--email', help='Defines the email',action='store')
    parser.add_argument('-m','--message', help='Sets Message', action='store')
    parser.add_argument('-f','--file', help='Set the filepath for saving the token',action='store')
    parser.add_argument('-p','--port', help='Sets the port where actions are gonna be called', action='store')
    parser.add_argument('-a','--auction', help='Sets the auction number', action='store')
    parser.add_argument('-id','--id', help='Sets the id (user or action) to be banned', action='store')
    parser.add_argument('-amt','--amount', help='Sets the amount for a bid', action='store')
    parser.add_argument('-li','--licitation', help='Make a licitation', action='store_true')
    parser.add_argument('-lm','--listmural', help='Shows the content of the mural for a certain auction', action='store_true')
    parser.add_argument('-pm','--postmural', help='Post the message to the mural', action='store_true')
    parser.add_argument('-la','--listauction', help='List auctions action', action='store_true')
    parser.add_argument('-bu','--banuser', help='List auctions action', action='store_true')
    parser.add_argument('-ca','--cancelauction', help='List auctions action', action='store_true')
    parser.add_argument('-sts','--getstats', help='List auctions action', action='store_true')

    args = parser.parse_args()
    print(args)
    port = args.port
    
    token = args.token
    url = f"http://localhost:{port}"


    if args.tokenfile != None:
        with open(args.tokenfile, "r") as f:
            data = f.readlines()[0]
            token = data
        args.tokenfile = "token.tkn"
    
    print(args)
 
    
    if args.login:
        check_params(['username', 'password'],args)
        r = get_login(args.username, args.password, args.file)
        print(json.dumps(r.json(), indent=2))

    if args.createuser:
        check_params(['username', 'password','email'],args)
        r = create_user(args.username, args.password,args.email)
        print(json.dumps(r.json(), indent=2))


    if args.listmural:
        check_params(['auction'],args)
        r = list_mural(args.auction)
        print(r)
        print(json.dumps(r.json(), indent=2))

    if args.postmural:
        check_params(['message', 'auction'], args)
        r = post_mural(args.auction, args.message)
        print(json.dumps(r.json(), indent=2))

    if args.licitation: 
        check_params(['auction', 'amount'],args)
        r = make_bid(args.auction, args.amount)
        print(r)
        print(json.dumps(r.json(), indent=2))

    if args.listauction: 
        r = list_auctions()
        print(json.dumps(r.json(), indent=2))

    if args.cancelauction: 
        check_params(['id'],args)
        r = cancel_auction(args.id)
        print(json.dumps(r.json(), indent=2))
    
    if args.banuser: 
        check_params(['id'],args)
        r = ban_user(args.id)
        print(json.dumps(r.json(), indent=2))
    
    if args.getstats: 
        r = get_stats()
        print(json.dumps(r.json(), indent=2))
    

if __name__ == '__main__':
    main()