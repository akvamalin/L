provider "aws" {
    region = "eu-central-1"
}

resource "aws_s3_bucket" "s3-lambdas-state" {
    bucket = "lambdas-state"
    acl = "private"
}

resource "aws_dynamodb_table" "dynamo-lambdas-state-lock" {
    name = "lambdas-state-lock"
    hash_key = "LockID"

    attribute {
        name = "LockID"
        type = "S"
    }

    read_capacity = 1
    write_capacity = 1
}