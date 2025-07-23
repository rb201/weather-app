variable "buildspec_file" {
    description = "The buildspec CodeBuild will use"
    type = string
}

variable "codebuild_role" {
  description = "CodeBuild role"
  type = string
}

variable "project_desc" {
    description = "Description CodeBuild Project"
    type = string
}

variable "project_name" {
    description = "Name of the CodeBuild Project"
    type = string
}

variable "project_env_vars" {
    default = {}
    description = "Environment variables"
    type = map(string)
}
