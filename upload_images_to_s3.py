import boto3
import os

# Let's use Amazon S3
s3 = boto3.resource('s3')

# Upload a new file
def uploadfile(bucket, upload_file_full_path, local_filepath):
    data = open(local_filepath, 'rb')
    print("Uploading " + local_filepath + '        TO: ' + upload_file_full_path)
    s3.Bucket(bucket).put_object(Key=upload_file_full_path, Body=data)

def uploadfolder(bucket='dark-cloud-bucket2', folder_to_upload='./pictures', destination_folder_path=''):
    directory = os.fsencode(folder_to_upload)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        filepath = folder_to_upload + '/' + filename
        
        if destination_folder_path != '':
                upload_file_full_path = destination_folder_path + '/' + filename
        else:
                upload_file_full_path = filename
        uploadfile( bucket=bucket, upload_file_full_path=upload_file_full_path, local_filepath=filepath)
 
def file_exists_in_s3(bucket, file_path):
        bucket = s3.Bucket(bucket)
        key = file_path
        objs = list(bucket.objects.filter(Prefix=key))
        if len(objs) > 0 and objs[0].key == key:
                return True
        else:
                return False

if __name__ == "__main__":
        uploadfolder(destination_folder_path='new_images')