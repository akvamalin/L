provider "aws" {
    region = "eu-central-1"
}

terraform {
    backend "s3" {
        encrypt = true
        bucket = "lambdas-state"
        dynamodb_table = "lambdas-state-lock"
        key = "l-state",
        region = "eu-central-1"
    }
}

resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_lambda_function" "pymail-lambda" {
    filename = "../pymail/package.zip"
    function_name = "pymail_lambda"
    handler = "src/main.handler"
    runtime = "python3.7"
    source_code_hash = "${filebase64sha256("../pymail/package.zip")}"
    role = "${aws_iam_role.iam_for_lambda.arn}"
}

resource "aws_cloudwatch_event_rule" "hour-rate" {
    name = "hour-rate"
    schedule_expression = "rate(1 hour)"
}

resource "aws_cloudwatch_event_target" "pymail_-cron" {
    rule = "${aws_cloudwatch_event_rule.hour-rate.name}"
    target_id = "${aws_lambda_function.pymail-lambda.id}"
    arn = "${aws_lambda_function.pymail-lambda.arn}"
}

resource "aws_lambda_permission" "cloudwatch-trigger-pymail" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = "${aws_lambda_function.pymail-lambda.function_name}"
    principal = "events.amazonaws.com"
    source_arn = "${aws_cloudwatch_event_rule.hour-rate.arn}"
}