terraform {
    required_providers {
        aws = {
            source = "hashicorp/aws"
            version = "~> 5.0"
        }
    }
}

provider "aws" {
    region = "us-east-2"
}

# resource "aws_instance" "eks_worder_node" {
#     ami = ""
#     instance_type = "t3.micro"

#     tags = {
#         Name = ""
#     }
# }