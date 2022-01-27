from rest_framework import viewsets, status



class TenantModelViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        org = self.request.user.org
        return self.serializer_class.Meta.model.objects.filter(organization=org)
        