class BaseCommand :
    def handle(self,*args, **kwargs):
        """handles the incoming command handle method must be overwritten when making 
        a new command unless it raises a Not Implemented Error

        Raises:
            NotImplementedError: raises a notimplemented error when handle is not overwritten
        """
        raise NotImplementedError("Subclass must be implemented and handle method must be overwritten")
    
    def run(self, *args, **kwargs):
        """Run the handle command
        """
        self.handle(*args , **kwargs)

