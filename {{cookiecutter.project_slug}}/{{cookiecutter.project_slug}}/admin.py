from flask import current_app
from flask import flash
from flask import redirect
from flask import request
from flask import url_for
from flask_admin import AdminIndexView
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.model.template import EndpointLinkRowAction
from flask_login import login_user
from flask_principal import Identity
from flask_principal import identity_changed

from .permissions import admin_permission


class SecureViewMixin:
    def is_accessible(self):
        return admin_permission.can()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("public.login", next=request.url))


class ProtectedAdminIndexView(SecureViewMixin, AdminIndexView):
    pass


class BaseModelView(SecureViewMixin, ModelView):
    extra_css = ["/static/vendor/fontawesome-free-5.14.0-web/css/all.min.css"]


class UserModelView(BaseModelView):
    can_delete = False  # disable model deletion
    can_create = False
    can_view_details = True
    can_export = True
    column_searchable_list = ["email"]
    form_excluded_columns = [
        "password",
        "subscriptions",
        "export_requests",
        "created_at",
        "bulk_search_requests",
        "api_keys",
        "features",
    ]
    column_exclude_list = [
        "password",
        "first_name",
        "last_name",
    ]
    column_details_list = [
        "id",
        "plan_slug",
        "feature_slugs",
        "created_at",
        "first_name",
        "last_name",
        "is_active",
        "is_admin",
    ]
    column_export_exclude_list = [
        "password",
    ]
    column_default_sort = ("created_at", True)
    column_list = [
        "email",
        "plan_slug",
        "created_at",
        "is_active",
        "is_admin",
    ]
    column_extra_row_actions = [
        EndpointLinkRowAction(
            "fa fa-sign-in-alt", "admin.user.login_as", id_arg="user_id",
        )
    ]

    @expose("/login-as/<user_id>")
    def login_as(self, user_id):
        from .models.accounts import User

        user = User.query.filter_by(id=user_id).first_or_404()
        login_user(user, remember=False)
        identity_changed.send(
            current_app._get_current_object(), identity=Identity(user.id)
        )
        flash(f"You are logged in as {user.email}.", "success")
        redirect_url = url_for("public.home")
        return redirect(redirect_url)
