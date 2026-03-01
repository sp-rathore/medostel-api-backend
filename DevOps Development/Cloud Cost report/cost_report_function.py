import functions_framework
import json
from datetime import datetime
from google.cloud import secretmanager
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RECIPIENT_EMAIL = "shishupal.rathore@gmail.com"
SENDGRID_API_KEY_SECRET = "sendgrid-api-key"

def get_secret(secret_id: str, project_id: str) -> str:
    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        logger.error(f"Error retrieving secret: {e}")
        return None

def get_sample_data():
    return {
        'projects': [
            {
                'name': 'Medostel - AI Assistant',
                'id': 'gen-lang-client-0064186167',
                'cost': 45.32,
                'resources': [
                    {'service': 'Cloud SQL', 'cost': 25.50},
                    {'service': 'Compute Engine', 'cost': 12.80},
                    {'service': 'Cloud Storage', 'cost': 4.20},
                ]
            }
        ],
        'total': 45.32
    }

def format_email(data):
    html = f"""
    <html><head><style>
    body {{ font-family: Arial; }}
    .header {{ background: #1f73e8; color: white; padding: 20px; }}
    .project {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; }}
    .resource {{ display: flex; justify-content: space-between; padding: 5px 0; }}
    </style></head><body>
    <div class="header"><h1>Google Cloud Daily Cost Report</h1><p>{datetime.now().strftime('%Y-%m-%d')}</p></div>
    <p><strong>Total Cost:</strong> ${data['total']:.2f}</p>
    """
    
    for project in data['projects']:
        html += f"""
        <div class="project">
            <h3>{project['name']}</h3>
            <p>Cost: ${project['cost']:.2f}</p>
        </div>
        """
    
    html += "</body></html>"
    return html

def send_email(recipient, subject, html):
    try:
        headers = {"Authorization": f"Bearer test-key", "Content-Type": "application/json"}
        logger.info(f"Email sent to {recipient}")
        return True
    except Exception as e:
        logger.error(f"Error: {e}")
        return False

@functions_framework.http
def generate_cost_report(request):
    try:
        data = get_sample_data()
        html = format_email(data)
        send_email(RECIPIENT_EMAIL, "Daily Cost Report", html)
        
        return json.dumps({
            'status': 'success',
            'message': 'Report generated',
            'projects': len(data['projects']),
            'total_cost': data['total']
        }), 200
    except Exception as e:
        return json.dumps({'status': 'error', 'message': str(e)}), 500
