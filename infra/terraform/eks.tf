
resource "aws_eks_node_group" "eks_worker_nodes" {
  cluster_name    = aws_eks_cluster.eks.name
  instance_types = ["t2.micro"]
  node_group_name = "weather-eks-worker-nodes"
  node_role_arn   = aws_iam_role.eks_worker_node_group_role.arn
  subnet_ids      = aws_subnet.eks_subnets[*].id

  scaling_config {
    desired_size = 3
    max_size     = 4
    min_size     = 1
  }

  update_config {
    max_unavailable = 1
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_node_group_worker_node_policy,
    aws_iam_role_policy_attachment.eks_node_group_cni_policy,
    aws_iam_role_policy_attachment.eks_node_group_ecr_policy,
    aws_iam_role_policy_attachment.eks_loadBalancing_policy,
    aws_iam_role_policy_attachment.eks_networking_policy,
  ]
}

resource "aws_eks_cluster" "eks" {
  name = "weather"

  access_config {
    authentication_mode = "API"
  }

  bootstrap_self_managed_addons = false

  compute_config {
    enabled       = true
    node_pools    = ["general-purpose"]
    node_role_arn = aws_iam_role.eks_worker_node_group_role.arn
  }

  kubernetes_network_config {
    elastic_load_balancing {
      enabled = true
    }
  }

  storage_config {
    block_storage {
      enabled = true
    }
  }

  role_arn = aws_iam_role.eks_role.arn

  vpc_config {
    subnet_ids = [ for subnet in aws_subnet.eks_subnets : subnet.id ]
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_policy,
  ]
}

