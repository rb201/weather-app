resource "aws_eks_node_group" "eks_worker_nodes" {
  cluster_name    = aws_eks_cluster.eks.name
  instance_types = "t2.micro"
  node_group_name = "weather-eks-worker-nodes"
  node_role_arn   = aws_iam_role.eks_worker_node_group_role.arn
  subnet_ids      = ""

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
  ]
}

resource "aws_eks_cluster" "eks" {
  name = "weather"

  access_config {
    authentication_mode = "API"
  }

  role_arn = aws_iam_role.eks_role.arn

  vpc_config {
    subnet_ids = [
        
    ]
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_policy,
  ]
}

