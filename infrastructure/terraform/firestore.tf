resource "google_firestore_database" "database" {
  project     = var.project_id
  name        = "(default)"
  location_id = "nam5" # Multi-region US
  type        = "FIRESTORE_NATIVE"

  depends_on = [google_project_service.firestore_api]
}
