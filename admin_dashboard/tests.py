from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .permissions import get_admin_role, can_update_payment_status
from unittest.mock import Mock
from django.http import HttpResponse
from django.urls import resolve
from django.test import Client


@override_settings(
    DEBUG=False,
    STORAGES={
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    },
)


class AdminAccessSecurityTests(TestCase):

    def test_customer_cannot_access_admin_dashboard(self):
        User = get_user_model()

        customer = User.objects.create_user(
            username="security_test_customer",
            email="security-test@example.com",
            password="TestPassword123!",
            is_staff=False,
        )

        self.client.force_login(customer)

        response = self.client.get("/admin_dashboard/")

        self.assertEqual(response.status_code, 404)

    def test_staff_can_access_admin_dashboard(self):
        User = get_user_model()

        staff = User.objects.create_user(
            username="security_test_staff",
            email="security-staff@example.com",
            password="TestPassword123!",
            is_staff=True,
            is_active=True,
        )
        group = Group.objects.create(name="Manager")

        staff.groups.add(group)

        self.client.force_login(staff)

        response = self.client.get("/admin_dashboard/")

        self.assertEqual(response.status_code, 200)

    def test_inactive_staff_cannot_access_admin_dashboard(self):
        User = get_user_model()

        staff = User.objects.create_user(
            username="security_inactive_staff",
            email="inactive-staff@example.com",
            password="TestPassword123!",
            is_staff=True,
            is_active=True,
        )

        self.client.force_login(staff)

        # Disable the account after login.
        staff.is_active = False
        staff.save(update_fields=["is_active"])

        response = self.client.get("/admin_dashboard/")

        self.assertEqual(response.status_code, 404)

    def test_regular_staff_cannot_access_admin_users(self):
        User = get_user_model()

        staff = User.objects.create_user(
            username="security_test_regular_staff",
            email="regular-staff@example.com",
            password="TestPassword123!",
            is_staff=True,
            is_active=True,
            is_superuser=False,
        )

        self.client.force_login(staff)

        response = self.client.get("/admin_dashboard/admin_users/")

        self.assertEqual(response.status_code, 404)

    def test_owner_can_access_admin_users(self):
        User = get_user_model()

        owner = User.objects.create_superuser(
            username="security_test_owner",
            email="security-owner@example.com",
            password="TestPassword123!",
        )

        self.client.force_login(owner)

        response = self.client.get("/admin_dashboard/admin_users/")

        self.assertEqual(response.status_code, 200)

    def test_staff_without_role_cannot_access_dashboard(self):
        User = get_user_model()

        staff = User.objects.create_user(
            username="security_test_groupless_staff",
            password="TestPassword123!",
            is_staff=True,
            is_active=True,
        )

        self.client.force_login(staff)

        response = self.client.get("/admin_dashboard/")

        self.assertEqual(response.status_code, 404)

    def test_support_cannot_access_payment_status_url(self):
        User = get_user_model()

        support = User.objects.create_user(
            username="security_test_payment_url_support",
            password="TestPassword123!",
            is_staff=True,
            is_active=True,
        )

        group = Group.objects.create(name="Support")
        support.groups.add(group)

        self.client.force_login(support)

        response = self.client.post(
            "/admin_dashboard/orders/999999/update-payment-status/",
            data={"payment_status": "Paid"},
        )

        self.assertEqual(response.status_code, 404)

    def test_warehouse_cannot_access_payment_status_url(self):
        User = get_user_model()

        warehouse = User.objects.create_user(
            username="security_test_payment_url_warehouse",
            password="TestPassword123!",
            is_staff=True,
            is_active=True,
        )

        group = Group.objects.create(name="Warehouse")
        warehouse.groups.add(group)

        self.client.force_login(warehouse)

        response = self.client.post(
            "/admin_dashboard/orders/999999/update-payment-status/",
            data={"payment_status": "Paid"},
        )

        self.assertEqual(response.status_code, 404)

    def test_manager_can_pass_payment_status_url_guard(self):
        User = get_user_model()

        manager = User.objects.create_user(
            username="security_test_payment_manager",
            password="TestPassword123!",
            is_staff=True,
            is_active=True,
        )

        group = Group.objects.create(name="Manager")
        manager.groups.add(group)

        request = self.client.post(
            "/admin_dashboard/orders/999999/update-payment-status/"
        ).wsgi_request

        request.user = manager

        matched = resolve(
            "/admin_dashboard/orders/999999/update-payment-status/"
        )

        mock_view = Mock(return_value=HttpResponse("Allowed"))

        from admin_dashboard.urls import payment_status_access_required

        protected_view = payment_status_access_required(mock_view)

        response = protected_view(
            request,
            *matched.args,
            **matched.kwargs
        )

        self.assertEqual(response.status_code, 200)
        mock_view.assert_called_once()

    def test_owner_can_pass_payment_status_url_guard(self):
        User = get_user_model()

        owner = User.objects.create_superuser(
            username="security_test_payment_owner",
            password="TestPassword123!",
        )

        request = self.client.post(
            "/admin_dashboard/orders/999999/update-payment-status/"
        ).wsgi_request

        request.user = owner

        from admin_dashboard.urls import payment_status_access_required

        mock_view = Mock(return_value=HttpResponse("Allowed"))
        protected_view = payment_status_access_required(mock_view)

        response = protected_view(request, order_id=999999)

        self.assertEqual(response.status_code, 200)
        mock_view.assert_called_once()

    def test_warehouse_cannot_update_order_status_url(self):
        User = get_user_model()

        warehouse = User.objects.create_user(
            username="security_order_warehouse",
            password="TestPassword123!",
            is_staff=True,
            is_active=True,
        )

        group = Group.objects.create(name="Warehouse")
        warehouse.groups.add(group)

        self.client.force_login(warehouse)

        response = self.client.post(
            "/admin_dashboard/orders/999999/update-status/",
            data={"status": "Confirmed"},
        )

        self.assertEqual(response.status_code, 404)

    def test_allowed_roles_can_pass_order_status_guard(self):
        from admin_dashboard.urls import order_status_access_required

        User = get_user_model()

        for role in ("Owner", "Manager", "Support"):
            with self.subTest(role=role):
                user = User.objects.create_user(
                    username=f"security_order_{role.lower()}",
                    password="TestPassword123!",
                    is_staff=True,
                    is_active=True,
                    is_superuser=(role == "Owner"),
                )

                if role != "Owner":
                    group, _ = Group.objects.get_or_create(name=role)
                    user.groups.add(group)

                request = self.client.post(
                    "/admin_dashboard/orders/999999/update-status/"
                ).wsgi_request

                request.user = user

                mock_view = Mock(return_value=HttpResponse("Allowed"))
                protected_view = order_status_access_required(mock_view)

                response = protected_view(request, order_id=999999)

                self.assertEqual(response.status_code, 200)
                mock_view.assert_called_once()

    def test_support_and_warehouse_cannot_manage_return_exchange(self):
        from django.urls import reverse

        User = get_user_model()

        actions = (
            "approve_return_exchange",
            "reject_return_exchange",
            "complete_return_exchange",
        )

        for role in ("Support", "Warehouse"):
            user = User.objects.create_user(
                username=f"security_return_{role.lower()}",
                password="TestPassword123!",
                is_staff=True,
                is_active=True,
            )

            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)

            self.client.force_login(user)

            for action in actions:
                with self.subTest(role=role, action=action):
                    url = reverse(action, args=[999999])

                    response = self.client.post(url)

                    self.assertEqual(response.status_code, 404)

    def test_owner_manager_can_manage_return_exchange(self):
        from admin_dashboard.urls import return_exchange_access_required
        from django.test import RequestFactory

        User = get_user_model()
        factory = RequestFactory()

        for role in ("Owner", "Manager"):
            user = User.objects.create_user(
                username=f"security_return_allowed_{role.lower()}",
                password="TestPassword123!",
                is_staff=True,
                is_active=True,
                is_superuser=(role == "Owner"),
            )

            if role == "Manager":
                group, _ = Group.objects.get_or_create(name="Manager")
                user.groups.add(group)

            for action in (
                "approve_return_exchange",
                "reject_return_exchange",
                "complete_return_exchange",
            ):
                with self.subTest(role=role, action=action):
                    request = factory.post("/security-test/")
                    request.user = user

                    mock_view = Mock(
                        return_value=HttpResponse("Allowed")
                    )

                    protected_view = return_exchange_access_required(mock_view)
                    response = protected_view(request, pk=999999)

                    self.assertEqual(response.status_code, 200)
                    mock_view.assert_called_once()

    def test_support_warehouse_cannot_manage_products(self):
        from django.urls import reverse

        actions = {
            "products_page": [],
            "categories_page": [],
            "add_product_page": [],
            "edit_product_page": [999999],
            "delete_product_page": [999999],
            "add_category": [],
            "edit_category": [999999],
            "delete_category": [999999],
        }

        User = get_user_model()

        for role in ("Support", "Warehouse"):
            user = User.objects.create_user(
                username=f"product_{role.lower()}",
                password="TestPass123!",
                is_staff=True,
            )
            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)
            self.client.force_login(user)

            for action, args in actions.items():
                with self.subTest(role=role, action=action):
                    response = self.client.get(reverse(action, args=args))
                    self.assertEqual(response.status_code, 404)

            self.client.logout()

    def test_support_cannot_access_inventory(self):
        from django.urls import reverse

        User = get_user_model()
        user = User.objects.create_user(
            username="inventory_support",
            password="TestPass123!",
            is_staff=True,
        )

        group, _ = Group.objects.get_or_create(name="Support")
        user.groups.add(group)
        self.client.force_login(user)

        for action in ("inventory_page", "update_inventory_stock"):
            with self.subTest(action=action):
                response = self.client.post(reverse(action))
                self.assertEqual(response.status_code, 404)

    def test_allowed_roles_pass_product_inventory_guards(self):
        from django.test import RequestFactory
        from django.urls import reverse
        from unittest.mock import Mock

        from .urls import (
            product_management_access_required,
            inventory_access_required,
        )

        User = get_user_model()
        factory = RequestFactory()

        cases = {
            "Owner": (
                "products_page",
                "add_product_page",
                "inventory_page",
                "update_inventory_stock",
            ),
            "Manager": (
                "products_page",
                "add_product_page",
                "inventory_page",
                "update_inventory_stock",
            ),
            "Warehouse": (
                "inventory_page",
                "update_inventory_stock",
            ),
        }

        for role, actions in cases.items():
            user = User.objects.create_user(
                username=f"allowed_{role.lower()}",
                password="TestPass123!",
                is_staff=True,
                is_superuser=(role == "Owner"),
            )

            if role != "Owner":
                group, _ = Group.objects.get_or_create(name=role)
                user.groups.add(group)

            for action in actions:
                with self.subTest(role=role, action=action):
                    url = reverse(action)

                    mock_view = Mock(
                        return_value=HttpResponse("OK")
                    )

                    guard = (
                        inventory_access_required
                        if action in (
                            "inventory_page",
                            "update_inventory_stock",
                        )
                        else product_management_access_required
                    )

                    request = factory.get(url)
                    request.user = user

                    response = guard(mock_view)(request)

                    self.assertEqual(response.status_code, 200)
                    mock_view.assert_called_once()

    def test_support_warehouse_cannot_access_coupons(self):
        from django.urls import reverse

        User = get_user_model()

        actions = {
            "coupons_page": [],
            "create_coupon": [],
            "update_coupon": [999999],
            "toggle_coupon": [999999],
            "delete_coupon": [999999],
        }

        for role in ("Support", "Warehouse"):
            user = User.objects.create_user(
                username=f"coupon_{role.lower()}",
                password="TestPass123!",
                is_staff=True,
            )

            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)

            self.client.force_login(user)

            for action, args in actions.items():
                with self.subTest(role=role, action=action):
                    response = self.client.post(
                        reverse(action, args=args)
                    )
                    self.assertEqual(response.status_code, 404)

            self.client.logout()

    def test_owner_manager_can_access_coupon_guards(self):
        from django.test import RequestFactory
        from django.urls import reverse
        from unittest.mock import Mock
        from .urls import coupon_access_required

        User = get_user_model()
        factory = RequestFactory()

        actions = {
            "coupons_page": [],
            "create_coupon": [],
            "update_coupon": [999999],
            "toggle_coupon": [999999],
            "delete_coupon": [999999],
        }

        for role in ("Owner", "Manager"):
            user = User.objects.create_user(
                username=f"coupon_allowed_{role.lower()}",
                password="TestPass123!",
                is_staff=True,
                is_superuser=(role == "Owner"),
            )

            if role == "Manager":
                group, _ = Group.objects.get_or_create(name="Manager")
                user.groups.add(group)

            for action, args in actions.items():
                with self.subTest(role=role, action=action):
                    url = reverse(action, args=args)

                    mock_view = Mock(
                        return_value=HttpResponse("OK")
                    )

                    request = factory.post(url)
                    request.user = user

                    response = coupon_access_required(mock_view)(request)

                    self.assertEqual(response.status_code, 200)
                    mock_view.assert_called_once()

    def test_warehouse_cannot_access_customers(self):
        from django.urls import reverse

        User = get_user_model()

        user = User.objects.create_user(
            username="customer_warehouse",
            password="TestPass123!",
            is_staff=True,
        )

        group, _ = Group.objects.get_or_create(name="Warehouse")
        user.groups.add(group)

        self.client.force_login(user)

        actions = {
            "customers_page": [],
            "customer_details": ["999999"],
        }

        for action, args in actions.items():
            with self.subTest(action=action):
                response = self.client.get(
                    reverse(action, args=args)
                )
                self.assertEqual(response.status_code, 404)

    def test_allowed_roles_pass_customer_guard(self):
        from django.test import RequestFactory
        from django.urls import reverse
        from unittest.mock import Mock
        from .urls import customer_access_required

        User = get_user_model()
        factory = RequestFactory()

        actions = {
            "customers_page": [],
            "customer_details": ["999999"],
        }

        for role in ("Owner", "Manager", "Support"):
            user = User.objects.create_user(
                username=f"customer_allowed_{role.lower()}",
                password="TestPass123!",
                is_staff=True,
                is_superuser=(role == "Owner"),
            )

            if role != "Owner":
                group, _ = Group.objects.get_or_create(name=role)
                user.groups.add(group)

            for action, args in actions.items():
                with self.subTest(role=role, action=action):
                    url = reverse(action, args=args)

                    mock_view = Mock(
                        return_value=HttpResponse("OK")
                    )

                    request = factory.get(url)
                    request.user = user

                    response = customer_access_required(mock_view)(request)

                    self.assertEqual(response.status_code, 200)
                    mock_view.assert_called_once()

    def test_warehouse_cannot_access_reviews_or_reports(self):
        from django.urls import reverse

        User = get_user_model()
        user = User.objects.create_user(
            username="review_report_warehouse",
            password="TestPass123!",
            is_staff=True,
        )

        group, _ = Group.objects.get_or_create(name="Warehouse")
        user.groups.add(group)
        self.client.force_login(user)

        for action in ("reviews_page", "reports_page"):
            with self.subTest(action=action):
                response = self.client.get(reverse(action))
                self.assertEqual(response.status_code, 404)

    def test_allowed_roles_pass_reviews_reports_guards(self):
        from django.test import RequestFactory
        from django.urls import reverse
        from unittest.mock import Mock
        from .urls import reviews_access_required, reports_access_required

        User = get_user_model()
        factory = RequestFactory()

        cases = {
            "Owner": {
                "reviews_page": reviews_access_required,
                "reports_page": reports_access_required,
            },
            "Manager": {
                "reviews_page": reviews_access_required,
                "reports_page": reports_access_required,
            },
            "Support": {
                "reviews_page": reviews_access_required,
            },
        }

        for role, actions in cases.items():
            user = User.objects.create_user(
                username=f"review_report_{role.lower()}",
                password="TestPass123!",
                is_staff=True,
                is_superuser=(role == "Owner"),
            )

            if role != "Owner":
                group, _ = Group.objects.get_or_create(name=role)
                user.groups.add(group)

            for action, guard in actions.items():
                with self.subTest(role=role, action=action):
                    url = reverse(action)
                    mock_view = Mock(return_value=HttpResponse("OK"))

                    request = factory.get(url)
                    request.user = user

                    response = guard(mock_view)(request)

                    self.assertEqual(response.status_code, 200)
                    mock_view.assert_called_once()

    def test_support_warehouse_cannot_access_store_settings(self):
        from django.urls import reverse

        User = get_user_model()

        for role in ("Support", "Warehouse"):
            user = User.objects.create_user(
                username=f"settings_{role.lower()}",
                password="TestPass123!",
                is_staff=True,
            )

            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)
            self.client.force_login(user)

            for action in (
                "delivery_settings_page",
                "home_management",
                "about_management",
                "contact_management",
                "update_home_page",
                "update_about_page",
            ):
                with self.subTest(role=role, action=action):
                    response = self.client.get(reverse(action))
                    self.assertEqual(response.status_code, 404)

            self.client.logout()

    def test_general_settings_owner_only(self):
        from django.urls import reverse

        User = get_user_model()

        manager = User.objects.create_user(
            username="general_settings_manager",
            password="TestPass123!",
            is_staff=True,
        )

        group, _ = Group.objects.get_or_create(name="Manager")
        manager.groups.add(group)

        self.client.force_login(manager)

        response = self.client.get(reverse("settings_page"))
        self.assertEqual(response.status_code, 404)

        self.client.logout()

        owner = User.objects.create_superuser(
            username="general_settings_owner",
            password="TestPass123!",
        )

        self.client.force_login(owner)

        response = self.client.get(reverse("settings_page"))
        self.assertEqual(response.status_code, 200)

    def test_owner_manager_pass_store_content_guards(self):
        from django.test import RequestFactory
        from django.urls import reverse
        from unittest.mock import Mock
        from .urls import store_content_access_required

        User = get_user_model()
        factory = RequestFactory()

        actions = (
            "delivery_settings_page",
            "home_management",
            "update_home_page",
            "about_management",
            "update_about_page",
            "contact_management",
        )

        for role in ("Owner", "Manager"):
            user = User.objects.create_user(
                username=f"store_content_{role.lower()}",
                password="TestPass123!",
                is_staff=True,
                is_superuser=(role == "Owner"),
            )

            if role != "Owner":
                group, _ = Group.objects.get_or_create(name=role)
                user.groups.add(group)

            for action in actions:
                with self.subTest(role=role, action=action):
                    mock_view = Mock(return_value=HttpResponse("OK"))

                    request = factory.get(reverse(action))
                    request.user = user

                    response = store_content_access_required(
                        mock_view
                    )(request)

                    self.assertEqual(response.status_code, 200)
                    mock_view.assert_called_once()

    def test_all_settings_routes_have_correct_guards(self):
        from django.contrib.auth.models import Group
        from django.http import Http404, HttpResponse
        from django.test import RequestFactory
        from unittest.mock import Mock

        from .urls import (
            urlpatterns,
            STORE_CONTENT_ACTIONS,
            store_content_access_required,
            general_settings_access_required,
        )

        User = get_user_model()
        factory = RequestFactory()
        roles = {}

        for role in ("Owner", "Manager", "Support", "Warehouse", "Customer"):
            user = User.objects.create_user(
                username=f"settings_audit_{role.lower()}",
                password="TestPass123!",
                is_staff=(role != "Customer"),
                is_superuser=(role == "Owner"),
            )

            if role in ("Manager", "Support", "Warehouse"):
                group, _ = Group.objects.get_or_create(name=role)
                user.groups.add(group)

            roles[role] = user

        settings_patterns = [
            pattern for pattern in urlpatterns
            if pattern.name == "settings_page"
            or pattern.name in STORE_CONTENT_ACTIONS
        ]

        self.assertEqual(len(settings_patterns), 30)
        self.assertEqual(
            {p.name for p in settings_patterns},
            STORE_CONTENT_ACTIONS | {"settings_page"},
        )

        for pattern in settings_patterns:
            action = pattern.name
            callback = pattern.callback

            if action == "settings_page":
                guard = general_settings_access_required
                allowed_roles = {"Owner"}
            else:
                guard = store_content_access_required
                allowed_roles = {"Owner", "Manager"}

            # Verify the actual registered security wrapper.
            self.assertEqual(
                callback.__code__,
                guard(Mock()).__code__,
                msg=f"Incorrect security wrapper: {action}",
            )

            for role, user in roles.items():
                with self.subTest(action=action, role=role):
                    request = factory.get("/")
                    request.user = user

                    if role not in allowed_roles:
                        with self.assertRaises(Http404):
                            callback(request)

                    else:
                        # Test the same guard with a harmless mock view.
                        mock_view = Mock(
                            return_value=HttpResponse("OK")
                        )

                        response = guard(mock_view)(request)

                        self.assertEqual(response.status_code, 200)
                        mock_view.assert_called_once()

    def test_warehouse_cannot_access_orders_page(self):
        User = get_user_model()

        warehouse = User.objects.create_user(
            username="security_warehouse_orders",
            password="TestPassword123!",
            is_staff=True,
            is_active=True,
        )

        group = Group.objects.create(name="Warehouse")
        warehouse.groups.add(group)

        self.client.force_login(warehouse)

        response = self.client.get("/admin_dashboard/orders/")

        self.assertEqual(response.status_code, 404)

    def test_warehouse_cannot_access_order_details(self):
        User = get_user_model()

        warehouse = User.objects.create_user(
            username="security_warehouse_order_details",
            password="TestPassword123!",
            is_staff=True,
            is_active=True,
        )

        group = Group.objects.create(name="Warehouse")
        warehouse.groups.add(group)

        self.client.force_login(warehouse)

        response = self.client.get(
            "/admin_dashboard/orders/NAFI-TEST-001/"
        )

        self.assertEqual(response.status_code, 404)

    def test_owner_manager_support_can_pass_orders_view_guard(self):
        from admin_dashboard.urls import order_view_access_required

        User = get_user_model()

        for role in ("Owner", "Manager", "Support"):
            with self.subTest(role=role):
                user = User.objects.create_user(
                    username=f"security_orders_{role.lower()}",
                    password="TestPassword123!",
                    is_staff=True,
                    is_active=True,
                    is_superuser=(role == "Owner"),
                )

                if role != "Owner":
                    group = Group.objects.create(name=role)
                    user.groups.add(group)

                request = self.client.get(
                    "/admin_dashboard/orders/"
                ).wsgi_request

                request.user = user

                mock_view = Mock(
                    return_value=HttpResponse("Allowed")
                )

                protected_view = order_view_access_required(mock_view)
                response = protected_view(request)

                self.assertEqual(response.status_code, 200)
                mock_view.assert_called_once()

    def test_warehouse_can_access_dashboard(self):
        User = get_user_model()

        warehouse = User.objects.create_user(
            username="security_warehouse_dashboard",
            password="TestPassword123!",
            is_staff=True,
            is_active=True,
        )

        group = Group.objects.create(name="Warehouse")
        warehouse.groups.add(group)

        self.client.force_login(warehouse)

        response = self.client.get("/admin_dashboard/")

        self.assertEqual(response.status_code, 200)

    def test_warehouse_can_access_inventory(self):
        User = get_user_model()

        warehouse = User.objects.create_user(
            username="security_warehouse_inventory",
            password="TestPassword123!",
            is_staff=True,
            is_active=True,
        )

        group = Group.objects.create(name="Warehouse")
        warehouse.groups.add(group)

        self.client.force_login(warehouse)

        response = self.client.get("/admin_dashboard/inventory/")

        self.assertEqual(response.status_code, 200)



