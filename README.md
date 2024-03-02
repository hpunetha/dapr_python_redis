# Dapr pub/sub

## Background
This repo uses python flask based REST-API microservices, redis and dapr runtime to enable publish-subscribe pattern. I have included docker-compose in it to run it as full fledged app in the system including all components.

For more details about this quickstart example please see the [Pub-Sub Quickstart documentation](https://docs.dapr.io/getting-started/quickstarts/pubsub-quickstart/).

Visit [this](https://docs.dapr.io/developing-applications/building-blocks/pubsub/) link for more information about Dapr and Pub-Sub.


This quickstart includes one publisher:

- Python client message generator `checkout` 

And one subscriber: 
 
- Python subscriber `order-processor`

### Pre-requisites

- [Dapr CLI](https://docs.dapr.io/getting-started/install-dapr-cli/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
<!-- END_IGNORE -->

# Running using docker-compose

- A docker compose file is created to dockerize the checkout and order processing.  
Use below commands to run :-  
  - ```docker-compose build```  
  - ```docker-compose up```  

  Redis is used as message-broker, docker-compose will create all the containers including microservices and redis container.
- Send event using postman or by using python script.  

  - Using Postman.  
    Send below json in body of the message.

    ```json
    {
      "orderId": "anyorderid"
    } 
    ```
  - Using curl
    ```curl
    curl --location 'http://localhost:3000/publish' \
      --header 'Content-Type: application/json' \
      --data '{
          "orderId": "testorder12345"
      }'
    ```

- Sample output
  ![req-resp](./outputsamples/request_response_sample.png)

# Running using Kubernetes

- Tested with Docker-Desktop's inbuilt kubernetes offering. Enable Kubernetes in the settings of Docker desktop.  

  - Create a namespace in kubernetes cluster using  
    ```kubectl create namespace test```  
  - Set the namespace as default using  
    ```kubectl config set-context --current --namespace=test```  
  - Install Dapr to kubernetes namespace (requires [Dapr CLI](https://docs.dapr.io/getting-started/install-dapr-cli/) to be installed in system)  
    ```dapr init -k  -n test```  
    Above will install all the dependencies of dapr
  
  - Change to directory dapr_python_redis\dapr\kubernetes and then run below command  
    ```kubectl apply -f pubsub.yaml -n test```  
    Above command will add the pubsub binding we use for communicating with redis
  
  - Change back to root directory of the repo and run below commands -
    ```sh
    kubectl apply -f kubedeploy-checkout.yml -n test
    kubectl apply -f  kubedeploy-orders.yml -n test
    kubectl apply -f kubedeploy-redis.yml  -n test
    ```
  - Check if all services and pods are up using Lens or with cli using below commands  
    ```
    kubectl get pods -n test
    kubectl get service -n test
    ```
  
  - Send event from postman or using curl using same approach as in docker-compose.    
  
- Sample output
  ![req-resp](./outputsamples/kubernetes_run.png)

# Reference links

https://docs.dapr.io/getting-started/  
https://docs.dapr.io/getting-started/quickstarts/pubsub-quickstart/  
https://docs.dapr.io/developing-applications/building-blocks/bindings/howto-triggers/  

