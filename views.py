# views.py



class DummyView(object):
    std_msg = "This is {}. You have been succesfully authenticated and authorized!"
    
    @staticmethod
    def hidden_view_1(request, response):
        response["msg"] = DummyView.std_msg.format("hidden view 1")
        return response
    
    @staticmethod
    def hidden_view_2(request, response):
        response["msg"] = DummyView.std_msg.format("hidden view 2")
        return response
    
    @staticmethod
    def hidden_view_3(request, response):
        response["msg"] = DummyView.std_msg.format("hidden view 3")
        return response
