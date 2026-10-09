resource "aws_dynamodb_table" "orders" {
  provider = aws.mumbai

  name         = "dr-lab-orders"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "order_id"

  attribute {
    name = "order_id"
    type = "S"
  }

  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"

  replica {
    region_name            = "ap-southeast-1"
    point_in_time_recovery = true
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = {
    Project     = "aws-dr-resilience-lab"
    Environment = "lab"
  }
}
