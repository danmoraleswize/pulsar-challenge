# Create basic cluster for job execution
gcloud dataproc clusters create cluster-2263 --bucket castle-black-store --region us-east1 --subnet default --zone "" --master-machine-type n1-standard-2 --master-boot-disk-size 15 --num-workers 2 --worker-machine-type n1-standard-2 --worker-boot-disk-size 15 --image-version 1.3-deb9 --project pulsar-dowj-challenge --initialization-actions 'gs://dataproc-initialization-actions/zeppelin/zeppelin.sh'


# Connect to cluster instance using cloud shell, once inside the master open a new browser viewer for the 8080 zeppelin app
gcloud compute ssh \
  --project=pulsar-dowj-challenge \
  --zone=us-east1-b \
  --ssh-flag="-L 8080:localhost:8080" cluster-2263-m
