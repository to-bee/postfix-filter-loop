from rest_framework import viewsets

from monitoring.models import Email
from monitoring.serializers import EmailSerializer


class EmailViewSet(viewsets.ModelViewSet):
    authentication_classes = []  # disable csrf for delete requests
    queryset = Email.objects.all()
    serializer_class = EmailSerializer

    def get_queryset(self):
        return self.queryset

    # def destroy(self, request, *args, **kwargs):
    #     existing_prediction = self.get_object()
    #
    #     img = existing_prediction.image.path
    #     if os.path.isfile(img):
    #         os.remove(img)
    #
    #     self.perform_destroy(existing_prediction)
    #     return Response(status.HTTP_200_OK)