resource "google_cloud_run_v2_service" "backend" {
  name     = "nutrisense-backend"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = "gcr.io/${var.project_id}/nutrisense-backend:latest"
      
      env {
        name  = "GCP_PROJECT_ID"
        value = var.project_id
      }
      
      # Secrets should ideally come from Secret Manager
      # using data "google_secret_manager_secret_version"
    }
  }

  depends_on = [google_project_service.run_api]
}

resource "google_cloud_run_service_iam_member" "backend_public" {
  location = google_cloud_run_v2_service.backend.location
  project  = google_cloud_run_v2_service.backend.project
  service  = google_cloud_run_v2_service.backend.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

resource "google_cloud_run_v2_service" "frontend" {
  name     = "nutrisense-frontend"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = "gcr.io/${var.project_id}/nutrisense-frontend:latest"
    }
  }

  depends_on = [google_project_service.run_api]
}

resource "google_cloud_run_service_iam_member" "frontend_public" {
  location = google_cloud_run_v2_service.frontend.location
  project  = google_cloud_run_v2_service.frontend.project
  service  = google_cloud_run_v2_service.frontend.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
