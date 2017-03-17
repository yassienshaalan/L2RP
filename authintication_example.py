from auth0.v2.management import Auth0

domain = 'myaccount.auth0.com'
token = 'A_JWT_TOKEN' # You can generate one of these by using the
                        # token generator at: https://auth0.com/docs/api/v2

auth0 = Auth0('myaccount.auth0.com', token)
auth0.connections.all()
print("hi i am done")

