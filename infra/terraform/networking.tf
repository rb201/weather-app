data "aws_availability_zones" "az_avail" {
  state = "available"
}

resource "aws_vpc" "eks_vpc" {
  cidr_block       = "10.0.0.0/16"

  tags = {
    Name = var.project_name_prefix
  }
}


resource "aws_subnet" "eks_subnets" {
  count = length(data.aws_availability_zones.az_avail.names)

  availability_zone = data.aws_availability_zones.az_avail.names[count.index]
  cidr_block = "10.0.${count.index}.0/24"
  vpc_id     = aws_vpc.eks_vpc.id

  tags = {
    Name = var.project_name_prefix
  }
}