class AdminRoleTests(TestCase):

    def test_manager_role_detection(self):
        User = get_user_model()

        manager = User.objects.create_user(
            username="security_test_manager",
            password="TestPassword123!",
            is_staff=True,
            is_active=True,
        )

        group = Group.objects.create(name="Manager")
        manager.groups.add(group)

        self.assertEqual(get_admin_role(manager), "Manager")

    def test_owner_role_detection(self):
        User = get_user_model()

        owner = User.objects.create_superuser(
            username="security_test_role_owner",
            email="role-owner@example.com",
            password="TestPassword123!",
        )

        self.assertEqual(get_admin_role(owner), "Owner")

    def test_support_role_detection(self):
        User = get_user_model()

        support = User.objects.create_user(
            username="security_test_support",
            password="TestPassword123!",
            is_staff=True,
            is_active=True,
        )

        group = Group.objects.create(name="Support")
        support.groups.add(group)

        self.assertEqual(get_admin_role(support), "Support")
    def test_warehouse_role_detection(self):
        User = get_user_model()

        warehouse = User.objects.create_user(
            username="security_test_warehouse",
            password="TestPassword123!",
            is_staff=True,
            is_active=True,
        )

        group = Group.objects.create(name="Warehouse")
        warehouse.groups.add(group)

        self.assertEqual(get_admin_role(warehouse), "Warehouse")
    def test_staff_without_role_returns_none(self):
        User = get_user_model()

        staff = User.objects.create_user(
            username="security_test_no_role",
            password="TestPassword123!",
            is_staff=True,
            is_active=True,
        )

        self.assertIsNone(get_admin_role(staff))

    def test_customer_with_admin_group_returns_none(self):
        User = get_user_model()

        customer = User.objects.create_user(
            username="security_test_customer_group",
            password="TestPassword123!",
            is_staff=False,
            is_active=True,
        )

        group = Group.objects.create(name="Manager")
        customer.groups.add(group)

        self.assertIsNone(get_admin_role(customer))

    def test_manager_can_update_payment_status(self):
        User = get_user_model()

        manager = User.objects.create_user(
            username="security_test_payment_manager",
            password="TestPassword123!",
            is_staff=True,
            is_active=True,
        )

        group = Group.objects.create(name="Manager")
        manager.groups.add(group)

        self.assertTrue(can_update_payment_status(manager))
    def test_support_cannot_update_payment_status(self):
        User = get_user_model()

        support = User.objects.create_user(
            username="security_test_payment_support",
            password="TestPassword123!",
            is_staff=True,
            is_active=True,
        )

        group = Group.objects.create(name="Support")
        support.groups.add(group)

        self.assertFalse(can_update_payment_status(support))
    def test_warehouse_cannot_update_payment_status(self):
        User = get_user_model()

        warehouse = User.objects.create_user(
            username="security_test_payment_warehouse",
            password="TestPassword123!",
            is_staff=True,
            is_active=True,
        )

        group = Group.objects.create(name="Warehouse")
        warehouse.groups.add(group)

        self.assertFalse(can_update_payment_status(warehouse))


