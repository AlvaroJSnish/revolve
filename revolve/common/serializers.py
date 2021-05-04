import json
from uuid import UUID

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class GenericPaginationSerializer(PageNumberPagination):
    PAGINATE_BY = 10
    page_size = PAGINATE_BY

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'prev': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data,
            'total_pages': self.page.paginator.num_pages
        })


class MassivePaginationSerializer(PageNumberPagination):
    PAGINATE_BY = 150
    page_size = PAGINATE_BY

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'prev': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data,
            'total_pages': self.page.paginator.num_pages
        })


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)
