# Project
This project sole purpose is to refresh my skills as enter back into the workforce. I've created an app, but the app was just a means to developing the infrastructure around it. I'm not a software engineer by trade, my core role is devops. I started from what I knew, and thought and researched about what i can do with what I knew, and then finally researching what was possible outside of what i learned. 

Some of the tech choices were are out of my own interest but never was able to use them professionally, CNCF, or just reading recommendations by users online. Most important factors for implementing any of the tech: 1) is it simple to use and get started and 2) is it resource efficient (due to my sever capacity)


### Kanban
The idea was to just get started and not over-think the project. I made the effort to break down all ideas into workable pieces and to start simple. I could refactor or optimize later, but mort importantly, I had to get started. I had Vikunja already in my homelab, so I just created a new project there to manage tasks

![Vikunja board](readme-misc/vikunja.png)


### Backend

##### K3S
I chose k3s as it is said to be designed for resource-constrained env. A plus was that Traefik is used by default, which I could leverage without extra config. 

##### Sqlite
SQLite is my database as requires basically nothing to get started. I had initially considered to move to PostGres after the project gets going, but I decided to stay with it. It is currently mounted via PV/NFS, and i would like to test for performance and itegreity. But I haven't done that yet as of writing this.

##### FastAPI
There are no particular reasons I chose FastAPI other than mostly because of the praise I've read online. I was never intending to make my app public or growing it too much. However, the native `async` support is nice as I knew I would need to read from a database



### Frontend
ReactJS was my choice simply becaues i've used it in the past and didn't want to spend much time researching frontend as it's not something I do professionally, although I have for a tiny project


### CI/CD
#### DroneCI
Very light and very simple. There are two pipelines, dev and prod
![DroneCI pipelines](readme-misc/drone-ci.png)

##### Dev
Dev runs on every push. This pipeline runs static anaylsis, unit-test, build images, push them, and deploys using `kubectl rollout ...`. You can see more details in `.drone.yml`


##### Prod
The prod pipeline run on a PR from dev into master. This pipeline simply re-tags the most recent dev images.

#### ArgoCD
Argo deploys to the prod namespace/env in conjunction with kustomize

##### Prod
![ArgoCD](readme-misc/argocd.png)