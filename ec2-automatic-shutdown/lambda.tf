### AWS Lambda function ###
# AWS Lambda API requires a ZIP file with the execution code
data "archive_file" "start" {
  type        = "zip"
  source_file = "start_instances.py"
  output_path = "start_instances.zip"
}

data "archive_file" "stop" {
  type        = "zip"
  source_file = "stop_instances.py"
  output_path = "stop_instances.zip"
}

data "archive_file" "setup" {
  type        = "zip"
  source_file = "asg_setup.py"
  output_path = "asg_setup.zip"
}

# Lambda defined that runs the Python code with the specified IAM role
resource "aws_lambda_function" "ec2_start_lambda" {
  filename = data.archive_file.start.output_path
  function_name = "start_instances"
  role = aws_iam_role.ec2_start_stop.arn
  handler = "start_instances.lambda_handler"
  runtime = "python2.7"
  timeout = 300
  source_code_hash = data.archive_file.start.output_base64sha256
}

resource "aws_lambda_function" "ec2_stop_lambda" {
  filename = data.archive_file.stop.output_path
  function_name = "stop_instances"
  role = aws_iam_role.ec2_start_stop.arn
  handler = "stop_instances.lambda_handler"
  runtime = "python2.7"
  timeout = 300
  source_code_hash = data.archive_file.stop.output_base64sha256
}

resource "aws_lambda_function" "asg_setup_lambda" {
  filename = data.archive_file.setup.output_path
  function_name = "asg_setup"
  role = aws_iam_role.ec2_start_stop.arn
  handler = "asg_setup.lambda_handler"
  runtime = "python2.7"
  timeout = 300
  source_code_hash = data.archive_file.setup.output_base64sha256
}