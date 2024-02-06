from django.shortcuts import render

def render_recipe(request, form):
        return render(
            request,
            'authors/pages/dashboard_recipe.html',
            context={
                'form': form
            }
        )