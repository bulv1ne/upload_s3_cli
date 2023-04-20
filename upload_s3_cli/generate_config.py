import argparse
import json

import boto3
from botocore.config import Config

config = Config(signature_version="s3v4")


def s3_path_parser(value):
    if not value.startswith("s3://"):
        raise ValueError("The s3 path must start with s3://")
    value = value[5:]
    if value.endswith("/"):
        value = value[:-1]
    return value.split("/", 1)


def main():
    parser = argparse.ArgumentParser("upload_s3_cli")
    parser.add_argument("--expires-in", type=int, required=True)
    parser.add_argument("--s3-path", type=s3_path_parser, required=True)
    parser.add_argument("--config-out", type=argparse.FileType("w"), required=True)
    args = parser.parse_args()

    s3 = boto3.client("s3", config=config)
    bucket, prefix = args.s3_path
    response = s3.generate_presigned_post(
        bucket,
        prefix + "/${filename}",
        ExpiresIn=args.expires_in,
    )
    json.dump(response, args.config_out, indent=2)


if __name__ == "__main__":
    main()
