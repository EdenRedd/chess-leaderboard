# --------------------------
# IAM Role for Lambda
# --------------------------
resource "aws_iam_role" "lambda_exec" {
  name = "populate_dynamo_lambda"

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
# --------------------------
# Custom resource definition to allow putting into our dynamodb table
# --------------------------
resource "aws_iam_role_policy" "lambda_dynamo_policy" {
  name = "lambda_dynamo_policy"
  role = aws_iam_role.lambda_exec.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem",
          "dynamodb:UpdateItem"
        ]
        Resource = "arn:aws:dynamodb:*:*:table/leaderboard-table"
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}


# Attach policies so Lambda can log to CloudWatch
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# --------------------------
# Lambda Function points to the leaderboard function that handles storing
# the incoming information from the Chess API
# --------------------------
resource "aws_lambda_function" "my_lambda" {
  function_name = "my_lambda_function"

  # Path to your code package (zip file)
  filename         = "../chess_leaderboard_lambdaV7.zip"
  source_code_hash = filebase64sha256("../chess_leaderboard_lambdaV7.zip")

  # Runtime + handler
  runtime = "python3.13"
  handler = "chess_leaderboard.services.leaderboard.lambda_handler"

  role = aws_iam_role.lambda_exec.arn

  # ✅ Set timeout to 8 minutes
  timeout = 480
}

# --------------------------
# EventBridge Rule (Schedule)
# --------------------------
resource "aws_cloudwatch_event_rule" "my_schedule" {
  name                = "my-schedule"
  schedule_expression = "rate(3 minutes)" # 👈 change to your cron/rate
}

# --------------------------
# EventBridge Target definition(Lambda)
# --------------------------
resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.my_schedule.name
  target_id = "my-lambda-target"
  arn       = aws_lambda_function.my_lambda.arn
}

# --------------------------
# Permission for EventBridge → Lambda
# --------------------------
resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.my_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.my_schedule.arn
}

# --------------------------
# Dynamodb table declaration for player and gamemode leaderboard
# --------------------------
resource "aws_dynamodb_table" "leaderboard-table" {
  name           = "leaderboard-table"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "GameModeCountryCode"
  range_key      = "RankAndID"

  attribute {
    name = "GameModeCountryCode"
    type = "S"
  }

  attribute {
    name = "RankAndID"
    type = "S"
  }
}

# --------------------------
# Dynamodb table declaration for snapshots of player leaderboard
# --------------------------
resource "aws_dynamodb_table" "leaderboard-snapshots" {
  name         = "leaderboard-snapshots"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "SnapshotType"
  range_key    = "SnapshotTimestamp"

  attribute {
    name = "SnapshotType"
    type = "S"
  }

  attribute {
    name = "SnapshotTimestamp"
    type = "S"
  }
}



# --------------------------
# s3 bucket for snapshots
# --------------------------
resource "aws_s3_bucket" "leaderboard-snapshots" {
  bucket = "leaderboard-snapshots"
}