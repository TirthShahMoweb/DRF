class Custom_Middleware:
    def __init__(self, get_response):
        self.get_response = get_response
        pass

    def __call__(self, request,*args, **kwds):
        # print("This is a custom middleware")
        response = self.get_response(request)

        user_agent = request.META.get('HTTP_USER_AGENT')
        # print("----------")
        # print(user_agent)
        # print("----------")
        return response