import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from apps.cars.forms import CarModelForm
from apps.cars.mixins import OwnerOrStaffRequiredMixin
from apps.cars.models import Brand, Car, Optional


class CarListView(ListView):
    model = Car
    template_name = 'cars/pages/car_list.html'
    ordering = ('-pk',)
    context_object_name = 'cars'
    paginate_by = 9

    def get_queryset(self):
        return (
            super().get_queryset()
            .select_related('brand')
            .prefetch_related('optionals')
            .exclude(status=Car.Status.SOLD)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({'title': 'Nosso Estoque', })
        return context


class CarDetailView(DetailView):
    model = Car
    template_name = 'cars/pages/car_detail.html'
    context_object_name = 'car'

    def get_queryset(self):
        return (
            super().get_queryset()
            .select_related('brand')
            .prefetch_related('image', 'optionals')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.get_object()
        whatsapp_message = (
            f'Olá! Tenho interesse no veículo {car.brand.name} {car.model} {car.year}. '
            f'Poderiam dar-me mais informações?'
        )
        context.update({
            'title': f'{car.brand.name} {car.model} {car.version}',
            'page_description': car.description,
            'og_image': car.cover,
            'whatsapp_message': whatsapp_message,
        })
        return context


class CarSearchView(CarListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        self.search_value = self.request.GET.get('search', '').strip()
        if self.search_value:
            queryset = queryset.filter(
                Q(model__icontains=self.search_value) |
                Q(brand__name__icontains=self.search_value)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': f'Busca: {self.search_value[:16]}',
            'search_value': self.search_value
        })
        return context


class CarCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Car
    template_name = 'cars/pages/car_form.html'
    form_class = CarModelForm
    success_url = reverse_lazy('users:dashboard')
    success_message = "O veículo %(brand)s %(model)s foi cadastrado com sucesso!"
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        car = form.save(commit=False)
        car.owner = self.request.user
        car.save()
        form.save_m2m()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Cadastro de Veículos',
            'car_form': context['form'],
        })
        return context


class CarUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Car
    template_name = 'cars/pages/car_form.html'
    form_class = CarModelForm
    success_url = reverse_lazy('users:dashboard')
    success_message = "O veículo %(brand)s %(model)s foi atualizado com sucesso!"
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        return super().get_queryset().select_related('brand').prefetch_related('image', 'optionals')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': f'Editanto {self.object.brand} {self.object.model} {self.object.version}',
            'car_form': context['form'],
        })
        return context


class CarSoldView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        car = get_object_or_404(Car, pk=pk)
        car.status = Car.Status.SOLD
        car.sold_at = timezone.now()
        car.save(update_fields=['status', 'sold_at'])
        messages.success(request, f'O veículo "{car.brand} {car.model}" foi marcado como vendido.')
        return redirect('users:dashboard')


class CarDeleteView(LoginRequiredMixin, OwnerOrStaffRequiredMixin, DeleteView):
    model = Car
    template_name = 'cars/pages/car_delete.html'
    context_object_name = 'car'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('users:dashboard')

    def form_valid(self, form):
        messages.success(self.request, f'O veículo "{self.object.brand} {self.object.model}" foi apagado com sucesso.')
        return super().form_valid(form)


class CreateRelatedObjectView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            model_type = data.get('model_type')
            name = data.get('name', '').strip()
            if not name:
                return JsonResponse({'error': 'O nome não pode estar vazio.'}, status=400)
            obj = None
            if model_type == 'brand':
                obj, created = Brand.objects.get_or_create(name=name)
            elif model_type == 'optional':
                obj, created = Optional.objects.get_or_create(name=name)
            else:
                return JsonResponse({'error': 'Tipo de modelo inválido.'}, status=400)
            if obj:
                return JsonResponse({
                    'id': obj.pk,
                    'name': obj.name,
                    'created': created
                }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Dados JSON inválidos.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            return JsonResponse({'error': str(e)}, status=500)
