# COVID19 Stats & Data Viz Report

## Requirements

* Docker & Docker Compose
* A working Kubernetes cluster (minikube is a good start)
* A working kubectl connected to the k8 cluster

## Deployment Instructions

1. In a terminal, clone the Barge repo so you can deploy the Ocean core infrastructure locally:

```
git clone https://github.com/oceanprotocol/barge
cd barge
```

2. Update Brizo configuration by updating the OPERATOR_SERVICE_URL env in `start_ocean.sh`:

```
...
export OPERATOR_SERVICE_URL=http://host.docker.internal:8050
...
```

3. Deploy barge:

```
./start_ocean.sh --mongodb --no-commons --purge
```

4. In another terminal, clone the `operator-service` node repo

```
git clone https://github.com/oceanprotocol/operator-service.git
cd operator-service
```
  - Changes on `deploy_on_k8s/postgres-storage.yaml`:
  
  ```
  ...
  hostPath:
    path: {A_LOCAL_PATH_TO_STORE_DATA}
  ...
  ```
  
  - Changes on `deploy_on_k8s/deployment.yaml`:
  
  ```
  ...
  - env:
    - name: ALGO_POD_TIMEOUT
      value: 60 # OR increase it if needed
  ...
  ```
  
5. In another terminal clone the `operator-engine` node repo:

```
git clone https://github.com/oceanprotocol/operator-engine.git
cd operator-engine

```
   -  Changes on `k8s_install/operator.yml`:
   
   ```
   ...
   spec:
      containers:
      - env:
        - name: ACCOUNT_JSON
          value: '{"address":"5eaa67b9f25be46c9d723440fff29bd9ee223693","crypto":{"cipher":"aes-128-ctr","ciphertext":"14d49447771e75c351522c7e18466b03d968a6f31f56dfbb1f055c66a49295c5","cipherparams":{"iv":"fb8b4284497996d18610648f813c1b55"},"kdf":"scrypt","kdfparams":{"dklen":32,"n":262144,"p":1,"r":8,"salt":"c7277c2d194321b2cba0e0d00601f90803e5ed6160c2b51c1dcaf75342e732a4"},"mac":"c07bc1b3319030affc867ef85e9d56cb471c3554066b7542b7f113940112acf1"},"id":"ccca3444-46f0-4574-8cb7-a3c263e7f47d","version":3}'
      - name: ACCOUNT_PASSWORD
        value: 1234abcd
   ...
   ...
      - name: AWS_ACCESS_KEY_ID
          value: somekey # NEED TO PROVIDE THIS
        - name: AWS_SECRET_ACCESS_KEY
          value: some secret # NEED TO PROVIDE THIS
        - name: AWS_REGION
          value: us-east-1 # NEED TO PROVIDE THIS
        - name: AWS_BUCKET_OUTPUT
          value: outputbucket # NEED TO PROVIDE THIS
        - name: AWS_BUCKET_ADMINLOGS
          value: adminbucket # NEED TO PROVIDE THIS
   ...
   ```
   
   - Create a file ` k8s_install/storage-class.yaml`:
   
   ```
   apiVersion: storage.k8s.io/v1
   kind: StorageClass
   metadata:
     name: standard
   provisioner: docker.io/hostpath
   reclaimPolicy: Retain
   ```

**NOTE**: For Storage class config on AWS see this [instructions](https://github.com/oceanprotocol/docs/blob/a83841e4282893d610f53fbe363fd306f506267d/content/setup/ctd.md#storage-class)

6. Create namespaces

```
kubectl create ns ocean-operator
kubectl create ns ocean-compute
```

7. Deploy the `operator-service`:

```
cd deploy_on_k8s/
kubectl config set-context --current --namespace ocean-operator
kubectl create -f postgres-configmap.yaml
kubectl create -f postgres-storage.yaml
kubectl create -f postgres-deployment.yaml
kubectl create -f postgresql-service.yaml
kubectl apply -f deployment.yaml
kubectl apply -f role_binding.yaml
kubectl apply -f service_account.yaml
```

8. Deploy the `operator-engine`:

```
cd k8s_install/
kubectl config set-context --current --namespace ocean-compute
kubectl apply -f sa.yml
kubectl apply -f storage-class.yml
kubectl apply -f binding.yaml
kubectl apply -f operator.yml
kubectl apply -f computejob-crd.yaml
kubectl apply -f workflow-crd.yaml
kubectl create -f ../../operator-service/deploy_on_k8s/postgres-configmap.yaml
```
9. Expose Operator Service

```
kubectl expose deployment operator-api --namespace=ocean-operator --port=8050
```

10. Port forward the `operator-service`:

```
kubectl -n ocean-operator port-forward svc/operator-api 8050
```

8. Initialize Database

```
curl -X POST "http://localhost:8050/api/v1/operator/pgsqlinit" -H  "accept: application/json"
```



## Demo instructions

- [Slides](https://drive.google.com/file/d/1-Kii48UqKx45vk-pmefR-GkbGVEKYN7h/view?usp=sharing)

## Useful commands

```
kubectl -n ocean-compute get pods
kubectl -n ocean-compute logs <>
kubectl get events -n ocean-compute
```
