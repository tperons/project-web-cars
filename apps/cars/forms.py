from django import forms

from apps.cars.models import Car, CarImages
from utils.image_tools import convert_image, resize_and_pad


class CarModelForm(forms.ModelForm):

    front_view = forms.ImageField(label='Visão frontal', required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    side_view = forms.ImageField(label='Visão lateral', required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    back_view = forms.ImageField(label='Visão traseira', required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    interior_view = forms.ImageField(label='Visão interior', required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Car
        exclude = ['status', 'created_at', 'sold_at']
        widgets = {
            'brand': forms.Select(attrs={'class': 'form-select'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Corolla, Civic, Onix...'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 2022'}),
            'version': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: SE 2.5'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 22000'}),
            'ai_description': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição Detalhada do Veículo', 'rows': 4}),
            'mileage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 180000'}),
            'transmission': forms.Select(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Prata'}),
            'optionals': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'cover': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def _process_image(self, image_file):
        if image_file:
            try:
                resized_file = resize_and_pad(image_file, 4, 3, 1920)
                converted_file = convert_image(resized_file, target_format='WEBP')
                return converted_file
            except Exception as e:
                self.add_error(None, f'Erro ao processar imagem: {e}')
        return None

    def save(self, commit=True):
        car = super().save(commit=False)
        if 'cover' in self.changed_data and self.cleaned_data.get('cover'):
            car.cover = self._process_image(self.cleaned_data.get('cover'))
        if commit:
            car.save()
            self.save_m2m()
            images_data = {}
            if 'front_view' in self.changed_data and self.cleaned_data.get('front_view'):
                images_data['front_view'] = self._process_image(self.cleaned_data.get('front_view'))
            if 'side_view' in self.changed_data and self.cleaned_data.get('side_view'):
                images_data['side_view'] = self._process_image(self.cleaned_data.get('side_view'))
            if 'back_view' in self.changed_data and self.cleaned_data.get('back_view'):
                images_data['back_view'] = self._process_image(self.cleaned_data.get('back_view'))
            if 'interior_view' in self.changed_data and self.cleaned_data.get('interior_view'):
                images_data['interior_view'] = self._process_image(self.cleaned_data.get('interior_view'))
            if images_data:
                CarImages.objects.update_or_create(
                    car=car,
                    defaults=images_data
                )
        return car
