from django.shortcuts import render, redirect
from .models import NetworkEvent
from .ai_engine import predict_intrusion, explain_intrusion

def dashboard(request):
    """
    Displays the main dashboard with the latest intrusion analysis results.
    """
    events = NetworkEvent.objects.order_by('-timestamp')[:20]
    context = {
        'events': events,
        'title': 'AI Intrusion Detection Dashboard'
    }
    # ✅ Correct: points to 'detection/dashboard.html'
    return render(request, 'detection/dashboard.html', context)


def analyze_event(request):
    """
    Allows the user to input a network event manually and get an AI + GPT analysis.
    """
    if request.method == 'POST':
        # Get form data safely using .get() to avoid KeyErrors
        src_ip = request.POST.get('source_ip')
        dst_ip = request.POST.get('destination_ip')
        protocol = request.POST.get('protocol', 'tcp')
        packet_size = int(request.POST.get('packet_size', 0))
        duration = int(request.POST.get('duration', 0))

        # Map protocol to numerical value for model
        proto_map = {'tcp': 0, 'udp': 1, 'icmp': 2}
        proto_val = proto_map.get(protocol.lower(), 0)

        # Prepare features for ML model
        features = [duration, packet_size, 500, proto_val]

        # Get AI model prediction
        prediction = predict_intrusion(features)

        # Prepare event data for GPT explanation
        event_data = {
            "source_ip": src_ip,
            "destination_ip": dst_ip,
            "protocol": protocol,
            "packet_size": packet_size
        }

        # Get GPT explanation (OpenAI integration)
        explanation = explain_intrusion(event_data, prediction)

        # Save to database
        NetworkEvent.objects.create(
            source_ip=src_ip,
            destination_ip=dst_ip,
            protocol=protocol,
            packet_size=packet_size,
            prediction=prediction,
            explanation=explanation
        )

        # Redirect back to dashboard
        return redirect('dashboard')

    # ✅ Render with base.html automatically (extends base in template)
    return render(request, 'detection/analyze.html', {'title': 'Analyze Network Event'})
