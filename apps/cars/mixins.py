from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404

from apps.cars.models import Car


class OwnerOrStaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return True
        if hasattr(self, 'get_object'):
            car = self.get_object()
        else:
            pk = self.kwargs.get('pk')
            if not pk:
                return False
            car = get_object_or_404(Car, pk=pk)
        return car.owner == user
