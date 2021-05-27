### Cloudwatch Events ###
# Event rule: Runs at 6am during working days
resource "aws_cloudwatch_event_rule" "start_instances_event_rule" {
  name = "start_instances_event_rule"
  description = "Starts stopped EC2 instances"
  schedule_expression = "cron(0 6 ? * MON-FRI *)"
  depends_on = [ aws_lambda_function.ec2_start_lambda ]
}

# Runs at 6:30AM during working days
resource "aws_cloudwatch_event_rule" "asg_setup_event_rule" {
  name = "asg_setup_event_rule"
  description = "Sets autoscaling groups"
  schedule_expression = "cron(0 6:30 ? * MON-FRI *)"
  depends_on = [ aws_lambda_function.asg_setup_lambda ]
}

# Runs at 9pm during working days
resource "aws_cloudwatch_event_rule" "stop_instances_event_rule" {
  name = "stop_instances_event_rule"
  description = "Stops running EC2 instances"
  schedule_expression = "cron(0 21 ? * MON-FRI *)"
  depends_on = [ aws_lambda_function.ec2_stop_lambda ]
}

# Event target: Associates a rule with a function to run
resource "aws_cloudwatch_event_target" "start_instances_event_target" {
  target_id = "start_instances_lambda_target"
  rule = aws_cloudwatch_event_rule.start_instances_event_rule.name
  arn = aws_lambda_function.ec2_start_lambda.arn
}

resource "aws_cloudwatch_event_target" "stop_instances_event_target" {
  target_id = "stop_instances_lambda_target"
  rule = aws_cloudwatch_event_rule.stop_instances_event_rule.name
  arn = aws_lambda_function.ec2_stop_lambda.arn
}

resource "aws_cloudwatch_event_target" "asg_setup_event_target" {
  target_id = "asg_setup_lambda_target"
  rule = aws_cloudwatch_event_rule.asg_setup_event_rule.name
  arn = aws_lambda_function.asg_setup_lambda.arn
}

# AWS Lambda Permissions: Allow CloudWatch to execute the Lambda Functions
resource "aws_lambda_permission" "allow_cloudwatch_to_call_start" {
  statement_id = "AllowExecutionFromCloudWatch"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ec2_start_lambda.function_name
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.start_instances_event_rule.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_stop" {
  statement_id = "AllowExecutionFromCloudWatch"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ec2_stop_lambda.function_name
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.stop_instances_event_rule.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_setup" {
  statement_id = "AllowExecutionFromCloudWatch"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.asg_setup_lambda.function_name
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.asg_setup_event_rule.arn
}