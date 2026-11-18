# Terraform Configuration for Vagabond Road Trip Agent Deployments
provider "google" {
  project = "vagabond-roadtrip"
  region  = "us-central1"
}

resource "google_cloud_run_service" "agent_service" {
  name     = "vagabond-agent-service"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "gcr.io/vagabond-roadtrip/agent-app:latest"
        
        # Reference Google Secret Manager for secure credentials
        env {
          name = "GEMINI_API_KEY"
          value_from {
            secret_key_ref {
              name = "gemini-api-key-secret"
              key  = "latest"
            }
          }
        }
      }
    }
  }
}
