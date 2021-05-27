### IAM Role and Policy ###
# Allows Lambda function to describe, stop and start EC2 instances
resource "aws_iam_role" "ec2_start_stop" {
  name = "ec2_start_stop"
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

data "aws_iam_policy_document" "ec2_start_stop" {
  statement {
      actions = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ]
      resources = [ "arn:aws:logs:*:*:*" ]
  }
  statement {
      actions = [
        "ec2:Describe*",
        "ec2:Stop*",
        "ec2:Start*"
      ]
      resources = [ "*" ]
  }
  statement {
      actions = [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject"
      ]
      resources = [ "arn:aws:s3:::atrium-ec2-scheduler-asg-data/*" ]
  }
  statement {
      actions = [
        "autoscaling:UpdateAutoScalingGroup",
        "autoscaling:DescribeAutoScalingGroups",
        "autoscaling:DescribeAutoScalingInstances"
      ]
      resources = [ "*" ]
  }
}

resource "aws_iam_policy" "ec2_start_stop" {
  name = "ec2_access"
  path = "/"
  policy = data.aws_iam_policy_document.ec2_start_stop.json
}

resource "aws_iam_role_policy_attachment" "ec2_access" {
  role       = aws_iam_role.ec2_start_stop.name
  policy_arn = aws_iam_policy.ec2_start_stop.arn
}