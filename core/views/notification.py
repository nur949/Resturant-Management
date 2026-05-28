from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ..models import Notification

@login_required
def get_notifications(request):
    # Get unread notifications for user or global ones
    notifications = Notification.objects.filter(is_read=False).order_by('-created_at')[:10]
    data = []
    for n in notifications:
        data.append({
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'time': n.created_at.strftime('%H:%M')
        })
    return JsonResponse({'status': 'success', 'notifications': data, 'count': notifications.count()})

@login_required
def mark_as_read(request, pk):
    if request.method == 'POST':
        notification = Notification.objects.get(pk=pk)
        notification.is_read = True
        notification.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
