# router.py

from utils import RequestOp
from views import DummyView
from custom_errors import Resource404, CustomError

"""
Rules for routing requests
"""
rules = {
    'test-1':DummyView.hidden_view_1,
    'test-2':DummyView.hidden_view_2,
    'test-3':DummyView.hidden_view_3,
}

ERROR_BUNDLE_KEYS = ["url"]

def route(request, response):
    _url = RequestOp.getURL(request)
    if _url in rules:
        return rules[_url](request, response)
    else:
        raise Resource404(Resource404.MSG_404, CustomError.bundle(ERROR_BUNDLE_KEYS, _url))
