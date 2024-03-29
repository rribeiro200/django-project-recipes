from django.core.paginator import Paginator
import math
import string as s
from random import SystemRandom as sr

def make_pagination_range(
    page_range,
    qty_pages,
    current_page,
):
    middle_range = math.ceil(qty_pages / 2) # 2
    start_range = current_page - middle_range # 1 - 2 = -1
    stop_range = current_page + middle_range # 1 + 2
    total_pages = len(page_range) # 21

    start_range_offset = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset

    if stop_range >= total_pages:
        start_range = start_range - abs(total_pages - stop_range)

    pagination = page_range[start_range:stop_range]
    return {
        'pagination': pagination,
        'page_range': page_range,
        'qty_pages': qty_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': current_page > middle_range,
        'last_page_out_of_range': stop_range < total_pages,
    }

def make_pagination(request, queryset, per_page, qty_pages=4):
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1

    # Instancia paginator passando o objeto, e quantos objetos serão exibidos por página.
    paginator = Paginator(queryset, per_page)

    # Retorna a página atual - <Page 1 of 12>
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        paginator.page_range,  # Se existe 12 páginas, por exemplo, retorna uma tupla: range(1, 13)
        qty_pages,
        current_page # Pega a página atual através do QuerySearch do GET na página
    )
    
    return page_obj, pagination_range

def generate_secret_key():
    secret_key = ''.join(sr().choices(s.ascii_letters + s.punctuation, k=64))
    return secret_key