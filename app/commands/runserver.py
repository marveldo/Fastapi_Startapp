from ..base.basecommand import BaseCommand


class RunserverCommand(BaseCommand):
    """Command to run the fastapi server

    Args:
        BaseCommand (_type_): _description_
    """

    def handle(self, *args, **kwargs):
        
        import uvicorn

        host = "127.0.0.1"
        port = 8000

        if len(args) > 0 :
            try :
                port = int(args[0])
            except ValueError :
                host = args[0]
            
        if len(args) > 1 :
            try: 
                port = int(args[1])
            except ValueError :
                print('Invalid Port number given host should always come before port')
                return 
            
        if port <= 1023 or port >= 65536:
            print('Invalid port can only be of range 1023-65536')
        uvicorn.run(app="app.main:app", host=host, port=port , reload=True)


