def menu_links(request):
    return {
        menu_links: [
            {'url': 'main', 'active':['main'], 'name': 'в дом'}, 
            {'url': 'products:all', 'active':['products:all', 'products:category'], 'name': 'в продукты'}, 
            {'url': 'contact', 'active':['contact'], 'name': 'в контакты'}
        ],
    }
