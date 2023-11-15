# Deploy image to Cloud Run
resource "google_cloud_run_service" "birdserver" {
  provider = google
  count    = var.first_time ? 0 : 1
  name     = "birdserver"
  location = var.region
  template {
    spec {
      containers {
        image = "${var.region}-docker.pkg.dev/${var.project_id}/${var.repository}/${var.docker_image}"
        resources {
          limits = {
            cpu    = "1"
            memory = "4G"
          }
        }
      }
    }
    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale" = "0"
        "autoscaling.knative.dev/maxScale" = "3"
      }
    }
  }
  traffic {
    percent         = 100
    latest_revision = true
  }
  depends_on = [google_artifact_registry_repository_iam_member.docker_pusher_iam]
}

# Create a policy that allows all users to invoke the API
data "google_iam_policy" "noauth" {
  provider = google
  count    = var.first_time ? 0 : 1
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

# Apply the no-authentication policy to our Cloud Run Service.
resource "google_cloud_run_service_iam_policy" "noauth" {
  count    = var.first_time ? 0 : 1
  provider = google
  location = var.region
  project  = var.project_id
  service  = google_cloud_run_service.birdserver[0].name

  policy_data = data.google_iam_policy.noauth[0].policy_data
}

output "cloud_run_instance_url" {
  value = var.first_time ? null : google_cloud_run_service.birdserver[0].status.0.url
}