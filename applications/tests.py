from django.http import HttpResponse
from django.utils import timezone
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from accounts.models import User
from marketplace.models import Listing, Career
from tests_mixins.init_accounts import InitAccountsMixin


class ApplicationsTestCase(TestCase, InitAccountsMixin):

    @classmethod
    def setUpTestData(cls):
        super().set_up()
        cls.rand_employer = cls.create_new_employer()
        cls.listing = cls.create_listing(cls)

    def setUp(self) -> None:
        self.factory = RequestFactory()

    def login(self, profile) -> None:
        self.client.login(username=profile.email, password=self.password)

    def logout(self) -> None:
        self.client.logout()

    def apply(self) -> HttpResponse:
        return self.client.get(reverse('apply', kwargs={'listing_id': self.listing.id}),
                               )

    def create_listing(self) -> Listing:
        career = Career.objects.create(career='some career')
        career.save()
        return Listing.objects.create(company=self.employer, title='some listing', type='Unpaid', where='Virtual',
                                      career=career, application_deadline=timezone.now(), description='description')

    def check_login_redirected(self, path):
        response = self.client.get(path, follow=True)
        self.assertEqual(response.request['PATH_INFO'], reverse('login'))

    def login_apply_out(self):
        self.login(self.student)
        self.apply()
        self.logout()

    @staticmethod
    def create_new_employer():
        new_employer = User.objects.create_user(email='rand@gmail.com', first_name='first', last_name='last',
                                                password='password',
                                                is_student=False, is_employer=True)
        new_employer.save()
        return new_employer

    def accept_student(self) -> HttpResponse:
        return self.client.get(reverse('accept', kwargs={
            'listing_id': self.listing.id,
            'student_id': self.student.id
        }))

    def reject_student(self) -> HttpResponse:
        return self.client.get(reverse('reject', kwargs={
            'listing_id': self.listing.id,
            'student_id': self.student.id
        }))

    def test_applications_login_redirect(self):
        self.check_login_redirected(reverse('applications'))

    def test_employer_applications(self):
        path = reverse('applications')
        self.login(self.employer)
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)

    def test_student_applications(self):
        path = reverse('applications')
        self.login(self.student)
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)

    def test_archive_interview_request_login_redirect(self):
        self.check_login_redirected(reverse('archive_interview_request', kwargs={
            'listing_id': self.listing.id,
            'student_id': self.student.id
        }))

    def test_student_archive_archive_interview_request(self):
        path = reverse('archive_interview_request', kwargs={
            'listing_id': self.listing.id,
            'student_id': self.student.id
        })
        self.login_apply_out()
        self.login(self.employer)
        self.accept_student()
        self.logout()
        self.login(self.student)
        response = self.client.get(path, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.student in self.listing.student_interview_requests.all())

    def test_rand_employer_archive_interview_request(self):
        path = reverse('archive_interview_request', kwargs={
            'listing_id': self.listing.id,
            'student_id': self.student.id
        })
        self.login_apply_out()
        self.login(self.employer)
        self.accept_student()
        self.login(self.rand_employer)
        self.assertRaises(PermissionError, self.client.get, path)

    def test_employer_archive_archive_interview_request(self):
        path = reverse('archive_interview_request', kwargs={
            'listing_id': self.listing.id,
            'student_id': self.student.id
        })
        self.login_apply_out()
        self.login(self.employer)
        self.accept_student()
        response = self.client.get(path, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.student in self.listing.employer_interview_requests.all())

    def test_archive_rejected_login_redirect(self):
        self.check_login_redirected(reverse('archive_rejected', kwargs={
            'listing_id': self.listing.id,
            'student_id': self.student.id
        }))

    def test_student_archive_rejected(self):
        path = reverse('archive_rejected', kwargs={
            'listing_id': self.listing.id,
            'student_id': self.student.id
        })
        self.login_apply_out()
        self.login(self.employer)
        self.accept_student()
        self.logout()
        self.login(self.student)
        response = self.client.get(path, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.student in self.listing.student_rejections.all())

    def test_rand_employer_archive_rejected(self):
        path = reverse('archive_rejected', kwargs={
            'listing_id': self.listing.id,
            'student_id': self.student.id
        })
        self.login(self.employer)
        self.accept_student()
        self.logout()
        self.login(self.rand_employer)
        self.assertRaises(PermissionError, self.client.get, path)

    def test_employer_archive_rejected(self):
        path = reverse('archive_rejected', kwargs={
            'listing_id': self.listing.id,
            'student_id': self.student.id
        })
        self.login_apply_out()
        self.login(self.employer)
        self.accept_student()
        response = self.client.get(path, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.student in self.listing.employer_rejections.all())

    def test_archive_accepted_login_redirect(self):
        self.check_login_redirected(reverse('archive_accepted', kwargs={
            'listing_id': self.listing.id,
            'student_id': self.student.id
        }))

    def test_student_archive_accepted(self):
        path = reverse('archive_accepted', kwargs={
            'listing_id': self.listing.id,
            'student_id': self.student.id
        })
        self.login_apply_out()
        self.login(self.employer)
        self.accept_student()
        self.logout()
        self.login(self.student)
        response = self.client.get(path, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.student in self.listing.student_acceptances.all())

    def test_rand_employer_archive_accepted(self):
        path = reverse('archive_accepted', kwargs={
            'listing_id': self.listing.id,
            'student_id': self.student.id
        })
        self.login(self.employer)
        self.accept_student()
        self.logout()
        self.login(self.rand_employer)
        self.assertRaises(PermissionError, self.client.get, path)

    def test_employer_archive_accepted(self):
        path = reverse('archive_accepted', kwargs={
            'listing_id': self.listing.id,
            'student_id': self.student.id
        })
        self.login_apply_out()
        self.login(self.employer)
        self.accept_student()
        response = self.client.get(path, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.student in self.listing.employer_acceptances.all())

    def test_view_interview_requests_login_redirect(self):
        self.check_login_redirected(reverse('rejections'))

    def test_student_view_interview_requests(self):
        path = reverse('interview_requests')
        self.login(self.employer)
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)

    def test_employer_view_interview_requests(self):
        path = reverse('interview_requests')
        self.login(self.employer)
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)

    def test_view_rejections_login_redirect(self):
        self.check_login_redirected(reverse('rejections'))

    def test_student_view_rejections(self):
        path = reverse('rejections')
        self.login(self.employer)
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)

    def test_employer_view_rejections(self):
        path = reverse('rejections')
        self.login(self.employer)
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)

    def test_view_acceptances_login_redirect(self):
        self.check_login_redirected(reverse('acceptances'))

    def test_student_view_acceptances(self):
        path = reverse('acceptances')
        self.login(self.employer)
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)

    def test_employer_view_acceptances(self):
        path = reverse('acceptances')
        self.login(self.employer)
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)

    def test_application_login_redirect(self):
        self.check_login_redirected(reverse('single_application', kwargs={
            'listing_slug': self.listing.slug,
            'user_slug': self.student.slug
        }))

    def test_student_view_application(self):
        path = reverse('single_application', kwargs={
            'listing_slug': self.listing.slug,
            'user_slug': self.student.slug
        })
        self.login(self.student)
        self.assertRaises(PermissionError, self.client.get, path)

    def test_rand_employer_view_application(self):
        self.login(self.rand_employer)

        self.assertRaises(PermissionError, self.client.get, reverse('single_application', kwargs={
            'listing_slug': self.listing.slug,
            'user_slug': self.student.slug
        }))

    def test_employer_view_application(self):
        path = reverse('single_application', kwargs={
            'listing_slug': self.listing.slug,
            'user_slug': self.student.slug
        })
        self.login(self.employer)
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)

    def test_random_employer_request_interview(self):
        self.login(self.rand_employer)
        self.assertRaises(PermissionError, self.client.get, reverse('request_interview', kwargs={
            'listing_id': self.listing.id,
            'student_id': self.student.id
        }))

    def test_request_interview_login_redirect(self):
        self.check_login_redirected(reverse('request_interview', kwargs={
            'listing_id': self.listing.id,
            'student_id': self.student.id
        }))

    def test_employer_request_interview(self):
        path = reverse('request_interview', kwargs={
            'listing_id': self.listing.id,
            'student_id': self.student.id
        })
        self.login_apply_out()
        self.login(self.employer)
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.student in self.listing.applications.all())
        self.assertTrue(self.student in self.listing.interview_requests.all())

    def test_student_request_interview(self):
        path = reverse('request_interview', kwargs={
            'listing_id': self.listing.id,
            'student_id': self.student.id
        })
        self.login(self.student)
        self.assertRaises(PermissionError, self.client.get, path)

    def test_reject_login_redirect(self):
        self.check_login_redirected(reverse('reject', kwargs={
            'listing_id': self.listing.id,
            'student_id': self.student.id
        }))

    def test_employer_reject(self):
        self.login_apply_out()
        self.login(self.employer)
        response = self.reject_student()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.student in self.listing.student_rejections.all())
        self.assertTrue(self.student in self.listing.employer_rejections.all())
        self.assertTrue(self.student in self.listing.rejections.all())
        self.assertFalse(self.student in self.listing.applications.all())

    # try to reject a student as a student
    def test_student_reject(self):
        self.login_apply_out()
        self.login(self.student)
        self.assertRaises(PermissionError, self.reject_student)

    def test_accept_login_redirect(self):
        self.check_login_redirected(reverse('accept', kwargs={
            'listing_id': self.listing.id,
            'student_id': self.student.id
        }))

    def test_employer_accept(self):
        self.login_apply_out()
        self.login(self.employer)
        response = self.accept_student()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.student in self.listing.student_acceptances.all())
        self.assertTrue(self.student in self.listing.employer_acceptances.all())
        self.assertTrue(self.student in self.listing.acceptances.all())
        self.assertFalse(self.student in self.listing.applications.all())

    # try to accept a student as a student
    def test_student_accept(self):
        self.login_apply_out()
        self.login(self.student)
        self.assertRaises(PermissionError, self.accept_student)

    def test_unapply_login_redirect(self):
        self.check_login_redirected(reverse('unapply', kwargs={
            'listing_id': self.listing.id,
        }))

    def test_student_unapply(self):
        path = reverse('unapply', kwargs={'listing_id': self.listing.id})
        self.login(self.student)
        self.apply()
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertRaises(ObjectDoesNotExist, self.listing.applications.get, id=self.student.id)

    def test_employer_unapply(self):
        path = reverse('unapply', kwargs={'listing_id': self.listing.id})
        self.login(self.employer)
        self.assertRaises(PermissionError, self.client.get, path,
                          )

    def test_apply_login_redirect(self):
        self.check_login_redirected(reverse('apply', kwargs={
            'listing_id': self.listing.id,
        }))

    def test_student_apply(self):
        path = reverse('apply', kwargs={'listing_id': self.listing.id})
        self.login(self.student)
        response = self.apply()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.listing.applications.get(id=self.student.id))

    def test_employer_apply(self):
        path = reverse('apply', kwargs={'listing_id': self.listing.id})
        self.login(self.employer)
        self.assertRaises(PermissionError, self.client.get, path)
