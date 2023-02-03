from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, BaseThrottle


class CustomAnonRateThrottle(BaseThrottle):
    rate = '10/min'
    def allow_request(self, request, view):
        if request.user and request.user.is_authenticated:
            return False




class CustomUserRateThrottle(BaseThrottle):
    rate = '20/min'
    def allow_request(self, request, view):
        if request.user and request.user.is_authenticated:
            return True

