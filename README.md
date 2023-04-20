# upload_s3_cli

## Installation

```
git clone https://github.com/bulv1ne/upload_s3_cli.git
cd upload_s3_cli
poetry install
```

## Usage

As the user with permissions to S3:

```
export AWS_PROFILE=my-profile # Only needed if you're using different profiles
poetry run python -m upload_s3_cli.generate_config --expires-in 3600 --s3-path s3://bucket/path/to/folder --config-out config.json
```

Send the config.json file to the uploading user

As the uploading user:

```
poetry run python -m upload_s3_cli.upload_files --config config.json path/with/files
```
