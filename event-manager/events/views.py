import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from .models import Event, Registration

# Home page dashboard view
def home(request):
    return render(request, 'index.html')

# 1. View Event List (GET /api/events)
def event_list(request):
    if request.method == 'GET':
        events = Event.objects.all()
        data = [{
            'id': e.id,
            'title': e.title,
            'description': e.description,
            'date': e.date.isoformat(),
            'location': e.location
        } for e in events]
        return JsonResponse(data, safe=False)

# 2. View Event Details (GET /api/events/<id>)
def event_detail(request, event_id):
    if request.method == 'GET':
        event = get_object_or_404(Event, pk=event_id)
        data = {
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'date': event.date.isoformat(),
            'location': event.location
        }
        return JsonResponse(data)

# 3. Submit Registration Form (POST /api/register)
@csrf_exempt
def register_event(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            event_id = body.get('event_id')
            name = body.get('user_name')
            email = body.get('user_email')

            if not all([event_id, name, email]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            event = get_object_or_404(Event, pk=event_id)
            
            registration = Registration.objects.create(
                event=event,
                user_name=name,
                user_email=email
            )
            
            return JsonResponse({
                'message': 'Registration successful!',
                'registration_id': registration.id
            }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

# 4. View or Cancel Registrations (GET & POST /api/manage-registrations)
@csrf_exempt
def manage_registrations(request):
    # View by email
    if request.method == 'GET':
        email = request.GET.get('email')
        if not email:
            return JsonResponse({'error': 'Email parameter is required'}, status=400)
        
        regs = Registration.objects.filter(user_email=email)
        data = [{
            'registration_id': r.id,
            'event_title': r.event.title,
            'user_name': r.user_name,
            'date_registered': r.registration_date.isoformat()
        } for r in regs]
        return JsonResponse(data, safe=False)

    # Cancel by registration ID
    elif request.method == 'POST':
        body = json.loads(request.body)
        reg_id = body.get('registration_id')
        
        if not reg_id:
            return JsonResponse({'error': 'Registration ID is required'}, status=400)
            
        registration = get_object_or_404(Registration, pk=reg_id)
        registration.delete()
        return JsonResponse({'message': 'Registration cancelled successfully!'})