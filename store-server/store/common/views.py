class TitleMixin:
    title = None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) #super(TitleMixin, self).get_context_data()
        context['title'] = self.title
        return context