@override_settings(DEBUG=False)
class BuiltinAdminSecurityTests(TestCase):

    def test_builtin_admin_owner_only(self):
        from django.urls import reverse

        User = get_user_model()
        admin_url = reverse("admin:index")

        cases = (
            ("Owner", True, True, True, True),
            ("Manager", True, False, True, False),
            ("Support", True, False, True, False),
            ("Warehouse", True, False, True, False),
            ("Customer", False, False, True, False),
            ("InactiveOwner", True, True, False, False),
        )

        for role, is_staff, is_superuser, is_active, allowed in cases:
            user = User.objects.create_user(
                username=f"builtin_admin_{role.lower()}",
                password="TestPass123!",
                is_staff=is_staff,
                is_superuser=is_superuser,
                is_active=is_active,
            )

            if role in ("Manager", "Support", "Warehouse"):
                group, _ = Group.objects.get_or_create(name=role)
                user.groups.add(group)

            self.client.force_login(user)

            with self.subTest(role=role):
                response = self.client.get(admin_url)

                if allowed:
                    self.assertEqual(response.status_code, 200)
                else:
                    self.assertNotEqual(response.status_code, 200)

            self.client.logout()

    def test_non_owner_cannot_access_sensitive_admin_models(self):
        from django.urls import reverse

        User = get_user_model()

        sensitive_urls = (
            reverse("admin:account_user_changelist"),
            reverse("admin:auth_group_changelist"),
            reverse("admin:experiment1_order_changelist"),
            reverse("admin:admin_dashboard_productsmodel_changelist"),
            reverse("admin:social_django_usersocialauth_changelist"),
        )

        for role in ("Manager", "Support", "Warehouse"):
            user = User.objects.create_user(
                username=f"sensitive_admin_{role.lower()}",
                password="TestPass123!",
                is_staff=True,
            )

            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)

            self.client.force_login(user)

            for url in sensitive_urls:
                with self.subTest(role=role, url=url):
                    response = self.client.get(url, follow=False)
                    self.assertNotEqual(response.status_code, 200)

            self.client.logout()

