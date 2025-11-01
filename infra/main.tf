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
          "dynamodb:UpdateItem",
          "dynamodb:Scan"
        ]
        Resource = [
          "arn:aws:dynamodb:*:*:table/leaderboard-table",
          "arn:aws:dynamodb:*:*:table/leaderboard-snapshots"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Resource = [
          "arn:aws:s3:::leaderboard-snapshots",
          "arn:aws:s3:::leaderboard-snapshots/*"
        ]
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
resource "aws_lambda_function" "populate_player_table" {
  function_name = "populate_players_in_leaderboard_table"

  # Path to your code package (zip file)
  filename         = "../IngestorV1.zip"
  source_code_hash = filebase64sha256("../IngestorV1.zip")

  # Runtime + handler
  runtime = "python3.13"
  handler = "chess_leaderboard.services.leaderboard.store_players_upload_snapshot"

  role = aws_iam_role.lambda_exec.arn

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
  arn       = aws_lambda_function.populate_player_table.arn
}

# --------------------------
# Permission for EventBridge → Lambda
# --------------------------
resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.populate_player_table.function_name
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

# --------------------------
# Defining the lambda function to retrieve the API data
# --------------------------
resource "aws_lambda_function" "get_snapshot" {
  function_name = "get-snapshot"
  handler       = "chess_leaderboard.services.reader.get_snapshot"
  runtime       = "python3.12"
  role          = aws_iam_role.lambda_exec.arn
  filename         = "../ReaderV3.zip"
  source_code_hash = filebase64sha256("../ReaderV3.zip")
  timeout = 480
}

# --------------------------
# Declaring the resource for the API gateway will only make the API container
# --------------------------
resource "aws_apigatewayv2_api" "snapshot_api" {
  name          = "snapshot-api"
  protocol_type = "HTTP"
}

# --------------------------
# Ties the gateway to the lambda fumnction that actually handles the logic
# --------------------------
resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id                 = aws_apigatewayv2_api.snapshot_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.get_snapshot.invoke_arn
  payload_format_version = "2.0"
}

# --------------------------
# Defines the HTTP route and attaches it to the integration that ties lambda to the endpoint
# --------------------------
resource "aws_apigatewayv2_route" "get_snapshot_route" {
  api_id    = aws_apigatewayv2_api.snapshot_api.id
  route_key = "GET /snapshot"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

# --------------------------
# Gives permission to my route to make calls to lambda
# --------------------------
resource "aws_lambda_permission" "apigw_invoke" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.get_snapshot.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.snapshot_api.execution_arn}/*/*"
}

resource "aws_apigatewayv2_stage" "snapshot_stage" {
  api_id      = aws_apigatewayv2_api.snapshot_api.id
  name        = "$default"
  auto_deploy = true
}

