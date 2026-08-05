from django.contrib.auth.models import User
from django.test import TestCase

from .models import Applications, Job


class RegisterUserTests(TestCase):
    def test_register_endpoint_creates_user_with_hashed_password(self):
        response = self.client.post(
            "/register/",
            {"username": "tom", "email": "tom@gmail.com", "password": "tom123"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username="tom").exists())

        user = User.objects.get(username="tom")
        self.assertTrue(user.check_password("tom123"))

    def test_apply_endpoint_accepts_applicant_payload_and_creates_application(self):
        recruiter = User.objects.create_user(
            username="recruiter", password="pass123")
        applicant = User.objects.create_user(
            username="applicant", password="pass123")
        job = Job.objects.create(
            title="Python Developer",
            description="Build APIs",
            company="Acme",
            location="Remote",
            salary_range="1000-2000",
            created_by=recruiter,
        )

        response = self.client.post(
            "/apply/",
            {"job": job.id, "applicant": applicant.id},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Applications.objects.filter(
            job=job, applicants=applicant).exists())

    def test_apply_endpoint_rejects_duplicate_application_for_same_job_and_applicant(self):
        recruiter = User.objects.create_user(
            username="recruiter2", password="pass123")
        applicant = User.objects.create_user(
            username="applicant2", password="pass123")
        job = Job.objects.create(
            title="Data Engineer",
            description="Work with ETL",
            company="Acme",
            location="Remote",
            salary_range="2000-3000",
            created_by=recruiter,
        )

        first_response = self.client.post(
            "/apply/",
            {"job": job.id, "applicants": applicant.id},
            content_type="application/json",
        )
        second_response = self.client.post(
            "/apply/",
            {"job": job.id, "applicants": applicant.id},
            content_type="application/json",
        )

        self.assertEqual(first_response.status_code, 201)
        self.assertEqual(second_response.status_code, 400)
        self.assertIn("already applied", str(second_response.data).lower())
