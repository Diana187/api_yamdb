class CreateListDestroyViewSet(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass
