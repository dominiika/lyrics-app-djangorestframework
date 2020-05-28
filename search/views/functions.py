from django.core.paginator import Paginator, EmptyPage


class PaginatedSerializer:
    def __init__(self, qs, serializer, page_size, page_number):
        self.qs = qs
        self.serializer = serializer
        self.page_size = page_size
        self.page_number = page_number
        self.paginator = None
        self.num_pages = None
        self.paginated_serializer = None

    def _get_paginator(self):
        self.paginator = Paginator(self.qs.distinct(), self.page_size)

    def _get_number_of_paginator_pages(self):
        self._get_paginator()
        self.num_pages = self.paginator.num_pages

    def get_paginated_serializer(self):
        self._get_number_of_paginator_pages()
        try:
            self.paginated_serializer = self.serializer(
                self.paginator.page(self.page_number), many=True,
            )
        except EmptyPage:
            self.paginated_serializer = self.serializer(
                self.paginator.page(self.paginator.num_pages), many=True,
            )
