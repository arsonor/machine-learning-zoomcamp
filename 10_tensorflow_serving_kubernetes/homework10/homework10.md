## Homework

In this homework, we'll deploy the Bank Marketing model from the homework 5.
We already have a docker image for this model - we'll use it for 
deploying the model to Kubernetes.


## Building the image

Clone the course repo if you haven't:

```
git clone https://github.com/DataTalksClub/machine-learning-zoomcamp.git
```

Go to the `course-zoomcamp/cohorts/2024/05-deployment/homework` folder and 
execute the following:


```bash
docker build -t zoomcamp-model:3.11.5-hw10 .
```

> **Note:** If you have troubles building the image, you can 
> use the image we built and published to docker hub:
> `docker pull svizor/zoomcamp-model:3.11.5-hw10`


## Question 1

Run it to test that it's working locally:

```bash
docker run -it --rm -p 9696:9696 zoomcamp-model:3.11.5-hw10
```

And in another terminal, execute `q6_test.py` file:

```bash
python q6_test.py
```

You should see this:

```python
{'has_subscribed': True, 'has_subscribed_probability': <value>}
```

Here `<value>` is the probability of getting a subscription. You need to choose the right one.

* 0.287
* 0.530
* **0.757**
* 0.960

Now you can stop the container running in Docker.


## Installing `kubectl` and `kind`

You need to install:

* `kubectl` - https://kubernetes.io/docs/tasks/tools/ (you might already have it - check before installing)
* `kind` - https://kind.sigs.k8s.io/docs/user/quick-start/


## Question 2

What's the version of `kind` that you have? 

Use `kind --version` to find out: `kind version 0.25.0`


## Creating a cluster

Now let's create a cluster with `kind`:

```bash
kind create cluster
```

And check with `kubectl` that it was successfully created:

```bash
kubectl cluster-info
```
Kubernetes control plane is running at https://127.0.0.1:39925  
CoreDNS is running at https://127.0.0.1:39925/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.

## Question 3

What's the smallest deployable computing unit that we can create and manage 
in Kubernetes (`kind` in our case)?

* Node
* **Pod**
* Deployment
* Service


## Question 4

Now let's test if everything works. Use `kubectl` to get the list of running services.

`kubectl get service`

NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   3m10s

What's the `Type` of the service that is already running there?

* NodePort
* **ClusterIP**
* ExternalName
* LoadBalancer


## Question 5

To be able to use the docker image we previously created (`zoomcamp-model:3.11.5-hw10`),
we need to register it with `kind`.

What's the command we need to run for that?

* `kind create cluster`
* `kind build node-image`
* **`kind load docker-image`**
* `kubectl apply`


## Question 6

Now let's create a deployment config (e.g. `deployment.yaml`):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: subscription
spec:
  selector:
    matchLabels:
      app: subscription
  replicas: 1
  template:
    metadata:
      labels:
        app: subscription
    spec:
      containers:
      - name: subscription
        image: <Image>
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"            
          limits:
            memory: <Memory>
            cpu: <CPU>
        ports:
        - containerPort: <Port>
```

Replace `<Image>`, `<Memory>`, `<CPU>`, `<Port>` with the correct values.

What is the value for `<Port>`? `9696`

Apply this deployment using the appropriate command and get a list of running Pods. 
You can see one running Pod.

`kubectl apply -f deployment.yaml`

`kubectl get pod`

NAME                            READY   STATUS    RESTARTS   AGE
subscription-544b4f9664-mmcl5   1/1     Running   0          30s

## Question 7

Let's create a service for this deployment (`service.yaml`):

```yaml
apiVersion: v1
kind: Service
metadata:
  name: <Service name>
spec:
  type: LoadBalancer
  selector:
    app: <???>
  ports:
  - port: 80
    targetPort: <PORT>
```

Fill it in. What do we need to write instead of `<???>`? `subscription`

Apply this config file: `kubectl apply -f service.yaml`

NAME           TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
kubernetes     ClusterIP      10.96.0.1      <none>        443/TCP        23m
subscription   LoadBalancer   10.96.207.60   <pending>     80:30480/TCP   111s


## Testing the service

We can test our service locally by forwarding the port 9696 on our computer 
to the port 80 on the service:

```bash
kubectl port-forward service/subscription 9696:80
```

Run `q6_test.py` (from the homework 5) once again to verify that everything is working. 
You should get the same result as in Question 1.


## Autoscaling

Now we're going to use a [HorizontalPodAutoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/) 
(HPA for short) that automatically updates a workload resource (such as our deployment), 
with the aim of automatically scaling the workload to match demand.

Use the following command to create the HPA:

```bash
kubectl autoscale deployment subscription --name subscription-hpa --cpu-percent=20 --min=1 --max=3
```

You can check the current status of the new HPA by running:

```bash
kubectl get hpa
```

The output should be similar to the next:

```bash
NAME               REFERENCE                 TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
subscription-hpa   Deployment/subscription   1%/20%    1         3         1          27s
```

`TARGET` column shows the average CPU consumption across all the Pods controlled by the corresponding deployment.
Current CPU consumption is about 0% as there are no clients sending requests to the server.
> 
>Note: In case the HPA instance doesn't run properly, try to install the latest Metrics Server release 
> from the `components.yaml` manifest:
> ```bash
> kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
>```


## Increase the load

Let's see how the autoscaler reacts to increasing the load. To do this, we can slightly modify the existing
`q6_test.py` script by putting the operator that sends the request to the subscription service into a loop.

```python
while True:
    sleep(0.1)
    response = requests.post(url, json=client).json()
    print(response)
```

Now you can run this script.


## Question 8 (optional)

Run `kubectl get hpa subscription-hpa --watch` command to monitor how the autoscaler performs. 
Within a minute or so, you should see the higher CPU load; and then - more replicas. 
What was the maximum amount of the replicas during this test?


* **1**
* 2
* 3
* 4

> Note: It may take a few minutes to stabilize the number of replicas. Since the amount of load is not controlled 
> in any way it may happen that the final number of replicas will differ from initial.
