terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.32.1"
    }
  }

  backend "s3" {
    bucket = "statefile-bucket-terraform1232"
    key    = "terraform.tfstate"
    region = "ap-south-1"
  }
}
