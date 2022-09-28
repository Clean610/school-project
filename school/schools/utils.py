from django.core.paginator import Paginator

class InvalidPage(Exception):
    pass

class PageNotAnInteger(InvalidPage):
    pass

class EmptyPage(InvalidPage):
    pass


def get_paginator(request, qs):
    try:
        page = int(request.GET.get("page", 1))
        limit = int(request.GET.get("limit", 10))
    except ValueError:
        page, limit = 1,10

    paginator = Paginator(qs, limit)

    try:
        page_object = paginator.page(page)
        object_list = page_object.object_list

    except (InvalidPage, PageNotAnInteger, EmptyPage):
        return qs, None, None
    return object_list, paginator.count, page