# Gitops with flux deployments

a simple microservice example with two services sitting in the same github repository

# What Is Flux CD?

Flux is a set of continuous and progressive delivery solutions for Kubernetes, and they are open and extensible. We can find out more from the official [website](https://fluxcd.io/)

# Our Example

In this example we will be deploying a simple web app broken into two microservices

- A single-sign-on / user app
- a shop application

Users can Sign up, Create a shop and add, update and destroy Items in their shop. other users can view the items in the shop (feel free to extend the shop micro service to have other interesting functionalities like a cart and checkout system)

to keep things simple, I have left both microservice inside the same repository but properly structured in the `Services/` directory

# prerequisite

as a prerequisite the minimal setup you would need to follow this example is `docker-desktop` with your `Kubernetes enabled` and a `Github account`

you also should be familliar [kubernetes concepts](https://kubernetes.io/docs/concepts/) and how it works

install docker desktop [here](https://docs.docker.com/desktop/) to enable kubernetes, open docker desktop click on the settings icon, on the menu that shows up to the left of your screen, click on kubernetes, click the checkbox that reads `Enable Kubernetes` and apply changes.

# How Flux works

All we are simply doing with flux is making github our single source of truth for the desired state of our kubernetes deployment per unit time.

all we need is to inform Flux of this source of truth (repository) and create configuration files that tell FLux where it can find the github repository holding all the manifest files it needs to deploy our application on Kubernetes.

By following Gitops principle we no longer need to worry about deploying/manage our apps sepeartely, for example if you have two github repositories holding say, your backend code and frontend code you can monitor changes to these repositories from one place and have your deployments automatically updated on kubernetes everytime you make a change to any of your repositories connected to flux.

There are just three major steps:

1. use the flux bootstrap command to generate the repository that will serve as your single source of truth

2. use flux create command to create a source object (The repository holding the code you intend to deploy)

3. use flux create command to create a kustomization (could also be a helm release) object specifying the path in your code/application source repo flux can find the yaml manifests it will need to make a deployment on your behalf

and it's as simple as that!

Kindly note that the above steps only describe a high level detail of what you do with flux. in the next section we will discuss the deployment process in more details

it's important to note that I have setup a CI pipeline in this repo to build and push my application images to to docker. and to do this I had to add my docker username and access token as github secrets (Just Incase you would want to fork the repository and create your own version or extend the code)

# Let's Deploy! :rocket:

in your terminal (or K8s cluster shell)

<b>Step 1</b>:
<br/>

Export your github personal access token:

linux users:

```bash
export GITHUB_TOKEN=<my-token>

```

Windows Users:

```ps
$env:GITHUB_TOKEN=<my-token>
```

<b>Step 2</b>:
<br/>

Run the flux bootstrap command:

```bash
flux bootstrap github --owner=<user> --repository=<repository name> --path=./clusters/my-cluster --private=false --personal=true
```

here we are making our repository public to keep things simple. the repository flag would hold the name of the repo we want flux to create on our behalf on github while the owner flag would hold our github user name (you can also pass a github organization name your access token has appropriate permissions in.) see [docs](https://fluxcd.io/docs/cmd/flux_bootstrap_github/) for more details

<b>Step 3</b>:
<br/>

Step two creates a repository on your behalf on your github account, we can now clone the repository:

```bash
git clone git clone https://github.com/<user>/<repository>.git

cd <repository>

```

<b> Step 4 </b>
<br/>

create a source object with flux create commmand, informing flux of a source repository you would want it to monitor

```bash
flux create source git django-flux-demo --url=https://github.com/JesuFemi-O/flux-django --branch=main --interval=30s --export > ./clusters/my-cluster/django-flux-demo-source.yaml
```

here we are telling flux to the said repositry and this command creates a manifest which we want to be stored in the specified path as seen in the command

<b> Step 5 </b>
<br/>

since there are two services sitting on the same github repository, we do not need to create multiple sources. we just need a single source and two flux deployment manifests - one for each microservice. let's create a kustomization manifest for the auth service:

```bash
flux create kustomization django-flux-auth --source=django-flux-demo --path=".services/auth_service/kustomize" --prune=true --validation=client --interval=5m --export > ./clusters/my-cluster/django-flux-auth-kustomization.yaml

```

in the above command the k8s manifests need to deploy our auth service is specified in the path

<b> Step 6 </b>
<br/>

Create a kustomization manifest for the shop service:

```bash
flux create kustomization django-flux-shop --source=django-flux-demo --path=".services/shop_service/kustomize" --prune=true --validation=client --interval=5m --export > ./clusters/my-cluster/django-flux-shop-kustomization.yaml

```

<b> Step 7 </b>
<br/>

commit changes and push them to your github repo:

```bash
git add -A && git commit -m "Add deployment source and kustomization manifests"
git push
```

<b> Step 8 </b>
<br/>

Flux would instantly Detect changes in the github repo we created in step 2 and would immediately try to reconcile it your K8s cluster current state with the updated desired state defined in your manifest files

we can wathc the deployment by running:

```bash
flux get kustomizations --watch
```

<b> Step 9 </b>
<br/>

once the deployment are susccessful we can access them on our node IP. If you used docker desktopo you can access it on local host as follows:

- Auth Service - localhost:30001

- Shop Service - localhost: 30002

Feel free to deploy an api gateway that allows you route requests to either of these services from a single endpoint!

# Trouble shooting image update sync

incase you run into silent errors where flux reconciles with changes in your codebase but fails to update deployment image on your cluster be sure to:

- Check that the variable you are using to define the image updates in kustomization.yaml is the same variable you are using to reference the latest image in your deployment.yaml file. in the example we use `IMAGE_PLACEHOLDER` in both deployment.yaml and kustomization.yaml files to make it very obvious.

if images are not being pulled correctly

- check to see that the value of IMAGE_PLACEHOLDER in your CI workflow manifest points to a very specific container repo. for exmaple, `django-flux-auth:${github.sha}` did not seem to work at first, but on changing the image name to `jayefee/django-flux-auth:${github.sha}`. deployment updates began to work fine without image pulling errors.

# Just Here for the MicroServices?

You can run the services on your machine with docker:

- Clone the repository

```bash
git clone https://github.com/JesuFemi-O/flux-django.git
cd flux-django
```

- cd to the services folder and run the auth service:

```bash
cd `services/auth_service`
```

build the image and spind up a container

```bash
# build image
docker build -t flux-django-auth .

# run container
docker run -n flux-django-auth-container -p 8000:8000 flux-django-auth
```

- in a new terminal cd to the `services/shop_service` directory and build and run the shop service

```bash
# build image
docker build -t flux-django-shop .

# run container
docker run -n flux-django-shop-container -p 8001:8001 flux-django-shop
```

you can now login on the auth service, copy your token and use it to authorize actions on the Shop service via the swagger UI
