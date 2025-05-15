#authorization , #netflix

Authenticate and Authorize 3M RPS
Complex signals - Fraud, device

Previously:
Client ---Access Token---> Edge Router ----> Downstream (authz)-----> Identity Provider

Authz rules replicated in code hundreds of time
Different microservices have same authz roles

Pros:
1. Scalable
2. Failure domain isolation

Cons:
1. Policies are simple - if you have membership, you get stuff ; when complexity is added it is distributed
2. Difficult to change
3. Exceptional access is exceptionally difficult.
4. Fraud awareness is localized


What is being authorized?
1. Product features 
2. Videos to playback or download
3. Asset discovery
4. 