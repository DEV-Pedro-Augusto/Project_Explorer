class System:
    
    def __init__(self, page, ft, time,os,httpx,create_client,Client,SyncClientOptions,SUPABASE_URL,SUPABASE_KEY, mainView, models, MainTest, Controller, AppServices):
        self.page = page
        self.ft = ft 
        self.time = time 
        self.os = os
        self.httpx = httpx
        self.supabase = {"create_client":create_client,"client":Client,"SyncClientOptions":SyncClientOptions,"SUPABASE_URL":SUPABASE_URL,"SUPABASE_KEY":SUPABASE_KEY}
        self.view = mainView
        self.model = models
        self.test = MainTest
        self.controller = Controller
        self.service = AppServices

