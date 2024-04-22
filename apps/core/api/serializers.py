import copy

from rest_framework import request, serializers


class BaseSerializer(serializers.Serializer):
    """Serializer with common logic."""

    def __init__(self, *args, **kwargs) -> None:
        """Set current user."""
        super().__init__(*args, **kwargs)
        self._request: request.Request = self.context.get("request")
        self._user = getattr(self._request, "user", None)

    @property
    def _meta(self):
        """Get `Meta` class.

        Used to avoid adding `pylint: disable=no-member`

        """
        return self.Meta


class ModelBaseSerializer(BaseSerializer, serializers.ModelSerializer):
    """Model Serializer with common logic."""

    def get_instance(self, attrs: dict):
        """Get instance depending on request."""
        if self.instance:  # if it's update request
            return copy.deepcopy(self.instance)
        # If attrs have `id` data, get instance form db
        # if it is a create request, we return empty instance
        instance_id = attrs.get("id")
        instance = self._meta.model.objects.filter(pk=instance_id).first()
        return instance or self._meta.model()

    def prepare_instance(self, attrs: dict):
        """Prepare instance depending on create/update.

        If `create` used, create empty instance and set fields' values with
        received data. If `update` used, update existing instance with received
        data.

        """
        # Prepare instance depending on create/update
        instance = self.get_instance(attrs)

        # skip creating/updating instance related objects
        relations = self._get_relations_fields_names()

        # Set new data for instance, while ignoring relations
        for attr, value in attrs.items():
            if attr not in relations:
                setattr(instance, attr, value)

        return instance

    def validate(self, attrs: dict) -> dict:
        """Call model's `.clean()` method during validation.

        Create:
            Just create model instance using provided data.
        Update:
            `self.instance` contains instance with new data. We apply passed
            data to it and then call `clean` method for this temp instance.

        """
        attrs = super().validate(attrs)

        instance = self.prepare_instance(attrs)

        instance.clean()

        return attrs

    def _get_relations_fields_names(self) -> set[str]:
        """Extract fields with relations before validation."""
        relations = set()

        # Remove related fields from validated data for future manipulations
        for _, field in self.fields.items():
            if field.read_only:
                continue

            if "." in field.source:
                source_attr = field.source.split(".")[0]
                relations.add(source_attr)
                continue

            is_many_model_serializer = isinstance(
                field,
                serializers.ListSerializer,
            ) and isinstance(
                field.child,
                serializers.ModelSerializer,
            )
            is_model_serializer = isinstance(
                field,
                serializers.ModelSerializer,
            )
            is_m2m_serializer = isinstance(
                field,
                serializers.ManyRelatedField,
            )
            if (
                is_many_model_serializer
                or is_model_serializer
                or is_m2m_serializer
            ):
                relations.add(field.source)

        return relations
