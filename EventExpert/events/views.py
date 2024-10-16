from django.shortcuts import get_object_or_404, render, redirect
from rest_framework import generics, permissions
from .models import Event, EmailList
from .serializers import EventSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .forms import EmailForm, MessageForm



# Dashboard: List events the user created and events they are attending
class EventDashboardView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can access

    def get_queryset(self):
        user = self.request.user
        # Return events where the user is the creator or an attendee
        return Event.objects.filter(creator=user) | Event.objects.filter(attendees=user)

# Create a new event
class CreateEventView(generics.CreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically assign the event's creator as the logged-in user
        serializer.save(creator=self.request.user)

# Join an existing event
@api_view(['POST'])
def join_event(request, pk):
    event = get_object_or_404(Event, pk=pk)  # Retrieve the event by its primary key (pk)
    event.attendees.add(request.user)  # Add the requesting user to the attendees list
    return Response({"message": "You have joined the event."})

# Optionally, if you want a view to handle specific event details later
class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()  # Retrieve any event
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]


def add_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_email')  # Redirect after saving email
        else:
            return render(request, 'add_email.html', {'form': form, 'error': 'Invalid email'})
    else:
        form = EmailForm()
    return render(request, 'add_email.html', {'form': form})

def send_bulk_email(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email_list = EmailList.objects.all()
            recipient_list = [email.email for email in email_list]
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    recipient_list
                )
                return render(request, 'send_bulk_email.html', {'form': form, 'success_message': 'Emails sent successfully!'})
            except Exception as e:
                return render(request, 'send_bulk_email.html', {'form': form, 'error_message': f"An error occurred: {e}"})
    else:
        form = MessageForm()
    return render(request, 'send_bulk_email.html', {'form': form})