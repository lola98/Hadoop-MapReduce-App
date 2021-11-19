from google.cloud import storage    
import glob, os

class Upload_Files():
    def upload_to_bucket(files, bucket_name, relative_path):
        storage_client = storage.Client()

        # get the bucket
        new_bucket = storage_client.get_bucket(bucket_name)

        # upload files
        for local_file in glob.glob(files + '**/**'):
            # if is a folder, create a new folder in the bucket
            if not os.path.isfile(local_file):
                Upload_Files.upload_to_bucket(local_file, bucket_name, relative_path + "/" + os.path.basename(local_file))

            # if is a file, upload to bucket
            else:
                remote_path = os.path.join(relative_path, local_file[1 + len(files):])
                print(remote_path)
                blob = new_bucket.blob(remote_path)
                blob.upload_from_filename(local_file)
    