@override_settings(DEBUG=False)
class AdminHttpMethodSecurityTests(TestCase):

    def test_sensitive_order_actions_reject_get(self):
        from django.urls import reverse

        User = get_user_model()

        owner = User.objects.create_superuser(
            username="http_method_owner",
            password="TestPass123!",
        )

        self.client.force_login(owner)

        urls = (
            reverse(
                "update_order_status",
                kwargs={"order_number": "NAFI-TEST-001"},
            ),
            reverse(
                "update_payment_status",
                kwargs={"order_number": "NAFI-TEST-001"},
            ),
            reverse(
                "approve_return_exchange",
                kwargs={"request_id": 999999},
            ),
            reverse(
                "reject_return_exchange",
                kwargs={"request_id": 999999},
            ),
            reverse(
                "complete_return_exchange",
                kwargs={"request_id": 999999},
            ),
        )

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 405)

    def test_sensitive_actions_reject_post_without_csrf(self):
        from django.urls import reverse

        User = get_user_model()

        owner = User.objects.create_superuser(
            username="csrf_test_owner",
            password="TestPass123!",
        )

        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(owner)

        urls_and_data = (
            (
                reverse(
                    "update_order_status",
                    kwargs={"order_number": "NAFI-TEST-001"},
                ),
                {"status": "Confirmed"},
            ),
            (
                reverse(
                    "update_payment_status",
                    kwargs={"order_number": "NAFI-TEST-001"},
                ),
                {"payment_status": "Paid"},
            ),
            (
                reverse(
                    "approve_return_exchange",
                    kwargs={"request_id": 999999},
                ),
                {},
            ),
            (
                reverse(
                    "reject_return_exchange",
                    kwargs={"request_id": 999999},
                ),
                {},
            ),
            (
                reverse(
                    "complete_return_exchange",
                    kwargs={"request_id": 999999},
                ),
                {"returned_item_condition": "sellable"},
            ),
        )

        for url, data in urls_and_data:
            with self.subTest(url=url):
                response = csrf_client.post(url, data)
                self.assertEqual(response.status_code, 403)

    def test_admin_get_logout_rejected(self):
        from django.urls import reverse

        User = get_user_model()

        owner = User.objects.create_superuser(
            username="logout_get_owner",
            password="TestPass123!",
        )

        self.client.force_login(owner)

        response = self.client.get(reverse("logout_page"))

        self.assertEqual(response.status_code, 405)
        self.assertIn("_auth_user_id", self.client.session)

    def test_admin_post_logout_success(self):
        from django.urls import reverse

        User = get_user_model()

        owner = User.objects.create_superuser(
            username="logout_post_owner",
            password="TestPass123!",
        )

        self.client.force_login(owner)

        response = self.client.post(reverse("logout_page"))

        self.assertEqual(response.status_code, 302)
        self.assertNotIn("_auth_user_id", self.client.session)

        dashboard_response = self.client.get(
            reverse("dashboard_page")
        )

        self.assertEqual(dashboard_response.status_code, 404)

    def test_admin_logout_rejects_post_without_csrf(self):
        from django.urls import reverse

        User = get_user_model()

        owner = User.objects.create_superuser(
            username="logout_csrf_owner",
            password="TestPass123!",
        )

        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(owner)

        response = csrf_client.post(reverse("logout_page"))

        self.assertEqual(response.status_code, 403)
        self.assertIn("_auth_user_id", csrf_client.session)
