# Project
This project sole purpose is to refresh my skills as enter back into the workforce. I've created an app, but the app was just a means to developing the infrastructure around it. I'm not a software engineer by trade, my core role is devops. I started from what I knew, and thought and researched about what i can do with what I knew, and then finally researching what was possible outside of what i learned. 

Some of the tech choices were are out interest but never was able to use them in the world, CNCF, or just reading recommendations by users online. 

My server is a hp elitedesk 800g5, that already has some homelab stuff I was doing before. Therefore the other big consideration was to work with tech that was lighter in resources. I had to work with what i had

### Backend
The idea was to just get started and not over-think the project. I wasn't interested in leetcode etc; projects seem to be more effective to learn from. Originally, I had wanted to just refresh my Python. So the thought was along the lines of, 'how do i get weather data?'. I have much experience and I could see so many ideas in an instant of what the final should look like, what tech to use etc. - which was initially overwhelming. So I made the effort to break down all ideas into workable pieces and to start simple. I could refactor or optimize later, but mort importantly, I had to get started


##### K3S
I chose k3s as it said to be designed for resource-constrained env. The installation was very simple too.

##### Sqlite
SQLite is my database as requires basically nothing to get started. I had initially considered to move to PostGres after the project gets going, but I decided to stay with it. It is currently mounted via PV/NFS, and i would like to test for performance and itegreity. But I haven't done that yet as of writing this.

##### FastAPI
There are no particular reasons I chose FastAPI other than mostly because of the praise I've read online. I was never intending to make my app public or growing it too much. However, the native `async` support nice as I knew I would need to read from a database



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
I have seen ArgoCD in my past experience, but I hadn't seen GitOps in action beyond a very superficial level. Argo deploys to the prod namespace/env in conjunction with kustomize

##### Prod
![ArgoCD](readme-misc/argocd.png)