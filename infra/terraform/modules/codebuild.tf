resource "aws_codebuild_project" "codebuild_project" {
  name          = var.project_name
  description   = var.project_desc
  build_timeout = 5
  service_role  = var.codebuild_role

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type = "BUILD_GENERAL1_SMALL"
    image        = "aws/codebuild/amazonlinux2-x86_64-standard:5.0"
    type         = "LINUX_CONTAINER"

    dynamic "environment_variable" {
        for_each = var.project_env_vars

        content {
            name = environment_variable.key
            value = environment_variable.value
        }
    }
  }

  logs_config {
    cloudwatch_logs {
      group_name  = "weather-app"
      status = "ENABLED"
      stream_name = var.project_name
    }
  }

  source {
    buildspec = var.buildspec_file
    type      = "CODEPIPELINE"
  }

  tags = {
    Name = "jrzyproj"
  }
}
