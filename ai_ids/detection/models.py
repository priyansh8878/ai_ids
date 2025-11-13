from django.db import models

class NetworkEvent(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    source_ip = models.GenericIPAddressField()
    destination_ip = models.GenericIPAddressField()
    protocol = models.CharField(max_length=10)
    packet_size = models.IntegerField()
    prediction = models.CharField(max_length=50, blank=True)
    explanation = models.TextField(blank=True)

    def __str__(self):
        return f"{self.source_ip} → {self.destination_ip} ({self.prediction})"
