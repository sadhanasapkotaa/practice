from rest_framework.pagination import CursorPagination


class OrderCursorPagination(CursorPagination):
    page_size = 10
    page_size_query_param = 'page_size'  # allow clients to request a different size
    max_page_size = 100
    ordering = '-created_at'
