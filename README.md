# Hadoop-MapReduce-App
14848 Cloud Infra hw4


## Setup Steps
1. Create a Dataproc cluster, and upload the temperature folder.

2. List all GCP buckets with the command ``gsutil ls`` and copy the id for current bucket. 
    ![alt text](images/list_bucket.png?raw=true "list buckets")


3. List the contents in the current GCP bucket with command ``gsutil ls gs://dataproc-temp-us-central1-105135044036-xgjwg8ut/1a8efd22-e72b-41ed-9867-aa9997ce5955/``. Make sure it 
contains the temperature folder. 
    ![alt text](images/list_gcp_bucket_content.png?raw=true "list gcp bucket")


4. Copy from GCP bucket to local cluster with command ``gsutil cp -r gs://dataproc-staging-us-central1-105135044036-jlvf54fr/temperature/ .``.
    ![alt text](images/copy_to_local_cluster.png?raw=true "copy to local cluster")


5. Move data files from local cluster to HDFS with command ``hadoop fs -put data/ /``. 
    ![alt text](images/list_hdfs.png?raw=true "list hdfs")


6. Perform mapreduce with command: 
    ```
    hadoop jar /usr/lib/hadoop/hadoop-streaming.jar \
    -files temperature_mapper.py,temperature_reducer.py \
    -input /data/* \
    -output /temperatureOutputFolder \
    -mapper 'python temperature_mapper.py' \
    -combiner 'python temperature_reducer.py' \
    -reducer 'python temperature_reducer.py'
    ```
    The terminal output looks like the following:
    ![alt text](images/map_reduce_output.png?raw=true "mapreduce output")

7. Check the output folder with command ``hadoop fs -ls /temperatureOutputFolder``. The folder should contain result files, one from each reducer.
    ![alt text](images/list_mapreduce_results.png?raw=true "list mapreduce results")


8. Merge all result into 1 file called `maxTempResult` using command ``hadoop fs -getmerge /temperatureOutputFolder maxTempResult``.


9. Copy the result file from local cluster to GCP bucket with command ``gsutil cp maxTempResult gs://dataproc-staging-us-central1-105135044036-jlvf54fr/temperature/``.
    ![alt text](images/copy_result_to_bucket.png?raw=true "copy result to bucket")


10. Download the result file from the console.
    ![alt text](images/console_output.png?raw=true "console output")
