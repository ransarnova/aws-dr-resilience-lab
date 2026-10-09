module "mumbai" {
  source = "../../modules/regional-api"

  providers = {
    aws = aws.mumbai
  }

  project_name     = "dr-lab-mumbai"
  lambda_zip_path  = data.archive_file.lambda.output_path
  lambda_zip_hash  = data.archive_file.lambda.output_base64sha256
  orders_table_arn = aws_dynamodb_table.orders.arn
}

data "archive_file" "lambda" {
  type        = "zip"
  source_file = "${path.module}/../../../application/lambda/handler.py"
  output_path = "${path.module}/lambda.zip"
}


module "singapore" {
  source = "../../modules/regional-api"

  providers = {
    aws = aws.singapore
  }

  project_name    = "dr-lab-singapore"
  lambda_zip_path = data.archive_file.lambda.output_path
  lambda_zip_hash = data.archive_file.lambda.output_base64sha256

  orders_table_arn = one([
    for replica in aws_dynamodb_table.orders.replica :
    replica.arn
    if replica.region_name == "ap-southeast-1"
  ])
}
