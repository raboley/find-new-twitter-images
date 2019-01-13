import boto3

def get_matching_s3_keys(bucket, prefix='', suffix=''):
    """Returns a list of file paths from a bucket based on matching prefix and suffix
    
    Parameters
    ----------
    bucket : str
        the string representing the bucket name to be queried
    prefix : str, optional
        the prefix each object in the s3 bucket should share, normally folder path
        (the default is '', which means it will return all folder paths)
    suffix : str, optional
        the ending characters required by the query, normally the extension of the file
        (the default is '', which means files of any extension will be returned)
        
    """
    for obj in __get_matching_s3_objects(bucket, prefix, suffix):
        yield obj['Key']

def __get_matching_s3_objects(bucket, prefix='', suffix=''):
    s3 = boto3.client('s3')
    kwargs = {'Bucket': bucket}

    # If the prefix is a single string (not a tuple of strings), we can
    # do the filtering directly in the S3 API.
    if isinstance(prefix, str):  # robustness; basestring is a common superclass of str, unicode and potentially some more string classes
        kwargs['Prefix'] = prefix

    while True:

        # The S3 API response is a large blob of metadata.
        # 'Contents' contains information about the listed objects.
        resp = s3.list_objects_v2(**kwargs)

        try:
            contents = resp['Contents']
        except KeyError:
            return

        for obj in contents:
            key = obj['Key']
            if key.startswith(prefix) and key.endswith(suffix):
                yield obj

        # The S3 API is paginated, returning up to 1000 keys at a time.
        # Pass the continuation token into the next response, until we
        # reach the final page (when this field is missing).
        try:
            kwargs['ContinuationToken'] = resp['NextContinuationToken']
        except KeyError:
            break



if __name__ == '__main__':
   l = get_matching_s3_keys(bucket='dark-cloud-bucket', prefix='__testing/')