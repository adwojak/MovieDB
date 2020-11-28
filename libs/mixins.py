from rest_framework.mixins import CreateModelMixin
from attrdict import AttrDict


class InputCreateModelMixin(CreateModelMixin):
    """
    Create a model instance, but with serialization of another serializer than `serializer_class`
    """

    @property
    def input_serializer_class(self):
        raise NotImplementedError

    def create_response(self, data: dict) -> dict:
        raise NotImplementedError

    def create(self, request, *args, **kwargs):
        serializer = self.input_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_response = self.create_response(request.data)
        return super(InputCreateModelMixin, self).create(AttrDict({'data': create_response}), *args, **kwargs)
