from __future__ import unicode_literals

from django.core.paginator import Paginator, InvalidPage
from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from .forms import SearchForm
from ..product.utils import products_with_details, products_with_availability


def paginate_results(results, get_data, paginate_by=settings.PAGINATE_BY):
    paginator = Paginator(results, paginate_by)
    page_number = get_data.get('page', 1)
    try:
        page = paginator.page(page_number)
    except InvalidPage:
        raise Http404('No such page!')
    return page


def evaluate_search_query(form, request):
    results = products_with_details(request.user) & form.search()
    return products_with_availability(results, discounts=request.discounts,
                                      local_currency=request.currency)


def search(request):
    if not settings.ENABLE_SEARCH:
        raise Http404('No such page!')
    form = SearchForm(data=request.GET or None)
    if form.is_valid():
        query = form.cleaned_data.get('q', '')
        results = evaluate_search_query(form, request)
    else:
        query, results = '', []
    page = paginate_results(list(results), request.GET)
    ctx = {
        'query': query,
        'results': page,
        'query_string': '?q=%s' % query}
    return render(request, 'search/results.html', ctx)