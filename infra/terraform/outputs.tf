
output "codebuild_role" {
    description = "Arn of role used for CodeBuild"
    value = aws_iam_role.codebuild_role.arn
}

output "pipeline_role" {
    description = "Role use for CodePipeline"
  value = aws_iam_role.pipeline_role.arn
}
