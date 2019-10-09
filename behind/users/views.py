from rest_auth.views import PasswordResetConfirmView, sensitive_post_parameters_m
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    renderer_classes = [TemplateHTMLRenderer]

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordResetConfirmView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(template_name='password/password_reset_done.html')

