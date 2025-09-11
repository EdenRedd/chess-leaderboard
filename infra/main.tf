# --------------------------
# 1. IAM Role for Lambda
# --------------------------
resource "aws_iam_role" "lambda_exec" {
  name = "my_lambda_exec_role"

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

# Attach policies so Lambda can log to CloudWatch
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# --------------------------
# 2. Lambda Function
# --------------------------
resource "aws_lambda_function" "my_lambda" {
  function_name = "my_lambda_function"

  # 👇 Fill this in: path to your code package (zip file)
  filename         = "<<< path_to_your_lambda_code.zip >>>"
  source_code_hash = filebase64sha256("<<< path_to_your_lambda_code.zip >>>")

  # 👇 Fill this in: runtime + handler (depends on your language)
  runtime = "<<< e.g., python3.11 or nodejs18.x >>>"
  handler = "<<< e.g., index.handler >>>"

  role = aws_iam_role.lambda_exec.arn
}

# --------------------------
# 3. EventBridge Rule (Schedule)
# --------------------------
resource "aws_cloudwatch_event_rule" "my_schedule" {
  name                = "my-schedule"
  schedule_expression = "rate(5 minutes)" # 👈 change to your cron/rate
}

# --------------------------
# 4. EventBridge Target (Lambda)
# --------------------------
resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.my_schedule.name
  target_id = "my-lambda-target"
  arn       = aws_lambda_function.my_lambda.arn
}

# --------------------------
# 5. Permission for EventBridge → Lambda
# --------------------------
resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.my_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.my_schedule.arn
}
