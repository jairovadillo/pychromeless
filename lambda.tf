//
//
// BIG NOQA
//
//

resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambdium"

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

resource "aws_lambda_function" "lambdium" {
  filename = "lambda_function.zip"
  function_name = "pychromeless"
  role = "${aws_iam_role.iam_for_lambda.arn}"
  handler = "lambda_function.lambda_handler"
  runtime = "python3.6"
  timeout = 120
  memory_size = 768

  // Total size of enviornment variables must not exceed 4KB.
  // http://docs.aws.amazon.com/lambda/latest/dg/limits.html
  environment {
    variables = {
      PATH = "/var/lang/bin:/usr/local/bin:/usr/bin/:/bin:/var/task/bin"
    }
  }
}
