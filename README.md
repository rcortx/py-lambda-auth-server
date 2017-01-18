py-lambda-auth-server

# A REST authorization microservice in python for AWS Lambda

### deploys a highly extensible microframework with stackable middleware architecture

Here's a brief on the architecture:  

layer(s) of middlewares process the request before it reaches the view layer. 
The middlewares are responsible for preprocessing, authorization and delegation to subsequent layers which may be more middlewares or a ROUTER, which will route requests to an appropriate VIEW.

A strict decoupling has been employed between Authorizers and Middleware where the latter aggregates the former for usage in authentication and authorization.

In order to fabricate a plug and play architecture, multiple normalized middlewares have been chosen over a monolithic object. 

Aim was to achieve DRY, i.e. not having to write a single line of AUTH or preprocessing code ever again and deriving any required  preprocessing/auth functionality through any permutation and combination of preexisting or customized middlewares.

These middlewares won't only be used for AUTH but for any processing or postprocessing of requests and responses passing through them to achieve predictable cohesion. 

This has been demonstrated in the code where I use different middlewares and authorizers to reject 'UNSAFE' http methods or reject any method other than 'POST' while authenticating.
