#TODO: github token as secret

##########
# SOURCE #
##########

resource "aws_codestarconnections_connection" "github" {
  name          = "github"
  provider_type = "GitHub"
}

module "codebuild_backend_static_checks" {
  source = "./modules/"

  buildspec_file = "infra/terraform/buildspecs/backend-static-checks.yml"
  codebuild_role = aws_iam_role.codebuild_role.arn
  project_name = "backend-static-checks"
  project_desc = "Static analysis for backend"
}

module "codebuild_backend_unit_test" {
  source = "./modules/"

  buildspec_file = "infra/terraform/buildspecs/backend-unit-tests.yml"
  codebuild_role = aws_iam_role.codebuild_role.arn
  project_name = "unit-tests"
  project_desc = "Pytest"
}

module "codebuild_backend_image" {
  source = "./modules/"

  buildspec_file = "infra/terraform/buildspecs/backend-build-image.yml"
  codebuild_role = aws_iam_role.codebuild_role.arn
  project_name = "build-image"
  project_desc = "Build, tag, and push image to ECR"

  project_env_vars = {
    "USERNAME" = ""
    "PASSWORD" = ""
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
        OAuthToken = ""
      }
    }
  }

  stage {
    name = "Tests"

    action {
      category        = "Test"
      input_artifacts = ["source_output"]
      name            = "Static_Checks"
      owner           = "AWS"
      provider        = "CodeBuild"
      version         = "1"

      configuration = {
        ProjectName = module.codebuild_backend_static_checks.project_name
      }
    }
  
    action {
      category        = "Test"
      input_artifacts = ["source_output"]
      name            = "Unit_Test"
      owner           = "AWS"
      provider        = "CodeBuild"
      version         = "1"

      configuration = {
        ProjectName = module.codebuild_backend_unit_test.project_name
      }
    }
  }

  stage {
    name = "Build_And_Push_Image"

    action {
      category        = "Build"
      input_artifacts = ["source_output"]
      name            = "Build"
      owner           = "AWS"
      provider        = "CodeBuild"
      version         = "1"

      configuration = {
        ProjectName = module.codebuild_backend_image.project_name
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

resource "aws_ecr_repository" "backend_container_registry" {
  name = "weather-backend"
}

resource "aws_ecr_repository" "frontend_container_registry" {
  name = "weather-frontend"
}