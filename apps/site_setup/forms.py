from django import forms

from apps.site_setup.models import Setup
from utils.image_tools import convert_image, resize_and_pad


class SetupModelForm(forms.ModelForm):

    class Meta:
        model = Setup
        fields = '__all__'

    def _process_image(self, image_file, aspect_w, aspect_h, target_w):
        if image_file:
            try:
                resized_file = resize_and_pad(image_file, aspect_w, aspect_h, target_w)
                converted_file = convert_image(resized_file, target_format='WEBP')
                return converted_file
            except Exception as e:
                self.add_error(None, f'Erro ao processar imagem: {e}')
        return None

    def save(self, commit):
        setup = super().save(commit=False)
        if 'logo' in self.changed_data and self.cleaned_data.get('logo'):
            setup.logo = self._process_image(self.cleaned_data['logo'], 4, 3, 512)
        if 'banner' in self.changed_data and self.cleaned_data.get('banner'):
            setup.banner = self._process_image(self.cleaned_data['banner'], 16, 9, 1920)
        if 'unknown_car' in self.changed_data and self.cleaned_data.get('unknown_car'):
            setup.unknown_car = self._process_image(self.cleaned_data['unknown_car'], 4, 3, 1920)
        if commit:
            setup.save()
            self.save_m2m()
        return setup
