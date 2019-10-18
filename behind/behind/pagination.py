from rest_framework.pagination import CursorPagination


class CreatedAtCursorPagination(CursorPagination):
    page_size = 50
    ordering = '-created_at'

    def paginate_queryset(self, queryset, request, view=None):
        if 'all' == request.query_params.get(self.cursor_query_param):
            return None
        return super().paginate_queryset(queryset, request, view)
