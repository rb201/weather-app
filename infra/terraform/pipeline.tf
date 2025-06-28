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
    image        = "aws/codebuild/amazonlinux2-x86_64-standard:5.0"
    type         = "LINUX_CONTAINER"
  }

  logs_config {
    cloudwatch_logs {
      group_name  = "weather-app"
      status = "ENABLED"
      stream_name = "backend-static-checks"
    }
  }

  source {
    buildspec = "infra/terraform/buildspecs/backend-static-checks.yml"
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
      owner            = "ThirdParty"
      output_artifacts = ["source_output"]
      provider         = "GitHub"
      version          = "1"

      configuration = {
        Branch     = "development"
        Owner      = "rb201"
        Repo       = "weather-app"
        OAuthToken = "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"
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
  bucket = "rb-weather-codepipeline"
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

data "aws_iam_policy_document" "codebuild_policy" {
  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "s3:GetObject",
    ]
    resources = ["*"]
  }
}

data "aws_iam_policy_document" "codepipeline_policy" {
  statement {
    effect = "Allow"
    actions = [
      "codebuild:BatchGetBuilds",
      "codebuild:StartBuild",
      "codecommit:GetBranch",
    ]
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
    ]
    resources = ["arn:aws:s3:::rb-weather-codepipeline/*"]
  }
}

resource "aws_iam_policy" "codebuild_policy" {
  name        = "codebuild-policy"
  description = "Allowed permissions for CodeBuild"
  policy      = data.aws_iam_policy_document.codebuild_policy.json
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

resource "aws_iam_role_policy_attachment" "codebuild_role_attachment" {
  role       = aws_iam_role.codebuild_role.name
  policy_arn = aws_iam_policy.codebuild_policy.arn
}