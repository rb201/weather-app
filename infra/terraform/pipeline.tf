##########
# SOURCE #
##########

resource "aws_codestarconnections_connection" "github" {
  name          = "github"
  provider_type = "GitHub"
}

#############
# CODEBUILD #
#############

resource "aws_codebuild_project" "backend_sc" {
  name          = "weather-backend-static-check"
  description   = "Static analysis for backend"
  build_timeout = 5
  service_role  = aws_iam_role.codebuild_role.arn

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type = "BUILD_GENERAL1_SMALL"
    image        = "aws/codebuild/amazonlinux2-x86_64-standard:4.0"
    type         = "LINUX_CONTAINER"
  }

  logs_config {
    cloudwatch_logs {
      group_name  = "weather-app"
      stream_name = "backend-static-checks"
    }
  }

  source {
    buildspec = "infra/terraform/buildspecs/backend-static-check.yml"
    type      = "CODEPIPELINE"
  }

  tags = {
    Name = "jrzyproj"
  }
}

############
# PIPELINE #
############
resource "aws_codepipeline" "weather_pipeline" {
  artifact_store {
    location = aws_s3_bucket.codepipeline_bucket.bucket
    type     = "S3"
  }
  name     = "weather_pipeline"
  role_arn = aws_iam_role.pipeline_role.arn

  stage {
    name = "Source"

    action {
      category         = "Source"
      name             = "Source"
      owner            = "AWS"
      output_artifacts = ["source_output"]
      provider         = "CodeStarSourceConnection"
      version          = "1"

      configuration = {
        BranchName       = "development"
        ConnectionArn    = aws_codestarconnections_connection.github.arn
        FullRepositoryId = "rb201/weather-app"
      }
    }
  }

  stage {
    name = "Build"

    action {
      category        = "Build"
      input_artifacts = ["source_output"]
      name            = "Build"
      owner           = "AWS"
      provider        = "CodeBuild"
      version         = "1"

      configuration = {
        ProjectName = aws_codebuild_project.backend_sc.name
      }
    }
  }
}

######
# S3 #
######

resource "aws_s3_bucket" "codepipeline_bucket" {
  bucket = "weather-codepipeline"
}


#######
# IAM #
#######

data "aws_iam_policy_document" "codepipeline_assume_role" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["codepipeline.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy_document" "codebuild_assume_role" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["codebuild.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy_document" "codepipeline_policy" {
  statement {
    effect = "Allow"
    actions = [
      "codebuild:StartBuild",
      "codecommit:GetBranch",
    ]
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    actions = [
      "codeconnections:UseConnection",
    ]
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    actions = [
      "s3:GetObjects",
    ]
    resources = [aws_s3_bucket.codepipeline_bucket.arn]
  }
}

resource "aws_iam_policy" "codepipeline_policy" {
  name        = "codepipeline-policy"
  description = "Allowed permissions for CodePipeline"
  policy      = data.aws_iam_policy_document.codepipeline_policy.json
}

resource "aws_iam_role" "pipeline_role" {
  name               = "weather-pipeline-role"
  assume_role_policy = data.aws_iam_policy_document.codepipeline_assume_role.json
}

resource "aws_iam_role" "codebuild_role" {
  name               = "weather-codebuild-role"
  assume_role_policy = data.aws_iam_policy_document.codebuild_assume_role.json
}

resource "aws_iam_role_policy_attachment" "codepipeline_role_attachment" {
  role       = aws_iam_role.pipeline_role.name
  policy_arn = aws_iam_policy.codepipeline_policy.arn
}