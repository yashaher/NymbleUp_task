from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Sum, F
from datetime import timedelta, date
from .models import MenuItem, Order
from .serializers import MenuItemSerializer, OrderSerializer

class MenuItemViewSet(viewsets.ModelViewSet): 
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        status_param = self.request.query_params.get('status')
        if status_param:
            return self.queryset.filter(status=status_param)
        return self.queryset

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = request.data.get("status", instance.status)
        instance.save()
        return Response(OrderSerializer(instance).data)

@api_view(['GET'])
def average_daily_sales(request):
    today = date.today()
    weekday_sales = []

    for i in range(1, 6):  
        day = today - timedelta(days=(today.weekday() - i) % 7)
        orders = Order.objects.filter(
            timestamp__date=day,
            status='completed'
        )
        revenue = orders.annotate(
            total=Sum(F('items__menu_item__price') * F('items__quantity'))
        ).aggregate(total_sales=Sum('total'))['total_sales'] or 0

        weekday_sales.append({
            'day': day.strftime('%A'),
            'average_sales': round(float(revenue), 2)
        })

    return Response(weekday_sales)
