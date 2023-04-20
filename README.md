# upload_s3_cli

## Usage

As the user with permissions to S3:

```
python -m upload_s3_cli.generate_config --expires-in 3600 --s3-path s3://bucket/path/to/folder --config-out config.json
```

Send the config.json file to the uploading user

As the uploading user:

```
python -m upload_s3_cli.upload_files --config config.json path/with/files
```
