provider "null" {}

# Declare the variables
variable "render_api_key" {
  description = "The API key for Render"
  type        = string
  sensitive   = true
}

variable "django_secret_key" {
  description = "The Django Secret Key for the project"
  type        = string
  sensitive   = true
}

variable "database_url" {
  description = "The database URL for the project"
  type        = string
  sensitive   = true
}

# Create Render service using curl in local-exec provisioner
resource "null_resource" "create_render_service" {
  provisioner "local-exec" {
    command = <<EOT
      curl -X POST https://api.render.com/v1/services \
      -H "Authorization: Bearer ${var.render_api_key}" \
      -H "Content-Type: application/json" \
      -d '{
        "serviceName": "clientorderapp",
        "environment": "production",
        "platform": "python",
        "buildCommand": "pipenv install --dev && python manage.py migrate",
        "startCommand": "pipenv run python manage.py runserver",
        "branch": "main",
        "repo": "https://github.com/andrewindeche/clientorderservice.git",
        "plan": "free",
        "autoDeploy": true,
        "healthCheck": {
          "path": "/health",
          "intervalSeconds": 30,
          "timeoutSeconds": 5
        },
        "envVars": [
          {"key": "DJANGO_SECRET_KEY", "value": "${var.django_secret_key}"},
          {"key": "DATABASE_URL", "value": "${var.database_url}"}
        ]
      }'
    EOT
  }
}
