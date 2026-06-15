from __future__ import annotations

from functools import wraps
from typing import Callable, Iterable, TypeVar

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden


TResponse = TypeVar("TResponse", bound=HttpResponse)


def require_user_types(*allowed: str):

    def decorator(view_func: Callable[[HttpRequest, ...], TResponse]):
        @login_required
        @wraps(view_func)
        def _wrapped(request: HttpRequest, *args, **kwargs) -> TResponse:
            user_type = getattr(request.user, "user_type", None)
            if user_type in allowed:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("Forbidden")

        return _wrapped

    return decorator

