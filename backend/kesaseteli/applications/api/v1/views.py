from django.core import exceptions
from django.http import FileResponse
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from shared.audit_log.viewsets import AuditLoggingModelViewSet
from shared.oidc.auth import EAuthRestAuthentication

from applications.api.v1.auth import StaffAuthentication
from applications.api.v1.permissions import (
    ALLOWED_APPLICATION_UPDATE_STATUSES,
    ALLOWED_APPLICATION_VIEW_STATUSES,
    ApplicationPermission,
    get_user_company,
    StaffPermission,
    SummerVoucherPermission,
)
from applications.api.v1.serializers import (
    ApplicationSerializer,
    AttachmentSerializer,
    SummerVoucherSerializer,
)
from applications.enums import ApplicationStatus
from applications.models import Application, SummerVoucher


class ApplicationViewSet(AuditLoggingModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, ApplicationPermission]

    def get_queryset(self):
        """
        Fetch all DRAFT status applications of the user & company.
        Should inlcude only 1 application since we don't allow creation of multiple
        DRAFT applications per user & company.
        """
        queryset = (
            super()
            .get_queryset()
            .select_related("company")
            .prefetch_related("summer_vouchers")
        )

        user = self.request.user
        if user.is_anonymous:
            return queryset.none()

        user_company = get_user_company(self.request)

        return queryset.filter(
            company=user_company,
            user=user,
            status__in=ALLOWED_APPLICATION_VIEW_STATUSES,
        )

    def create(self, request, *args, **kwargs):
        """
        Allow only 1 (DRAFT) application per user & company.
        """
        if self.get_queryset().filter(status=ApplicationStatus.DRAFT).exists():
            raise ValidationError("Company & user can have only one draft application")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Allow to update only DRAFT status applications.
        """
        instance = self.get_object()
        if instance.status not in ALLOWED_APPLICATION_UPDATE_STATUSES:
            raise ValidationError("Only DRAFT applications can be updated")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class SummerVoucherViewSet(AuditLoggingModelViewSet):
    queryset = SummerVoucher.objects.all()
    serializer_class = SummerVoucherSerializer
    authentication_classes = [EAuthRestAuthentication, StaffAuthentication]
    permission_classes = [IsAuthenticated, SummerVoucherPermission | StaffPermission]

    def get_queryset(self):
        """
        Fetch summer vouchers of DRAFT status applications of the user & company.
        """
        queryset = (
            super()
            .get_queryset()
            .select_related("application")
            .prefetch_related("attachments")
        )

        user = self.request.user
        if user.is_staff:
            return queryset
        elif user.is_anonymous:
            return queryset.none()

        user_company = get_user_company(self.request)

        return queryset.filter(
            application__company=user_company,
            application__user=user,
            application__status__in=ALLOWED_APPLICATION_VIEW_STATUSES,
        )

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        methods=("POST",),
        detail=True,
        url_path="attachments",
        parser_classes=(MultiPartParser,),
    )
    def post_attachment(self, request, *args, **kwargs):
        """
        Upload a single file as attachment
        """
        obj = self.get_object()

        if obj.application.status not in ALLOWED_APPLICATION_UPDATE_STATUSES:
            raise ValidationError(
                "Attachments can be uploaded only for DRAFT applications"
            )

        # Validate request data
        serializer = AttachmentSerializer(
            data={
                "summer_voucher": obj.id,
                "attachment_file": request.data["attachment_file"],
                "content_type": request.data["attachment_file"].content_type,
                "attachment_type": request.data["attachment_type"],
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        methods=(
            "GET",
            "DELETE",
        ),
        detail=True,
        url_path="attachments/(?P<attachment_pk>[^/.]+)",
    )
    def handle_attachment(self, request, attachment_pk, *args, **kwargs):
        obj = self.get_object()

        if request.method == "GET":
            """
            Read a single attachment as file
            """
            attachment = obj.attachments.filter(pk=attachment_pk).first()
            if not attachment or not attachment.attachment_file:
                return Response(
                    {
                        "detail": format_lazy(
                            _("File not found."),
                        )
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            return FileResponse(attachment.attachment_file)

        elif request.method == "DELETE":
            """
            Delete a single attachment as file
            """
            if obj.application.status not in ALLOWED_APPLICATION_UPDATE_STATUSES:
                raise ValidationError(
                    "Attachments can be deleted only for DRAFT applications"
                )

            if (
                obj.application.status
                not in AttachmentSerializer.ATTACHMENT_MODIFICATION_ALLOWED_STATUSES
            ):
                return Response(
                    {"detail": _("Operation not allowed for this application status.")},
                    status=status.HTTP_403_FORBIDDEN,
                )
            try:
                instance = obj.attachments.get(id=attachment_pk)
            except exceptions.ObjectDoesNotExist:
                return Response(
                    {"detail": _("File not found.")}, status=status.HTTP_404_NOT_FOUND
                )
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
