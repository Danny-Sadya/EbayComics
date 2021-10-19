from django.shortcuts import render, get_object_or_404, redirect
from django.forms.models import model_to_dict
from django.views import View

from .forms import SnipeForm
from .models import SnipeModel
from .scripts.get_comics_title import get_comics_title


def dashboard_control(request, *args, **kwargs):
    snipe_items = SnipeModel.objects.all()
    form = SnipeForm()

    if request.method == "POST":
        form = SnipeForm(request.POST)
        if form.is_valid():
            try:
                title = get_comics_title(request.POST['gocollect_link'])
            except Exception as ex:
                print('error in getting comics title in views: ', ex)
                title = request.POST['gocollect_link']
            SnipeModel.objects.create(title=title, **form.cleaned_data)
        else:
            print(form.errors)
        return redirect('/dashboard/')
    snipe_items = SnipeModel.objects.all()
    return render(request, 'snipe_control.html', context={'snipe_items': snipe_items, 'form': form})

def create_snipe(request):
    template_name = 'snipe_control.html'
    form = SnipeForm(request.POST, request.FILES)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('/dashboard/')
        else:
            form = SnipeForm()
            return render(request, template_name, context={'form': form})
    else:
        context = {'form': form}
        return render(request, template_name, context)


def delete_snipe(request, pk):
    if request.user.is_authenticated:
        snipe_item = get_object_or_404(SnipeModel, pk=pk)
        snipe_item.delete()
        return redirect('/dashboard/')
    else:
        return redirect('/dashboard/')


def edit_snipe(request, pk):
    snipe_item = get_object_or_404(SnipeModel, pk=pk)
    form = SnipeForm(instance=snipe_item, initial=model_to_dict(snipe_item))

    if request.method == "POST":
        form = SnipeForm(request.POST, instance=snipe_item, initial=model_to_dict(snipe_item))
        if form.is_valid():
            snipe_item = form.save(commit=False)
            snipe_item.save()
            return redirect('/dashboard/')
        else:
            form = SnipeForm(instance=snipe_item, initial=model_to_dict(snipe_item))
            return render(request, 'snipe_edit.html', context={'form': form})
    else:
        context = {'form': form}
        return render(request, 'snipe_edit.html', context)

